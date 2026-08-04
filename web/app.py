import sys
import os
import json
import traceback
import streamlit as st

# Garante que a raiz do projeto esteja no path para importar iron_ledger
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the custom WebLLM component
from components.webllm import webllm_generate

# Import Iron Ledger core
from iron_ledger.api.client import HevyClient
from iron_ledger.importer.importer import ProgramImporter

st.set_page_config(page_title="Iron Ledger Web", page_icon="🏋️", layout="centered")

st.title("🏋️ Iron Ledger AI")
st.markdown("*Every set. Every rep. Accounted for. — Powered by local WebLLM.*")

# Initialize session state for API Key
if "hevy_api_key" not in st.session_state:
    st.session_state.hevy_api_key = ""

# API Key input (saved only in session state)
api_key = st.text_input(
    "Hevy API Key", 
    value=st.session_state.hevy_api_key, 
    type="password",
    help="Your API key is only stored in your browser's current session. It is never saved to a server."
)
if api_key:
    st.session_state.hevy_api_key = api_key

st.divider()

st.subheader("1. Describe your workout")
st.markdown("Paste your natural language workout below. The local WebLLM will structure it into JSON.")

default_prompt = """ROTINA DE TREINAMENTO: PERIODIZAÇÃO AB (2 DIAS)

TREINO A:
1. Bench Press (Barbell) - 4 sets of 8 reps (60kg)
2. Bent Over Row (Barbell) - 4 sets of 8 reps (50kg)
3. Squat (Barbell) - 4 sets of 6 reps (80kg)"""

workout_text = st.text_area("Natural Language Workout", value=default_prompt, height=200)

if "llm_result" not in st.session_state:
    st.session_state.llm_result = None

if "prompt_to_send" not in st.session_state:
    st.session_state.prompt_to_send = None

col1, col2 = st.columns([1, 3])
with col1:
    if st.button("Generate JSON"):
        st.session_state.prompt_to_send = workout_text
        st.session_state.llm_result = None # Clear previous result

with col2:
    # Run the component (it will mount and wait, or process if prompt is set)
    webllm_status = webllm_generate(prompt=st.session_state.prompt_to_send, key="webllm_instance")
    
    if webllm_status:
        if webllm_status.get("status") == "success":
            st.success("WebLLM generated the structured workout!")
            # Save the result so it persists across Streamlit reruns
            if st.session_state.prompt_to_send:
                st.session_state.llm_result = webllm_status.get("text")
                st.session_state.prompt_to_send = None # Reset so we don't trigger again
                st.rerun()
        elif webllm_status.get("status") == "error":
            st.error(f"WebLLM Error: {webllm_status.get('error')}")

st.divider()

st.subheader("2. Review & Upload")

if st.session_state.llm_result:
    try:
        # Try to parse the JSON returned by the LLM
        parsed_json = json.loads(st.session_state.llm_result)
        
        # Allow user to edit the JSON directly in the browser
        edited_json_str = st.text_area("Review and edit the structured JSON before uploading:", value=json.dumps(parsed_json, indent=2), height=300)
        
        if st.button("Upload to Hevy", type="primary"):
            if not st.session_state.hevy_api_key:
                st.error("Please enter your Hevy API Key at the top of the page.")
            else:
                try:
                    final_json = json.loads(edited_json_str)
                    
                    with st.spinner("Connecting to Hevy API..."):
                        # Initialize Iron Ledger SDK
                        client = HevyClient(api_key=st.session_state.hevy_api_key)
                        importer = ProgramImporter(client)
                        
                        # Upload using the importer logic
                        folder_name = final_json.get("name", "Imported Workout")
                        # Emulate the dict structure expected by the importer
                        # importer.import_program takes a dict matching PROGRAM structure
                        importer.import_program(final_json, folder_name=folder_name)
                    
                    st.success(f"Successfully uploaded '{folder_name}' to Hevy!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Upload failed: {str(e)}")
                    st.code(traceback.format_exc())
                    
    except json.JSONDecodeError:
        st.error("WebLLM returned invalid JSON. Please try generating again.")
        st.code(st.session_state.llm_result)
else:
    st.info("Awaiting generated workout...")

