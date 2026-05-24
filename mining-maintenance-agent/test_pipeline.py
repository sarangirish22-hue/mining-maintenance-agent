from agents.pipeline import run_pipeline

result = run_pipeline(
    truck_id="CAT-793-001",
    truck_model="CAT 793",
    fault_description="Truck making loud knocking noise from engine, black smoke from exhaust, loss of power on uphill gradient"
)

print("\n========== FULL PIPELINE RESULT ==========")
print(f"🔍 DIAGNOSIS")
print(f"   Fault Type: {result['fault_type']}")
print(f"   Severity: {result['severity']}")
print(f"   Required Parts: {result['required_parts']}")
print(f"\n📦 INVENTORY")
print(f"   Available: {result['available_parts']}")
print(f"   Unavailable: {result['unavailable_parts']}")
print(f"   Status: {result['inventory_status']}")
print(f"\n🔧 OEM VALIDATION")
print(f"   Validated Parts: {result['validated_parts']}")
print(f"   Warranty Status: {result['warranty_status']}")
print(f"\n📋 JOB CARD")
print(f"   Job Card ID: {result['job_card_id']}")
print(f"   Priority: {result['priority']}")
print(f"   Estimated Time: {result['estimated_time']}")
print(f"   Work Instructions: {result['work_instructions']}")
print(f"   Status: {result['status']}")
print("==========================================")
