import streamlit as st
import pandas as pd
from datetime import datetime

# --- MOCK DATA (Simulates the Output of the Technical Agent) ---

# This JSON structure proves the Technical Agent successfully ran the logic
MOCK_CALCULATION_RESULT = {
    "final_status": "SUCCESS",
    "best_sku": "P-1100-XL",
    "match_percentage": 100.0,
    "material_cost": 75000.00,
    "total_test_cost": 16500.00,
    "final_bid_price": 91500.00,
    "required_tests": ["High Voltage (HV) Test", "Short Circuit Test"],
    "required_specs": {"voltage": "1100V", "insulation": "XLPE", "quantity": 5000}
}

# This is the expected narrative output from the Finalization Agent (LLM)
MOCK_FINAL_PROPOSAL = f"""
## Executive Summary and Technical Fit

We are pleased to submit our final proposal for the supply of required materials. The automated **Technical Agent** has confirmed that our product, **SKU P-1100-XL**, achieves a **100% technical match** against the core requirements of your tender. Our solution meets all minimum specifications for voltage, insulation, and quantity, significantly de-risking your procurement process.

## Detailed Bid Breakdown

The proposed total price is derived from the material supply and mandatory acceptance testing costs required for compliance in this sector. The final calculated figure is **${MOCK_CALCULATION_RESULT['final_bid_price']:,.2f}**.

**This bid is optimized for compliance and total lifecycle value.**

## Mandatory Audit Table (Structured Data)

| Requirement | Best SKU (P-1100-XL) | Match Status |
| :--- | :--- | :--- |
| **Voltage Rating (1100V)** | 1100V | ✅ Match |
| **Insulation Type (XLPE)** | XLPE | ✅ Match |
| **Required Quantity (5000m)** | 5000m | ✅ Matched |
| **Technical Match Score** | **{MOCK_CALCULATION_RESULT['match_percentage']}%** | **MAXIMUM** |

### Financial Summary

| Cost Component | Total Price (USD) |
| :--- | :--- |
| Material Cost (5000m @ $15.00/m) | ${MOCK_CALCULATION_RESULT['material_cost']:,.2f} |
| Acceptance Testing (HV + SC Tests) | ${MOCK_CALCULATION_RESULT['total_test_cost']:,.2f} |
| **TOTAL FINAL BID PRICE** | **${MOCK_CALCULATION_RESULT['final_bid_price']:,.2f}** |
"""

# --- STREAMLIT FRONTEND ---

st.set_page_config(page_title="RFP Automation Hub (Static Demo)", layout="wide")
st.title("🔌 RFP Response Automation Hub (Prototype Demo)")
st.markdown("---")

st.markdown("""
### Project Goal: Automating the B2B Tender Bottleneck

This prototype demonstrates a multi-agent system built on **IBM watsonx Orchestrate** that automates the time-consuming process of technical bid creation for high-value contracts.

**The value:** Transforming a slow, error-prone manual handoff between Sales and Engineering teams into a seamless, automated workflow.
""")

# --- AGENT ORCHESTRATION FLOW CHART ---
st.header("1. Multi-Agent Workflow Delegation ")
st.code("""
USER INPUT (RFP Specs)
      ↓ (Delegate)
MAIN ORCHESTRATOR AGENT (Supervisor)
      ↓ (Calls)
SALES AGENT (Data Parser) -> Retrieves data from RAG/KB and formats as JSON.
      ↓ (Passes JSON)
TECHNICAL AGENT (Custom ADK Tool) -> Executes Spec Match Algorithm & Pricing.
      ↓ (Passes Structured Results)
FINALIZATION AGENT (LLM Drafter) -> Generates proposal narrative & audit table.
      ↓ (Final Output)
USER (Professional Bid Document)
""", language="markdown")
st.markdown("---")


# --- SIMULATED INPUT SECTION ---
st.header("2. Simulated Input: RFP Requirements")

st.markdown("*(Inputs are simulated to immediately trigger the successful workflow logic)*")

col1, col2 = st.columns(2)

with col1:
    st.info("Material 1 Specs (Triggering 100% Match)")
    st.text_input("Required Voltage (V)", value="1100 V", disabled=True)
    st.text_input("Required Insulation", value="XLPE", disabled=True)
    st.number_input("Required Quantity (Meters)", value=5000, disabled=True)
with col2:
    st.warning("Data Source Files")
    st.text_input("Product Catalog Source", value="Product_Specs.csv (RAG Knowledge)", disabled=True)
    st.text_input("Test Cost Catalog Source", value="Test_Costs_DB.csv (RAG Knowledge)", disabled=True)

# --- RUN SIMULATION BUTTON ---
if st.button("RUN SIMULATION (Show Final Output)", type="primary"):
    st.markdown("---")
    st.subheader("Simulating Orchestration Steps...")
    
    with st.spinner("Processing Data Retrieval, Calculation, and LLM Synthesis..."):
        # Simulated delay to visualize work being done
        import time
        time.sleep(2) 
        
    st.success("✅ **SUCCESS: Orchestration Completed** (Delegate Flow Executed)")
    st.markdown("---")
    
    # --- FINAL OUTPUT DISPLAY ---
    st.header("3. Final Result: Generated Proposal")
    st.markdown(MOCK_FINAL_PROPOSAL)
    st.balloons()

st.markdown("---")
st.markdown(f"*(Prototype demonstrated using multi-agent principles in IBM watsonx Orchestrate. Time Simulated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})*")