from agents.diagnosis_agent import run_diagnosis_agent

result = run_diagnosis_agent(
    truck_id="CAT-793-001",
    fault_description="Truck is making loud knocking noise from engine, black smoke from exhaust, loss of power on uphill gradient"
)

print("=== DIAGNOSIS AGENT RESULT ===")
print(f"Fault Type: {result.fault_type}")
print(f"Severity: {result.severity}")
print(f"Required Parts: {result.required_parts}")
print(f"Recommended Action: {result.recommended_action}")
