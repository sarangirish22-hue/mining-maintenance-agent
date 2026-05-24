from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from agents.diagnosis_agent import run_diagnosis_agent
from agents.inventory_agent import run_inventory_agent
from agents.oem_agent import run_oem_agent
from agents.jobcard_agent import run_jobcard_agent

# State definition
class MiningAgentState(TypedDict):
    truck_id: str
    truck_model: str
    fault_description: str
    fault_type: str
    severity: str
    required_parts: List[str]
    recommended_action: str
    available_parts: List[str]
    unavailable_parts: List[str]
    inventory_status: str
    validated_parts: List[str]
    rejected_parts: List[str]
    warranty_status: str
    oem_recommendation: str
    job_card_id: str
    work_instructions: str
    estimated_time: str
    priority: str
    status: str

# Node functions
def diagnosis_node(state: MiningAgentState) -> MiningAgentState:
    print("🔍 Running Diagnosis Agent...")
    result = run_diagnosis_agent(
        truck_id=state["truck_id"],
        fault_description=state["fault_description"]
    )
    return {
        **state,
        "fault_type": result.fault_type,
        "severity": result.severity,
        "required_parts": result.required_parts,
        "recommended_action": result.recommended_action
    }

def inventory_node(state: MiningAgentState) -> MiningAgentState:
    print("📦 Running Inventory Agent...")
    result = run_inventory_agent(
        required_parts=state["required_parts"]
    )
    return {
        **state,
        "available_parts": result.available_parts,
        "unavailable_parts": result.unavailable_parts,
        "inventory_status": result.inventory_status
    }

def oem_node(state: MiningAgentState) -> MiningAgentState:
    print("🔧 Running OEM Validation Agent...")
    result = run_oem_agent(
        available_parts=state["available_parts"],
        truck_model=state["truck_model"]
    )
    return {
        **state,
        "validated_parts": result.validated_parts,
        "rejected_parts": result.rejected_parts,
        "warranty_status": result.warranty_status,
        "oem_recommendation": result.oem_recommendation
    }

def jobcard_node(state: MiningAgentState) -> MiningAgentState:
    print("📋 Running Job Card Agent...")
    result = run_jobcard_agent(
        truck_id=state["truck_id"],
        fault_type=state["fault_type"],
        severity=state["severity"],
        validated_parts=state["validated_parts"],
        recommended_action=state["recommended_action"]
    )
    return {
        **state,
        "job_card_id": result.job_card_id,
        "work_instructions": result.work_instructions,
        "estimated_time": result.estimated_time,
        "priority": result.priority,
        "status": result.status
    }

# Build LangGraph pipeline
def build_pipeline():
    workflow = StateGraph(MiningAgentState)
    
    workflow.add_node("diagnosis", diagnosis_node)
    workflow.add_node("inventory", inventory_node)
    workflow.add_node("oem_validation", oem_node)
    workflow.add_node("job_card", jobcard_node)
    
    workflow.set_entry_point("diagnosis")
    workflow.add_edge("diagnosis", "inventory")
    workflow.add_edge("inventory", "oem_validation")
    workflow.add_edge("oem_validation", "job_card")
    workflow.add_edge("job_card", END)
    
    return workflow.compile()

def run_pipeline(truck_id: str, truck_model: str, fault_description: str):
    pipeline = build_pipeline()
    
    initial_state = MiningAgentState(
        truck_id=truck_id,
        truck_model=truck_model,
        fault_description=fault_description,
        fault_type="",
        severity="",
        required_parts=[],
        recommended_action="",
        available_parts=[],
        unavailable_parts=[],
        inventory_status="",
        validated_parts=[],
        rejected_parts=[],
        warranty_status="",
        oem_recommendation="",
        job_card_id="",
        work_instructions="",
        estimated_time="",
        priority="",
        status=""
    )
    
    result = pipeline.invoke(initial_state)
    return result
