from agents.oem_agent import run_oem_agent

result = run_oem_agent(
    available_parts=["Engine Filter (Qty: 5)"],
    truck_model="CAT 793"
)

print("=== OEM VALIDATION AGENT RESULT ===")
print(f"Validated Parts: {result.validated_parts}")
print(f"Rejected Parts: {result.rejected_parts}")
print(f"Warranty Status: {result.warranty_status}")
print(f"OEM Recommendation: {result.oem_recommendation}")
