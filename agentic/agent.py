import os
import sys
import json
import logging

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


# Ensure project root is in python path to access other module functions if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Configure structured audit logging
os.makedirs(os.path.join(os.path.dirname(__file__), "reports"), exist_ok=True)
audit_log_path = os.path.join(os.path.dirname(__file__), "reports", "agent_execution_audit.log")

logging.basicConfig(
    filename=audit_log_path,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [Agentic-AI] %(message)s'
)

# MCP-Style Tool Registry
class AgentTools:
    @staticmethod
    def search_precedents(query: str):
        """MCP Tool: Searches vector index for statutory and case law precedents."""
        return f"[Tool: search_precedents] Found precedent 35 U.S.C. 103 & Graham v. John Deere for query: '{query}'"

    @staticmethod
    def draft_clause(scenario: str):
        """MCP Tool: Drafts patent claim clause wording."""
        return f"[Tool: draft_clause] Drafted utility claim: 'A system for {scenario} comprising a neural risk scorer.'"

    @staticmethod
    def summarize_clause(clause_text: str):
        """MCP Tool: Calls SLM to summarize long legalese."""
        return f"[Tool: summarize_clause] SLM Summary: 'Claim rejected as obvious over prior art vector match.'"

    @staticmethod
    def check_prior_art(prior_art_similarity: float, claims_count: int, attorney_assistance: str):
        """MCP Tool: Evaluates ML model outcome score."""
        risk_score = (prior_art_similarity * 2.0) + (0.05 * claims_count) - (0.3 if attorney_assistance == "Yes" else 0.0)
        predicted_outcome = "Approved" if risk_score < 0.6 else ("Needs_Revision" if risk_score < 0.9 else "Rejected")
        return {"risk_score": round(risk_score, 4), "predicted_outcome": predicted_outcome}

    @staticmethod
    def submit_for_human_review(filing_id: str, reason: str):
        """MCP Tool: Routes high-risk filing to mandatory human paralegal review."""
        return f"[Tool: submit_for_human_review] Filing {filing_id} routed to Human Attorney Queue. Reason: {reason}"

    @staticmethod
    def auto_submit_filing(filing_id: str):
        """MCP Tool: Submits low-risk filing automatically to USPTO API."""
        return f"[Tool: auto_submit_filing] SUCCESS - Filing {filing_id} auto-submitted to USPTO Portal."


class AutonomousIPFilingAgent:
    """
    Autonomous Agent implementing a Perceive -> Reason -> Plan -> Act loop.
    Enforces mandatory human-in-the-loop safety routing for any filing exceeding risk threshold.
    """
    def __init__(self, risk_threshold: float = 0.70):
        self.risk_threshold = risk_threshold
        self.tools = AgentTools()

    def run_filing_workflow(self, filing_data: dict):
        filing_id = filing_data.get("filing_id", "IP-2026-UNKNOWN")
        print(f"\n=======================================================")
        print(f"🤖 [Autonomous Agent] Starting Workflow for Filing: {filing_id}")
        print(f"=======================================================")
        logging.info(f"Starting workflow for filing_id: {filing_id}")

        # 1. PERCEIVE
        print(f"\n1. 👁️ PERCEIVE Stage:")
        prior_art_sim = filing_data.get("prior_art_similarity", 0.0)
        claims = filing_data.get("claims_count", 15)
        attorney = filing_data.get("attorney_assistance", "No")
        print(f"   -> Filing Features: PriorArtSim={prior_art_sim}, Claims={claims}, Attorney={attorney}")
        logging.info(f"PERCEIVE: PriorArtSim={prior_art_sim}, Claims={claims}, Attorney={attorney}")

        # 2. REASON
        print(f"\n2. 🧠 REASON Stage:")
        ml_eval = self.tools.check_prior_art(prior_art_sim, claims, attorney)
        risk_score = ml_eval["risk_score"]
        predicted_outcome = ml_eval["predicted_outcome"]
        print(f"   -> Evaluated Risk Score: {risk_score} | Predicted ML Outcome: {predicted_outcome}")
        logging.info(f"REASON: Risk Score={risk_score}, ML Outcome={predicted_outcome}")

        # 3. PLAN
        print(f"\n3. 📋 PLAN Stage:")
        steps = []
        steps.append("Call search_precedents for prior art comparison")
        steps.append("Call draft_clause for specification enhancement")

        if risk_score > self.risk_threshold or predicted_outcome in ["Rejected", "Needs_Revision"]:
            steps.append(f"MANDATORY ROUTING: Call submit_for_human_review (Risk Score {risk_score} > Threshold {self.risk_threshold})")
            is_high_risk = True
        else:
            steps.append("Call auto_submit_filing")
            is_high_risk = False

        for idx, step in enumerate(steps, 1):
            print(f"   Step {idx}: {step}")
        logging.info(f"PLAN: Planned steps = {steps}")

        # 4. ACT
        print(f"\n4. ⚡ ACT Stage (Executing MCP Tools):")
        
        # Tool Call 1
        res1 = self.tools.search_precedents(f"Prior art sim {prior_art_sim}")
        print(f"   -> Executed: {res1}")
        logging.info(f"ACT: {res1}")

        # Tool Call 2
        res2 = self.tools.draft_clause(filing_data.get("title", "neural network invention"))
        print(f"   -> Executed: {res2}")
        logging.info(f"ACT: {res2}")

        # Final Action - Safety Routing Enforcement
        if is_high_risk:
            reason = f"High Risk Score ({risk_score}) / ML Outcome '{predicted_outcome}' requires human attorney sign-off."
            final_res = self.tools.submit_for_human_review(filing_id, reason)
            print(f"   -> 🚨 SAFETY GUARDRAIL TRIGGERED: {final_res}")
            logging.warning(f"ACT GUARDRAIL: {final_res}")
        else:
            final_res = self.tools.auto_submit_filing(filing_id)
            print(f"   -> ✅ AUTO-SUBMITTED: {final_res}")
            logging.info(f"ACT SUCCESS: {final_res}")

        audit_summary = {
            "filing_id": filing_id,
            "risk_score": risk_score,
            "predicted_outcome": predicted_outcome,
            "is_high_risk": is_high_risk,
            "final_action": final_res
        }

        report_json_path = os.path.join(os.path.dirname(__file__), "reports", "agent_summary.json")
        with open(report_json_path, 'w') as f:
            json.dump(audit_summary, f, indent=4)

        return audit_summary

if __name__ == "__main__":
    agent = AutonomousIPFilingAgent(risk_threshold=0.70)
    
    # Test 1: High Risk Sample -> Must Route to Human Review
    high_risk_filing = {
        "filing_id": "IP-2026-99011",
        "title": "Autonomous Neural Claim Writer",
        "prior_art_similarity": 0.45,
        "claims_count": 25,
        "attorney_assistance": "No"
    }
    agent.run_filing_workflow(high_risk_filing)

    # Test 2: Low Risk Sample -> Auto Submits
    low_risk_filing = {
        "filing_id": "IP-2026-10204",
        "title": "Low Risk Semiconductor Packaging",
        "prior_art_similarity": 0.15,
        "claims_count": 8,
        "attorney_assistance": "Yes"
    }
    agent.run_filing_workflow(low_risk_filing)
