from agents.jobcard_agent import run_jobcard_agent

result = run_jobcard_agent(
    truck_id="CAT-793-001",
    fault_type="Engine Mechanical Failure",
    severity="Critical",
    validated_parts=["Engine Filter (Qty: 5)"],
    recommended_action="Immediately shut down engine and replace faulty parts"
)

print("=== JOB CARD AGENT RESULT ===")
print(f"Job Card ID: {result.job_card_id}")
print(f"Truck ID: {result.truck_id}")
print(f"Fault Type: {result.fault_type}")
print(f"Severity: {result.severity}")
print(f"Validated Parts: {result.validated_parts}")
print(f"Work Instructions: {result.work_instructions}")
print(f"Estimated Time: {result.estimated_time}")
print(f"Priority: {result.priority}")
print(f"Status: {result.status}")
