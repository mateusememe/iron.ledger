import sys
import os
import re
import json
import traceback
import streamlit as st

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the custom WebLLM component wrapper
from components.webllm import webllm_generate

# Import Iron Ledger core
from iron_ledger.api.client import HevyClient
from iron_ledger.importer.importer import ProgramImporter

st.set_page_config(page_title="Iron Ledger Web", page_icon="🏋️", layout="centered")

def smart_parse_workout(text: str) -> dict:
    """
    Built-in smart parser that extracts workouts, exercises, sets, reps, and weights.
    Acts as a 100% instant fallback for all browsers and environments.
    """
    lines = text.strip().split('\n')
    name = "Imported Workout Program"
    workouts = []
    current_workout = None
    
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
            
        # Program Title
        if line_str.upper().startswith("ROTINA") or line_str.upper().startswith("PROGRAM"):
            name = line_str.replace("ROTINA DE TREINAMENTO:", "").replace("PROGRAM:", "").strip()
            continue
            
        # Workout Day Title
        if line_str.upper().startswith("TREINO") or line_str.upper().startswith("DAY") or line_str.upper().startswith("WORKOUT"):
            current_workout = {
                "title": line_str,
                "notes": "",
                "exercises": []
            }
            workouts.append(current_workout)
            continue
            
        if current_workout is None:
            current_workout = {
                "title": "Treino 1",
                "notes": "",
                "exercises": []
            }
            workouts.append(current_workout)
            
        # Parse set / rep / weight
        sets_count = 3
        reps_count = 10
        weight_kg = 0.0
        
        # Match sets x reps (e.g. 4 x 8, 4x8, 4 sets of 8, 4 séries x 8)
        sr_match = re.search(r'(\d+)\s*(?:x|sets|séries|\*|de)\s*(\d+)', line_str, re.IGNORECASE)
        if sr_match:
            sets_count = int(sr_match.group(1))
            reps_count = int(sr_match.group(2))
            
        # Match weight in kg (e.g. 60kg, 60 kg)
        w_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:kg|kilos|lbs)', line_str, re.IGNORECASE)
        if w_match:
            weight_kg = float(w_match.group(1))
            
        # Extract Exercise Name
        ex_name = None
        # Pattern 1: 1. Bench Press (Barbell) - 4 sets of 8
        ex_match = re.search(r'^(?:\d+[\.\)]\s*)?([A-Za-zÀ-ÿ\s\(\)\-\/\:\,\'\"]+?)(?:[\:\-]\s*|\s+\d+\s*(?:x|sets|séries|\*))', line_str, re.IGNORECASE)
        if ex_match:
            candidate = ex_match.group(1).strip(" :-")
            if len(candidate) > 2 and not candidate.upper().startswith("FOCO") and not candidate.upper().startswith("OBSERVAÇÃO"):
                ex_name = candidate
                
        if ex_name:
            exercise_obj = {
                "name": ex_name,
                "rest_seconds": 90,
                "notes": "",
                "sets": [{"type": "normal", "reps": reps_count, "weight_kg": weight_kg} for _ in range(sets_count)]
            }
            current_workout["exercises"].append(exercise_obj)
            
    if not workouts:
        workouts = [{"title": "Treino 1", "notes": "", "exercises": []}]
        
    return {
        "name": name if name else "Imported Workout Program",
        "workouts": workouts
    }


st.title("🏋️ Iron Ledger AI")
st.markdown("*Every set. Every rep. Accounted for.*")

# Initialize Session State
if "hevy_api_key" not in st.session_state:
    st.session_state.hevy_api_key = ""
if "llm_result" not in st.session_state:
    st.session_state.llm_result = None
if "parser_mode" not in st.session_state:
    st.session_state.parser_mode = "⚡ Smart Parser (Instant)"

# API Key Header
api_key = st.text_input(
    "Hevy API Key", 
    value=st.session_state.hevy_api_key, 
    type="password",
    help="Sua chave de API é mantida estritamente na sessão atual do navegador."
)
if api_key:
    st.session_state.hevy_api_key = api_key

st.divider()

st.subheader("1. Digite seu Treino")

default_prompt = """ROTINA DE TREINAMENTO: PERIODIZAÇÃO AB (2 DIAS)

TREINO A:
1. Bench Press (Barbell) - 4 sets of 8 reps (60kg)
2. Bent Over Row (Barbell) - 4 sets of 8 reps (50kg)
3. Squat (Barbell) - 4 sets of 6 reps (80kg)

TREINO B:
1. Deadlift (Barbell) - 4 sets of 8 reps (100kg)
2. Overhead Press (Barbell) - 4 sets of 8 reps (40kg)
3. Lat Pulldown (Cable) - 3 sets of 15 reps (45kg)"""

workout_text = st.text_area("Treino em Linguagem Natural", value=default_prompt, height=220)

col_mode, col_btn = st.columns([2, 1])

with col_mode:
    mode = st.radio(
        "Modo de Conversão:",
        ["⚡ Smart Parser (Instantâneo)", "🤖 WebLLM AI (Local Browser WebGPU)"],
        horizontal=True
    )
    st.session_state.parser_mode = mode

with col_btn:
    st.write("") # Alignment spacing
    st.write("")
    generate_clicked = st.button("Gerar JSON", type="primary", use_container_width=True)

if generate_clicked:
    if "Smart Parser" in mode:
        parsed = smart_parse_workout(workout_text)
        st.session_state.llm_result = json.dumps(parsed, indent=2, ensure_ascii=False)
        st.success("JSON gerado com sucesso via Smart Parser!")
    else:
        st.session_state.prompt_to_send = workout_text

# WebLLM Component integration (only rendered when WebLLM mode is selected)
if "WebLLM" in mode:
    st.info("💡 **WebLLM AI Mode:** O modelo Llama-3.1-8B roda 100% no seu navegador via WebGPU.")
    webllm_status = webllm_generate(prompt=st.session_state.get("prompt_to_send"), key="webllm_box")
    
    if webllm_status:
        if webllm_status.get("status") == "success":
            st.session_state.llm_result = webllm_status.get("text")
            st.session_state.prompt_to_send = None
            st.success("WebLLM gerou a estrutura do treino!")
        elif webllm_status.get("status") == "error":
            st.warning(f"WebLLM não pôde ser carregado no iframe: {webllm_status.get('error')}. Recomendamos usar o modo **⚡ Smart Parser (Instantâneo)** acima.")

st.divider()

st.subheader("2. Revisão & Envio para o Hevy")

if st.session_state.llm_result:
    try:
        parsed_json = json.loads(st.session_state.llm_result)
        
        # Display/Edit JSON
        edited_json_str = st.text_area(
            "Confira e edite a estrutura JSON antes de enviar:", 
            value=json.dumps(parsed_json, indent=2, ensure_ascii=False), 
            height=320
        )
        
        if st.button("🚀 Enviar para o Hevy", type="primary", use_container_width=True):
            if not st.session_state.hevy_api_key:
                st.error("Por favor, insira sua Hevy API Key no campo superior antes de enviar.")
            else:
                try:
                    final_json = json.loads(edited_json_str)
                    
                    with st.spinner("Conectando à API do Hevy e importando rotinas..."):
                        client = HevyClient(api_key=st.session_state.hevy_api_key)
                        importer = ProgramImporter(client)
                        
                        folder_name = final_json.get("name", "Imported Workout Program")
                        importer.import_program(final_json, folder_name=folder_name)
                        
                    st.success(f"🎉 Programa '{folder_name}' importado com sucesso para o Hevy!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Erro ao importar para o Hevy: {str(e)}")
                    st.code(traceback.format_exc())
                    
    except json.JSONDecodeError:
        st.error("JSON inválido gerado. Tente clicar em Gerar JSON novamente ou edite o texto acima.")
        st.code(st.session_state.llm_result)
else:
    st.info("Aguardando geração do treino...")
