from agents.inventory_agent import run_inventory_agent

result = run_inventory_agent(
    required_parts=["Cylinder Head Gasket", "Engine Oil Cooler", "Engine Filter"]
)

print("=== INVENTORY AGENT RESULT ===")
print(f"Available Parts: {result.available_parts}")
print(f"Unavailable Parts: {result.unavailable_parts}")
print(f"Status: {result.inventory_status}")
