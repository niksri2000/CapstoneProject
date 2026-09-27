import json
import time
import uuid

def review_gate_v1(report, decision, reviewer_note=""):
    """
    Evaluates a report's readiness for downstream consumption.
    
    Parameters:
    - report: dict, the source report/memo metadata
    - decision: str, must be one of "approve", "edit", or "reject"
    - reviewer_note: str, context or reasoning provided by the reviewer
    
    Returns:
    - dict containing the status, downstream release clearance, and unique audit reference.
    """
    allowed_decisions = {"approve", "edit", "reject"}
    if decision not in allowed_decisions:
        raise ValueError(f"Invalid decision '{decision}'. Must be one of {allowed_decisions}.")
        
    # Generate run/audit metadata
    run_id = str(uuid.uuid4())
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    region = report.get("region", "Unknown")
    
    # Map decision to downstream clearance allowance
    release_allowed = (decision == "approve")
    
    result = {
        "run_id": run_id,
        "timestamp": timestamp,
        "region": region,
        "decision": decision,
        "reviewer_note": reviewer_note,
        "release_allowed": release_allowed
    }
    
    # Write record to audit_log.jsonl
    audit_line = {
        "timestamp": timestamp,
        "run_id": run_id,
        "region": region,
        "decision": decision,
        "reviewer_note": reviewer_note
    }
    
    with open("audit_log.jsonl", "a") as f:
        f.write(json.dumps(audit_line) + "\n")
        
    return result

# --- Test Harness ---
def test_review_gate_harness():
    # Clear any previous audit log to keep testing fresh
    import os
    if os.path.exists("audit_log.jsonl"):
        os.remove("audit_log.jsonl")

    sample_report = {
        "region": "Guntur",
        "report_type": "Regional Growth Memo",
        "period": "April-May 2026"
    }
    
    test_cases = [
        ("approve", "Guntur metrics are verified against SQL output; release approved."),
        ("edit", "Needs additional proofreading on formatting before final release."),
        ("reject", "Major factual inconsistency with region name; rejection enforced.")
    ]
    
    print("=== EXERCISING ALL 3 DECISION PATHS ===\n")
    for idx, (decision, note) in enumerate(test_cases, 1):
        print(f"--- Test Case {idx}: Decision = '{decision}' ---")
        print(f"Before Gate Call: Report Region = '{sample_report['region']}'")
        
        gate_output = review_gate_v1(sample_report, decision, reviewer_note=note)
        
        print("After Gate Output:")
        print(json.dumps(gate_output, indent=2))
        print("-" * 50 + "\n")
        
    print("=== VERIFYING AUDIT LOG FILE ENTRIES ===")
    with open("audit_log.jsonl", "r") as f:
        for line in f:
            print(line.strip())

test_review_gate_harness()


"""
=== EXERCISING ALL 3 DECISION PATHS ===

--- Test Case 1: Decision = 'approve' ---
Before Gate Call: Report Region = 'Guntur'
After Gate Output:
{
  "run_id": "3fb21d3e-39f9-4707-a91a-a8614e7340a0",
  "timestamp": "2026-09-25 20:28:45",
  "region": "Guntur",
  "decision": "approve",
  "reviewer_note": "Guntur metrics are verified against SQL output; release approved.",
  "release_allowed": true
}
--------------------------------------------------

--- Test Case 2: Decision = 'edit' ---
Before Gate Call: Report Region = 'Guntur'
After Gate Output:
{
  "run_id": "dc79ed82-9ad8-4145-a617-c3cc1dae7834",
  "timestamp": "2026-09-25 20:28:45",
  "region": "Guntur",
  "decision": "edit",
  "reviewer_note": "Needs additional proofreading on formatting before final release.",
  "release_allowed": false
}
--------------------------------------------------

--- Test Case 3: Decision = 'reject' ---
Before Gate Call: Report Region = 'Guntur'
After Gate Output:
{
  "run_id": "896699bb-9557-4762-9577-a666f1072005",
  "timestamp": "2026-09-25 20:28:45",
  "region": "Guntur",
  "decision": "reject",
  "reviewer_note": "Major factual inconsistency with region name; rejection enforced.",
  "release_allowed": false
}
--------------------------------------------------
"""