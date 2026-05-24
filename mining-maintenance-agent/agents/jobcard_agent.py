from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class JobCardOutput(BaseModel):
    job_card_id: str
    truck_id: str
    fault_type: str
    severity: str
    validated_parts: List[str]
    work_instructions: str
    estimated_time: str
    priority: str
    status: str

def run_jobcard_agent(
    truck_id: str,
    fault_type: str,
    severity: str,
    validated_parts: List[str],
    recommended_action: str
) -> JobCardOutput:
    
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    system_prompt = """You are a workshop job card generator for mining equipment.
    Generate a detailed job card for the workshop technician.
    Return EXACTLY in this format with no extra lines:
    WORK_INSTRUCTIONS: <detailed step by step instructions in one line>
    ESTIMATED_TIME: <time in hours>
    PRIORITY: <Immediate/High/Medium/Low>
    STATUS: Open"""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""
Truck ID: {truck_id}
Fault Type: {fault_type}
Severity: {severity}
Validated Parts Available: {validated_parts}
Recommended Action: {recommended_action}
Generate workshop job card.
        """)
    ]
    
    response = llm.invoke(messages)
    content = response.content
    lines = content.strip().split('\n')
    
    estimated_time = ""
    priority = ""
    status = "Open"
    work_instructions = ""
    
    for line in lines:
        if line.startswith("WORK_INSTRUCTIONS:"):
            work_instructions = line.split(":", 1)[1].strip()
        elif line.startswith("ESTIMATED_TIME:"):
            estimated_time = line.split(":", 1)[1].strip()
        elif line.startswith("PRIORITY:"):
            priority = line.split(":", 1)[1].strip()
        elif line.startswith("STATUS:"):
            status = line.split(":", 1)[1].strip()
    
    job_card_id = f"JC-{truck_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return JobCardOutput(
        job_card_id=job_card_id,
        truck_id=truck_id,
        fault_type=fault_type,
        severity=severity,
        validated_parts=validated_parts,
        work_instructions=work_instructions,
        estimated_time=estimated_time,
        priority=priority,
        status=status
    )
