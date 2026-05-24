import json
import os
from pydantic import BaseModel
from typing import List

class InventoryCheckOutput(BaseModel):
    available_parts: List[str]
    unavailable_parts: List[str]
    inventory_status: str

def run_inventory_agent(required_parts: List[str]) -> InventoryCheckOutput:
    with open("data/inventory.json", "r") as f:
        inventory = json.load(f)
    
    available_parts = []
    unavailable_parts = []
    
    for required_part in required_parts:
        found = False
        for item in inventory["parts"]:
            if any(word.lower() in item["name"].lower() 
                   for word in required_part.split()):
                if item["quantity"] > 0:
                    available_parts.append(f"{item['name']} (Qty: {item['quantity']})")
                else:
                    unavailable_parts.append(f"{item['name']} (OUT OF STOCK)")
                found = True
                break
        if not found:
            unavailable_parts.append(f"{required_part} (NOT IN INVENTORY)")
    
    if not unavailable_parts:
        status = "ALL PARTS AVAILABLE - Ready for repair"
    elif not available_parts:
        status = "NO PARTS AVAILABLE - Procurement needed"
    else:
        status = "PARTIAL AVAILABILITY - Some parts need procurement"
    
    return InventoryCheckOutput(
        available_parts=available_parts,
        unavailable_parts=unavailable_parts,
        inventory_status=status
    )
