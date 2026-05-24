from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class DiagnosisOutput(BaseModel):
    fault_type: str
    severity: str
    required_parts: List[str]
    recommended_action: str

def run_diagnosis_agent(truck_id: str, fault_description: str) -> DiagnosisOutput:
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    system_prompt = """You are an expert mining equipment diagnostic engineer.
    When given a fault description, analyze it and return EXACTLY in this format:
    FAULT_TYPE: <type>
    SEVERITY: <Critical/High/Medium/Low>
    REQUIRED_PARTS: <part1>, <part2>
    RECOMMENDED_ACTION: <action>"""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Truck ID: {truck_id}\nFault Description: {fault_description}")
    ]
    
    response = llm.invoke(messages)
    content = response.content
    
    lines = content.strip().split('\n')
    fault_type = ""
    severity = ""
    required_parts = []
    recommended_action = ""
    
    for line in lines:
        if line.startswith("FAULT_TYPE:"):
            fault_type = line.split(":", 1)[1].strip()
        elif line.startswith("SEVERITY:"):
            severity = line.split(":", 1)[1].strip()
        elif line.startswith("REQUIRED_PARTS:"):
            parts_str = line.split(":", 1)[1].strip()
            required_parts = [p.strip() for p in parts_str.split(",")]
        elif line.startswith("RECOMMENDED_ACTION:"):
            recommended_action = line.split(":", 1)[1].strip()
    
    return DiagnosisOutput(
        fault_type=fault_type,
        severity=severity,
        required_parts=required_parts,
        recommended_action=recommended_action
    )
