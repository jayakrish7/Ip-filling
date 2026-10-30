# Low-Level Design (LLD) Document
## Automated Legal Document Generation for IP Filings

> **Document Version:** 1.0.0  
> **System Scope:** Microservices Architecture, API Gateway, REST Endpoints, Data Schemas & NFR Specifications

---

## 1. System Architecture

```
+-----------------------------------------------------------------------------+
|                               API GATEWAY LAYER                              |
|          (Reverse Proxy / Authentication / Rate Limiting / TLS 1.3)          |
+-----------------------------------------------------------------------------+
                                       |
                   +-------------------+-------------------+
                   |                                       |
+-------------------------------------+ +-------------------------------------+
|            SERVICE LAYER            | |            SERVICE LAYER            |
|       (Filing Management API)       | |     (GenAI / SLM Generation API)    |
|   - Outcome Predictor Service (ML)  | |   - Clause Summarizer Service (SLM) |
|   - Sequence Forecaster Service(DL) | |   - RAG & Drafting Engine (GenAI)   |
+-------------------------------------+ +-------------------------------------+
                   |                                       |
                   +-------------------+-------------------+
                                       |
+-----------------------------------------------------------------------------+
|                                 DATA LAYER                                  |
|   - PostgreSQL (Transactional Filings, Users, Agent Action Audit Logs)      |
|   - Vector DB (FAISS / Chroma for Legal Precedent & Statute Embeddings)     |
|   - Redis & RabbitMQ (Distributed Job Queue for Asynchronous Doc Generation) |
+-----------------------------------------------------------------------------+
```

---

## 2. REST API Contracts (OpenAPI Specification)

### 2.1 `POST /filings`
Creates a new IP filing record and triggers initial risk assessment scoring.

```yaml
Request:
  Method: POST
  Path: /api/v1/filings
  Headers:
    Content-Type: application/json
    Authorization: Bearer <JWT_TOKEN>
  Body:
    filing_type: "Patent" # Enum: Patent, Trademark, Design, Copyright
    title: "Method and System for Neural IP Risk Scoring"
    specification_word_count: 4500
    claims_count: 15
    prior_art_similarity: 0.25
    examiner_workload: 22
    attorney_assistance: true
    fees_paid: 1850.00

Response:
  Status: 201 Created
  Body:
    filing_id: "IP-2026-10492"
    status: "Draft"
    predicted_outcome: "Approved"
    confidence_score: 0.942
    created_at: "2026-07-23T10:00:00Z"
```

### 2.2 `GET /filings/{id}`
Retrieves detailed metadata, historical prosecution timeline, and audit logs for a filing.

```yaml
Request:
  Method: GET
  Path: /api/v1/filings/IP-2026-10492

Response:
  Status: 200 OK
  Body:
    filing_id: "IP-2026-10492"
    filing_type: "Patent"
    predicted_outcome: "Approved"
    timeline_forecast:
      next_6_months_activity: [4, 5, 3, 4, 6, 5]
    clauses:
      - clause_id: "CLS-991"
        type: "Claims"
        status: "Verified"
```

### 2.3 `POST /filings/{id}/generate-document`
Enqueues an asynchronous document generation job for patent specification and office action responses.

```yaml
Request:
  Method: POST
  Path: /api/v1/filings/IP-2026-10492/generate-document
  Body:
    template_id: "TPL-USPTO-UTILITY-2026"
    include_clauses: ["CLS-991", "CLS-992"]
    export_format: "PDF" # Enum: PDF, DOCX, XML

Response:
  Status: 202 Accepted
  Body:
    job_id: "JOB-DOC-88219"
    status: "QUEUED"
    estimated_completion_seconds: 4
```

### 2.4 `POST /clauses/summarize`
Invokes the Small Language Model (SLM) to summarize long legalese into plain English.

```yaml
Request:
  Method: POST
  Path: /api/v1/clauses/summarize
  Body:
    clause_text: "Under 35 U.S.C. 103, claims 1-10 are rejected as obvious over..."
    max_target_tokens: 60

Response:
  Status: 200 OK
  Body:
    original_tokens: 42
    summary_text: "Claims 1-10 are rejected as obvious based on two combined prior art references."
    inference_latency_ms: 18.4
```

---

## 3. Data Schemas (Database Entity Specifications)

### 3.1 `Filing` Entity
| Field Name | Type | Constraints | Description |
|---|---|---|---|
| `filing_id` | String (PK) | Unique, Indexed | Format: `IP-YYYY-XXXXX` |
| `filing_type` | Enum | Not Null | `Patent`, `Trademark`, `Design`, `Copyright` |
| `word_count` | Integer | > 0 | Specification length |
| `claims_count` | Integer | > 0 | Total independent & dependent claims |
| `prior_art_similarity` | Float | 0.0 to 1.0 | Vector cosine similarity score |
| `examiner_workload` | Integer | >= 0 | Examiner pending docket size |
| `attorney_assistance` | Boolean | Not Null | Whether legal counsel is assigned |
| `fees_paid` | Decimal(10,2) | >= 0 | Official statutory filing fee |
| `filing_outcome` | Enum | Indexed | `Approved`, `Rejected`, `Needs_Revision` |

### 3.2 `Clause` Entity
| Field Name | Type | Constraints | Description |
|---|---|---|---|
| `clause_id` | String (PK) | Unique | `CLS-YYYY-XXXXX` |
| `filing_id` | String (FK) | References Filing | Associated filing |
| `clause_type` | Enum | Indexed | `Claims`, `Prior_Art_Objection`, `Abstract`, etc. |
| `clause_text` | Text | Not Null | Complete legal clause wording |
| `patent_number` | String | Nullable | Referenced patent number (e.g. US10984123B2) |

### 3.3 `Template` Entity
| Field Name | Type | Constraints | Description |
|---|---|---|---|
| `template_id` | String (PK) | Unique | Utility patent or trademark draft template |
| `jurisdiction` | String | Not Null | e.g. `USPTO`, `EPO`, `WIPO` |
| `structure_json` | JSONB | Not Null | Section hierarchy & placeholder tags |

### 3.4 `Agent_Action` Entity (Audit Trail)
| Field Name | Type | Constraints | Description |
|---|---|---|---|
| `action_id` | String (PK) | Unique | UUID |
| `filing_id` | String (FK) | References Filing | Target filing |
| `tool_name` | String | Not Null | MCP tool invoked (`check_prior_art`, etc.) |
| `reasoning_step` | Text | Not Null | Agent chain-of-thought rationale |
| `human_review_required` | Boolean | Not Null | High risk safety trigger flag |

---

## 4. Non-Functional Requirements (NFRs)

### 4.1 Security
- **Encryption at Rest:** All stored filing specifications and sensitive user details encrypted using AES-256-GCM.
- **Encryption in Transit:** TLS 1.3 mandated across external API Gateway and internal service-to-service communication.
- **Access Control:** Role-Based Access Control (RBAC) with granular scopes (`filing:read`, `filing:write`, `agent:override`).

### 4.2 Scalability & Resilience
- **Stateless Microservices:** API services run as containerized stateless instances behind an ALB.
- **Asynchronous Task Queue:** Document generation and vector ingestion executed via Celery + Redis queues with automatic retry policy.

### 4.3 Observability & Auditability
- **Structured Logging:** JSON logs containing `trace_id`, `filing_id`, `timestamp`, and `execution_duration_ms`.
- **Metrics Tracking:** Prometheus exporters monitoring inference latency, queue depth, error rates, and model accuracy drift.
