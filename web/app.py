import sys
import os
import re
import json
import traceback
import streamlit as st
import streamlit.components.v1 as components

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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

workout_text = st.text_area("Treino em Linguagem Natural", value=default_prompt, height=200)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("⚡ Gerar JSON (Smart Parser)", type="primary", use_container_width=True):
        parsed = smart_parse_workout(workout_text)
        st.session_state.llm_result = json.dumps(parsed, indent=2, ensure_ascii=False)
        st.success("JSON gerado instantaneamente via Smart Parser!")

with col2:
    show_webllm = st.checkbox("🤖 Exibir WebLLM AI (Local GPU)", value=False)

if show_webllm:
    st.info("💡 **WebLLM AI Mode:** Executa o modelo Llama-3.1 via WebGPU diretamente no seu navegador.")
    
    webllm_html = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        body { font-family: system-ui, -apple-system, sans-serif; color: #1f2937; margin: 0; padding: 10px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; }
        #status { font-size: 13px; font-weight: 500; margin-bottom: 8px; color: #475569; display: flex; align-items: center; gap: 8px; }
        .spinner { border: 2px solid #cbd5e1; border-top: 2px solid #2563eb; border-radius: 50%; width: 14px; height: 14px; animation: spin 0.8s linear infinite; display: none; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        button { background: #2563eb; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 13px; }
        button:hover { background: #1d4ed8; }
        button:disabled { background: #94a3b8; cursor: not-allowed; }
        textarea { width: 100%; height: 100px; font-family: monospace; font-size: 11px; margin-top: 8px; padding: 6px; border-radius: 6px; border: 1px solid #cbd5e1; box-sizing: border-box; background: #ffffff; }
      </style>
    </head>
    <body>
      <div id="status"><div class="spinner" id="spinner"></div><span id="text">Engine WebLLM Pronto</span></div>
      <button id="genBtn" onclick="runWebLLM()">🤖 Processar com WebLLM AI</button>
      <textarea id="output" placeholder="O JSON gerado pelo WebLLM aparecerá aqui..." readonly></textarea>

      <script type="module">
        import { CreateMLCEngine } from "https://esm.run/@mlc-ai/web-llm";

        let engine = null;

        window.runWebLLM = async function() {
          const btn = document.getElementById('genBtn');
          const textEl = document.getElementById('text');
          const spinnerEl = document.getElementById('spinner');
          const out = document.getElementById('output');

          btn.disabled = true;
          spinnerEl.style.display = 'inline-block';

          try {
            if (!navigator.gpu) {
              throw new Error("WebGPU não suportado neste navegador. Use Chrome ou Edge no Desktop.");
            }

            if (!engine) {
              textEl.innerText = "Baixando modelo Llama-3.1 (WebLLM)...";
              engine = await CreateMLCEngine("Llama-3.1-8B-Instruct-q4f32_1-MLC", {
                initProgressCallback: (p) => { textEl.innerText = p.text; }
              });
            }

            textEl.innerText = "Gerando estrutura JSON...";
            
            // Search for parent textarea content
            let promptText = "Bench Press 4x8 60kg";
            try {
              const textareas = window.parent.document.querySelectorAll('textarea');
              if (textareas && textareas.length > 0) {
                promptText = textareas[0].value;
              }
            } catch(e) {}

            const reply = await engine.chat.completions.create({
              messages: [
                { 
                  role: "system", 
                  content: "Convert workout to valid JSON format: {\\\"name\\\": \\\"Workout Title\\\", \\\"workouts\\\": [{\\\"title\\\": \\\"Day 1\\\", \\\"exercises\\\": [{\\\"name\\\": \\\"Bench Press (Barbell)\\\", \\\"sets\\\": [{\\\"type\\\": \\\"normal\\\", \\\"reps\\\": 8, \\\"weight_kg\\\": 60}]}]}]}. Return ONLY JSON." 
                },
                { role: "user", content: promptText }
              ]
            });

            out.value = reply.choices[0].message.content;
            textEl.innerText = "Concluído! Copie o JSON abaixo para a Etapa 2.";
          } catch (err) {
            textEl.innerText = "Erro: " + err.message;
            out.value = "Erro WebLLM: " + err.message + "\\n\\nDica: Use o botão '⚡ Gerar JSON (Smart Parser)' acima que é 100% compatível!";
          }

          btn.disabled = false;
          spinnerEl.style.display = 'none';
        };
      </script>
    </body>
    </html>
    """
    components.html(webllm_html, height=220)

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
