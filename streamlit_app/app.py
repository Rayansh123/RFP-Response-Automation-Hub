import streamlit as st
import time
from datetime import datetime
from typing import Dict

# --- MOCK DATA (Pre-Calculated Results) ---
# This data simulates the FINAL output received from the Technical Agent.
MOCK_CALCULATION_RESULT = {
    "best_sku": "P-1100-XL",
    "match_percentage": 100.0,
    "material_cost": 75000.00,
    "total_test_cost": 12500.00, 
    "final_bid_price": 87500.00,
    "required_tests": ["High Voltage (HV) Test", "Short Circuit Test"],
}

# --- MOCK PROPOSAL TEXT (Narrative Output from Finalization Agent) ---
MOCK_PROPOSAL_TEXT = f"""
Dear Customer Name,

We are pleased to submit our proposal in response to your Request for Proposal (RFP). Our multi-agent system has confirmed that our solution meets your needs.

### Executive Summary
Our automated analysis has determined that our proposed product achieves a **{MOCK_CALCULATION_RESULT['match_percentage']}% technical match** with your specifications. The entire bid was processed instantly by our multi-agent system, confirming compliance, calculating precise costs, and generating this executive summary for immediate review.

### Technical Details & Solution
We propose the following product to meet your requirements:
- **Product ID:** **{MOCK_CALCULATION_RESULT['best_sku']}** (The highest-scoring SKU)
- **Voltage Rating:** 1100 V
- **Insulation Type:** XLPE
- **Required Tests:** High Voltage (HV) Test and Short Circuit Test

### Financial Audit Table
| Cost Component | Total Price (USD) |
| :--- | :--- |
| **Best SKU** | {MOCK_CALCULATION_RESULT['best_sku']} |
| **Material Cost (5000m)** | **${MOCK_CALCULATION_RESULT['material_cost']:,.2f}** |
| **Total Test Cost** | **${MOCK_CALCULATION_RESULT['total_test_cost']:,.2f}** |
| **TOTAL FINAL BID PRICE** | **${MOCK_CALCULATION_RESULT['final_bid_price']:,.2f}** |

### Conclusion
We believe that our proposal offers the best solution to meet your requirements. We look forward to the opportunity to work with you.
Sincerely,
[Your Name] | [Your Company]
"""

# --- STREAMLIT FRONTEND ---

st.set_page_config(page_title="RFP Automation Hub", layout="wide")
st.title("🤖 RFP Response Automation Hub")
st.markdown("---")

# --- Tabs for Interface and Explanation ---
tab1, tab2 = st.tabs(["💬 Conversational Demo", "🛠️ Project Overview"])

with tab1:
    # --- CONVERSATIONAL DEMO ---
    
    st.subheader("Simulated Agent Interaction")
    st.caption("Select a prompt to initiate the multi-agent workflow and showcase contextual Q&A (RAG).")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state["messages"].append({"role": "assistant", "content": "Welcome! I am the **RFP Automation Hub**. I can instantly analyze your technical requirements and generate a professional bid proposal."})

    # --- Suggested Prompts (The RAG Test Cases) ---
    starter_prompts = {
        "Generate Full Bid": "Generate a complete RFP bid response for a product that requires a 1100 Volt Rating and XLPE Insulation, including the final calculated bid price and match score.",
        "Check Max Load (RAG Test)": "What is the maximum connected load allowed on a single lighting circuit as per the reference documents?",
        "Check Conductor Color": "As per the general specifications, what color must the protective earth conductor be?",
    }

    # Add buttons for suggested prompts (displayed horizontally)
    cols = st.columns(3)
    for i, (key, prompt) in enumerate(starter_prompts.items()):
        with cols[i]:
            if st.button(key, key=f"btn_{i}"):
                st.session_state.current_prompt = prompt
                
    # --- Chat Display ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- Chat Input Logic ---
    prompt_input = st.session_state.get('current_prompt', "")
    if prompt_input:
        # Clear the temporary prompt
        if 'current_prompt' in st.session_state:
            del st.session_state.current_prompt
        
        # Process the prompt
        with st.chat_message("user"):
            st.markdown(prompt_input)
        st.session_state.messages.append({"role": "user", "content": prompt_input})
        
        # --- MOCKED RESPONSE GENERATION ---
        
        # Simulate agent processing time
        with st.spinner("Delegating task to Agents: Technical Analysis and Proposal Drafting..."):
            time.sleep(3) # Simulate API latency and agent processing

        # Decide which mocked response to send
        if "Generate Full Bid" in prompt_input:
            response_text = MOCK_PROPOSAL_TEXT
        elif "lighting circuit" in prompt_input:
            # RAG/Contextual Answer (from Page 37)
            response_text = "As per the General Specifications (RFP Document Clause 3.10(i) of the uploaded document), each lighting circuit shall not have more than **800 Watt** connected load or more than **10 points**, whichever is less."
        elif "earth conductor" in prompt_input:
            # RAG/Contextual Answer (from Page 36)
            response_text = "The protective earth conductor must be colored **Yellow/Green** (RFP Document Clause 3.5(v))."
        else:
            response_text = "I'm sorry, I could not complete that workflow. I can only perform bid generation or answer questions about the documentation."

        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.rerun() # Rerun to update chat history

    # Display an empty input box if no prompt is loaded
    if 'current_prompt' not in st.session_state:
        st.text_input("Ask the Main Orchestrator Agent...", key="chat_input")

with tab2:
    # --- PROJECT OVERVIEW (For Judging) ---
    
    st.header("1. Problem & Business Value")
    st.markdown("""
    The core challenge in B2B tendering (e.g., industrial, high-spec components) is the **slow, manual handoff** between **Sales, Technical, and Pricing** teams. This sequential workflow leads to delays, errors, and lost contracts.
    """)
    st.info("Goal: To automate this cross-functional bid process and reduce submission time from days to minutes.")

    st.header("2. Multi-Agent System Architecture")
    st.markdown("""
    Our solution is built on **IBM watsonx Orchestrate**, utilizing **hierarchical delegation** to manage the workflow. This structure proves the system's ability to handle complex, multi-step tasks.
    """)
    
    st.code("""
USER (Natural Language Request)
      ↓ (Intent Delegation)
MAIN ORCHESTRATOR AGENT (Supervisor, RAG-Enabled)
      ↓ (Flow Control)
SALES AGENT (Data Retrieval & Parsing)
      ↓ (Output: Structured JSON)
TECHNICAL AGENT (Custom ADK Algorithm)
      ↓ (Output: Calculated Price/Score JSON)
FINALIZATION AGENT (LLM Drafter)
      ↓ (Final Output)
PROFESSIONAL PROPOSAL (Narrative + Audit Table)
""")

    st.header("3. Technical Achievements")
    st.markdown("""
    * **Custom Technical IP:** The **Technical Agent** executes a proprietary, weighted Spec Match Algorithm (built using **Python ADK**), providing a precise, auditable Technical Fit Score (%).
    * **Cognitive Orchestration:** The Main Agent manages the flow and uses its **Knowledge Base (RAG)** to answer contextual questions about the uploaded RFP documents, showcasing intelligence beyond simple execution.
    * **Structured Reporting:** The system reliably transforms messy inputs into a final report that includes both **narrative explanation** and a **structured financial audit table**.
    """)
    st.markdown("---")
    st.caption(f"Developed using IBM watsonx Orchestrate. Date: {datetime.now().strftime('%Y-%m-%d')}")