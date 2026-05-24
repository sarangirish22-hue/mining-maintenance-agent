import json
from pydantic import BaseModel
from typing import List
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()

class OEMValidationOutput(BaseModel):
    validated_parts: List[str]
    rejected_parts: List[str]
    warranty_status: str
    oem_recommendation: str

def run_oem_agent(available_parts: List[str], truck_model: str) -> OEMValidationOutput:
    with open("data/oem_specs.json", "r") as f:
        oem_specs = json.load(f)
    
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    oem_context = json.dumps(oem_specs, indent=2)
    
    system_prompt = """You are an OEM warranty validation specialist for mining equipment.
    Given available parts and OEM specifications, validate if parts are warranty compliant.
    Return EXACTLY in this format:
    VALIDATED_PARTS: <part1>, <part2>
    REJECTED_PARTS: <part1>, <part2>
    WARRANTY_STATUS: <Valid/Invalid/Partial>
    OEM_RECOMMENDATION: <recommendation>"""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""
Truck Model: {truck_model}
Available Parts: {available_parts}
OEM Specifications: {oem_context}
Validate these parts for OEM warranty compliance.
        """)
    ]
    
    response = llm.invoke(messages)
    content = response.content
    
    lines = content.strip().split('\n')
    validated_parts = []
    rejected_parts = []
    warranty_status = ""
    oem_recommendation = ""
    
    for line in lines:
        if line.startswith("VALIDATED_PARTS:"):
            parts_str = line.split(":", 1)[1].strip()
            validated_parts = [p.strip() for p in parts_str.split(",")]
        elif line.startswith("REJECTED_PARTS:"):
            parts_str = line.split(":", 1)[1].strip()
            rejected_parts = [p.strip() for p in parts_str.split(",")]
        elif line.startswith("WARRANTY_STATUS:"):
            warranty_status = line.split(":", 1)[1].strip()
        elif line.startswith("OEM_RECOMMENDATION:"):
            oem_recommendation = line.split(":", 1)[1].strip()
    
    return OEMValidationOutput(
        validated_parts=validated_parts,
        rejected_parts=rejected_parts,
        warranty_status=warranty_status,
        oem_recommendation=oem_recommendation
    )
