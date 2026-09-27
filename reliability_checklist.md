checklist_content = """# Reliability Checklist: Regional Pulse Memo

## 1. Safety Check
No personally identifiable customer information, patient records, or transaction-level sensitive details appear in the memo or narrative—only safe, high-level regional aggregates are displayed.

## 2. Validation
Every numerical sales value, metric, growth percentage, and chronological period cited in the memo matches the raw and aggregated data outputs of our validated SQLite database and Pandas computations exactly.

## 3. Critique/Refine
The business narrative and key insights have been rigorously audited to ensure a clear boundary between mathematically derived facts and operational hypotheses (such as localized marketing or supply shifts), which are properly routed to the Assumptions section.

## 4. Human Sign-off
The finalized document structure and its inline risk tags ([LOW] / [MEDIUM] / [HIGH]) have been manually verified and approved by the reviewer to ensure it meets our strict organizational standards for analytical transparency.
"""

with open('reliability_checklist.md', 'w') as f:
    f.write(checklist_content)

print("Saved reliability_checklist.md successfully!")
