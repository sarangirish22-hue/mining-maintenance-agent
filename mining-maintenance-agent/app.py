import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agents.pipeline import run_pipeline

st.set_page_config(
    page_title="Mining Maintenance Agent",
    page_icon="⛏️",
    layout="wide"
)

st.title("⛏️ Mining Equipment Maintenance Agent")
st.markdown("### AI-Powered Breakdown → Job Card Automation")
st.divider()

col1, col2 = st.columns(2)

with col1:
    truck_model = st.selectbox("🔧 Truck Model", ["CAT 793", "CAT 797", "Komatsu 930E"])
    
    truck_options = {
        "CAT 793": ["CAT-793-001", "CAT-793-002", "CAT-793-003"],
        "CAT 797": ["CAT-797-001", "CAT-797-002"],
        "Komatsu 930E": ["KOM-930E-001", "KOM-930E-002", "KOM-930E-003"]
    }
    truck_id = st.selectbox("🚛 Truck ID", truck_options[truck_model])

with col2:
    fault_description = st.text_area(
        "⚠️ Fault Description",
        placeholder="Describe the fault in detail...",
        height=120
    )

if st.button("🤖 Run Maintenance Agents", type="primary"):
    if fault_description:
        with st.spinner("Running AI Agents..."):
            
            progress = st.progress(0)
            status = st.empty()
            
            status.info("🔍 Agent 1: Diagnosing fault...")
            progress.progress(25)
            
            result = run_pipeline(
                truck_id=truck_id,
                truck_model=truck_model,
                fault_description=fault_description
            )
            
            progress.progress(100)
            status.success("✅ All agents completed!")
            
            st.divider()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Fault Type", result['fault_type'])
            with col2:
                st.metric("Severity", result['severity'])
            with col3:
                st.metric("Warranty", result['warranty_status'])
            with col4:
                st.metric("Priority", result['priority'])
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📦 Inventory Status")
                st.info(result['inventory_status'])
                if result['available_parts']:
                    st.success("✅ Available Parts")
                    for part in result['available_parts']:
                        st.write(f"• {part}")
                if result['unavailable_parts']:
                    st.error("❌ Unavailable Parts")
                    for part in result['unavailable_parts']:
                        st.write(f"• {part}")
            
            with col2:
                st.subheader("🔧 OEM Validation")
                if result['validated_parts']:
                    st.success("✅ Validated Parts")
                    for part in result['validated_parts']:
                        st.write(f"• {part}")
                if result['rejected_parts']:
                    st.error("❌ Rejected Parts")
                    for part in result['rejected_parts']:
                        st.write(f"• {part}")
            
            st.divider()
            
            st.subheader("📋 Generated Job Card")
            
            job_col1, job_col2 = st.columns(2)
            with job_col1:
                st.write(f"**Job Card ID:** {result['job_card_id']}")
                st.write(f"**Truck ID:** {result['truck_id']}")
                st.write(f"**Estimated Time:** {result['estimated_time']} hours")
            with job_col2:
                st.write(f"**Priority:** {result['priority']}")
                st.write(f"**Status:** {result['status']}")
                st.write(f"**Warranty:** {result['warranty_status']}")
            
            st.subheader("🛠️ Work Instructions")
            st.info(result['work_instructions'])
            
    else:
        st.warning("Please enter a fault description!")
