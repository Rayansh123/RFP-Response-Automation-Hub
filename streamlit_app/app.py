# streamlit_app/app.py

import streamlit as st
import pandas as pd
import json
# Import the core client from the root of the package (where it is currently located)
from ibm_watsonx_orchestrate import OrchestrateClient 
# The credentials structure is often a separate import path
from ibm_watsonx_orchestrate.common.credentials import IBMCloudCredentials
from ibm_watsonx_orchestrate.common.credentials import IBMCloudCredentials
from typing import Dict, List

# --- CONFIGURATION (REPLACE WITH YOUR ACTUAL CREDENTIALS) ---
# NOTE: Replace these with your live, working credentials
ORCHESTRATE_URL = " https://api.eu-gb.watson-orchestrate.cloud.ibm.com/instances/05bcb974-d752-46b1-b6f2-1895c62a6d6f" 
ORCHESTRATE_API_KEY = "306zrjlubZImaSopBFBS7n-ghvl_dvROPPToIWAhlLyq"
ORCHESTRATE_AGENT_ID = "0b8c9111-c128-43f9-84b9-0e2a41fb8278" 

# --- DATA PROCESSING UTILITIES ---

def load_data_and_convert_to_json(uploaded_file):
    """Reads CSV content and converts it into a clean JSON string."""
    if uploaded_file is None:
        return None
    try:
        df = pd.read_csv(uploaded_file)
        df = df.fillna('')
        # Use records format for safe LLM parsing
        return df.to_json(orient='records')
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

def create_orchestrate_client():
    """Initializes the Orchestrate Client using IAM API Key."""
    try:
        credentials = IBMCloudCredentials(api_key=ORCHESTRATE_API_KEY)
        client = OrchestrateClient(
            service_url=ORCHESTRATE_URL,
            credentials=credentials
        )
        return client
    except Exception as e:
        st.error(f"Failed to initialize Orchestrate Client. Check API Key and URL.")
        st.exception(e)
        return None

# --- STREAMLIT FRONTEND ---

st.set_page_config(page_title="RFP Automation Hub MVP", layout="wide")
st.title("🔌 RFP Automation Hub MVP: The Bid Coordinator")
st.markdown("---")

st.info(f"Current time in Manipal, India is **{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**. Ready for deployment!")

# --- 1. File Upload Section ---
st.header("1. Upload Catalog Data (CSV Files)")

col1, col2 = st.columns(2)

with col1:
    product_file = st.file_uploader("Upload Product Catalog (Product_Specs.csv)", type=['csv'])
with col2:
    test_costs_file = st.file_uploader("Upload Test Costs (Test_Costs_DB.csv)", type=['csv'])

# --- 2. RFP Specification Input (Multi-Product) ---
st.header("2. Define Bid Requirements")
st.markdown("Define the specifications for **two** materials required in the RFP.")

col3, col4 = st.columns(2)

# Material 1 Inputs (High-Value Cable)
with col3:
    st.subheader("Material 1: Power Cable")
    m1_voltage = st.number_input("Voltage (V) - M1", value=1100, step=100)
    m1_insulation = st.selectbox("Insulation - M1", ["XLPE", "PVC", "HDPE"], index=0)
    m1_quantity = st.number_input("Quantity (Meters) - M1", min_value=1000, value=5000, step=500)
    m1_tests = st.multiselect("Tests - M1", ["High Voltage (HV) Test", "Short Circuit Test"], default=["High Voltage (HV) Test"])

# Material 2 Inputs (Control Cable)
with col4:
    st.subheader("Material 2: Control Cable")
    m2_voltage = st.number_input("Voltage (V) - M2", value=450, step=100)
    m2_insulation = st.selectbox("Insulation - M2", ["PVC", "XLPE", "HDPE"], index=0)
    m2_quantity = st.number_input("Quantity (Meters) - M2", min_value=100, value=2500, step=100)
    m2_tests = st.multiselect("Tests - M2", ["Documentation_Fee", "Freight_Handling"], default=["Documentation_Fee"])


# --- 3. RUN BUTTON ---
if st.button("Generate Final Bid Proposal", type="primary"):
    
    # 3.1. Convert uploaded files to JSON strings
    product_json_str = load_data_and_convert_to_json(product_file)
    test_costs_json_str = load_data_and_convert_to_json(test_costs_file)

    if product_json_str is None or test_costs_json_str is None:
        st.error("Please upload both Product Catalog and Test Costs CSV files before proceeding.")
    else:
        # 3.2. Construct the Core Prompt with ALL data
        # We send the two different product specs and the combined test requirements
        user_prompt = (
            f"Generate a complete RFP bid proposal based on the following combined requirements: "
            f"MATERIAL 1: {m1_quantity}m of {m1_voltage}V {m1_insulation} cable, requiring tests: {m1_tests}. "
            f"MATERIAL 2: {m2_quantity}m of {m2_voltage}V {m2_insulation} cable, requiring tests: {m2_tests}. "
            f"Your response must be a professional summary, including the final total bid price."
        )

        # The Orchestrator's instructions will pull the data from the prompt and the RAG (as confirmed)
        st.success("Files processed successfully. Initiating multi-agent workflow...")
        
        # --- Execute Orchestration ---
        client = create_orchestrate_client()
        
        if client:
            with st.spinner("Delegating tasks to Agents: Technical Analysis and Proposal Drafting..."):
                try:
                    # Call the Main Orchestrator Agent
                    response = client.agents.chat(
                        agent_id=ORCHESTRATE_AGENT_ID,
                        message=user_prompt
                    )
                    
                    proposal_text = response.text
                    
                    st.subheader("✅ Final Proposal Report")
                    st.markdown(proposal_text)
                    st.balloons()
                        
                except Exception as e:
                    st.error(f"Orchestration Error: The workflow failed to complete.")
                    st.exception(e)

st.markdown("---")
st.markdown("### Deployment Note")
st.markdown("Replace the placeholder credentials and the Main Orchestrator Agent ID in the `app.py` script before pushing to GitHub/Streamlit Cloud.")