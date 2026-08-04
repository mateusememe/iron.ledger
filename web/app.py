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
from iron_ledger.config import Config
from iron_ledger.importer.importer import ProgramImporter

st.set_page_config(page_title="Iron Ledger Web", page_icon="🏋️", layout="centered")

def extract_json_from_llm_response(text: str) -> str:
    """
    Extracts valid JSON object from LLM response text,
    stripping markdown codeblocks (```json ... ```) and conversational text.
    """
    if not text:
        return ""
        
    # Strip markdown codeblock backticks
    clean = re.sub(r'```(?:json)?', '', text).strip('` \t\r\n')
    
    # Extract first '{' to last '}'
    match = re.search(r'(\{[\s\S]*\})', clean)
    if match:
        return match.group(1).strip()
        
    return clean

# Default rest time in seconds between sets
DEFAULT_REST_SECONDS = 90

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
        ex_match = re.search(r'^(?:\d+[\.\)]\s*)?([A-Za-zÀ-ÿ\s\(\)\-\/\:\,]+?)(?:[\:\-]\s*|\s+\d+\s*(?:x|sets|séries|\*))', line_str, re.IGNORECASE)
        if ex_match:
            candidate = ex_match.group(1).strip(" :-")
            if len(candidate) > 2 and not candidate.upper().startswith("FOCO") and not candidate.upper().startswith("OBSERVAÇÃO"):
                ex_name = candidate
                
        if ex_name:
            exercise_obj = {
                "name": ex_name,
                "rest_seconds": DEFAULT_REST_SECONDS,
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

default_prompt = """ROTINA DE TREINAMENTO: PERIODIZAÇÃO AB (2 DIAS)

TREINO A:
1. Bench Press (Barbell) - 4 sets of 8 reps (60kg)
2. Bent Over Row (Barbell) - 4 sets of 8 reps (50kg)
3. Squat (Barbell) - 4 sets of 6 reps (80kg)

TREINO B:
1. Deadlift (Barbell) - 4 sets of 8 reps (100kg)
2. Overhead Press (Barbell) - 4 sets of 8 reps (40kg)
3. Lat Pulldown (Cable) - 3 sets of 15 reps (45kg)"""

if "llm_result" not in st.session_state or st.session_state.llm_result is None:
    initial_parsed = smart_parse_workout(default_prompt)
    st.session_state.llm_result = json.dumps(initial_parsed, indent=2, ensure_ascii=False)

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

workout_text = st.text_area("Treino em Linguagem Natural", value=default_prompt, height=200)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("⚡ Gerar JSON (Smart Parser)", type="primary", use_container_width=True):
        parsed = smart_parse_workout(workout_text)
        st.session_state.llm_result = json.dumps(parsed, indent=2, ensure_ascii=False)
        st.success("JSON gerado instantaneamente na Etapa 2 abaixo!")

with col2:
    show_webllm = st.checkbox("🤖 Exibir WebLLM AI (Local GPU)", value=False)

if show_webllm:
    model_choice = st.selectbox(
        "Escolha o Modelo WebLLM:",
        [
            "Llama-3.2-1B-Instruct-q4f16_1-MLC (⚡ Localhost Server ~0.5s)",
            "Qwen2.5-1.5B-Instruct-q4f16_1-MLC (🚀 Localhost Server ~0.8s)",
            "Phi-3.5-mini-instruct-q4f16_1-MLC (⚖️ HuggingFace CDN ~1.6GB)",
            "Llama-3.1-8B-Instruct-q4f32_1-MLC (🧠 HuggingFace CDN ~4.3GB)",
        ],
        index=0
    )
    
    # Extract actual MLC model id string
    selected_model_id = model_choice.split(" ")[0]
    
    st.info(f"💡 **WebLLM AI Mode ({selected_model_id}):** Ao clicar no botão abaixo, o JSON será gerado pela GPU e preencherá a **Etapa 2** automaticamente!")
    
    webllm_html = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        :root {
          --bg-color: #0e1117;
          --card-bg: #161b22;
          --border-color: #30363d;
          --text-color: #e6edf3;
          --muted-color: #8b949e;
          --primary-color: #ff4b4b;
          --primary-hover: #e03e3e;
          --code-bg: #0d1117;
        }
        @media (prefers-color-scheme: light) {
          :root {
            --bg-color: #ffffff;
            --card-bg: #f8fafc;
            --border-color: #e2e8f0;
            --text-color: #1e293b;
            --muted-color: #64748b;
            --primary-color: #ff4b4b;
            --primary-hover: #e03e3e;
            --code-bg: #ffffff;
          }
        }
        body {
          font-family: Source Sans Pro, -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
          color: var(--text-color);
          margin: 0;
          padding: 12px;
          background: var(--card-bg);
          border: 1px solid var(--border-color);
          border-radius: 8px;
        }
        #status {
          font-size: 13px;
          font-weight: 500;
          margin-bottom: 10px;
          color: var(--muted-color);
          display: flex;
          align-items: center;
          gap: 8px;
        }
        .spinner {
          border: 2px solid var(--border-color);
          border-top: 2px solid var(--primary-color);
          border-radius: 50%;
          width: 14px;
          height: 14px;
          animation: spin 0.8s linear infinite;
          display: none;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        button {
          background-color: var(--primary-color);
          color: #ffffff;
          border: none;
          padding: 9px 18px;
          border-radius: 6px;
          font-weight: 600;
          cursor: pointer;
          font-size: 13px;
          transition: background-color 0.2s;
        }
        button:hover { background-color: var(--primary-hover); }
        button:disabled { opacity: 0.6; cursor: not-allowed; }
        textarea {
          width: 100%;
          height: 90px;
          font-family: "Source Code Pro", monospace;
          font-size: 11px;
          margin-top: 10px;
          padding: 8px;
          border-radius: 6px;
          border: 1px solid var(--border-color);
          box-sizing: border-box;
          background: var(--code-bg);
          color: var(--text-color);
        }
      </style>
    </head>
    <body>
      <div id="status"><div class="spinner" id="spinner"></div><span id="text">Modelo selecionado: {SELECTED_MODEL_ID}</span></div>
      <button id="genBtn" onclick="runWebLLM()">🤖 Processar & Preencher Etapa 2 ({SELECTED_MODEL_ID})</button>

      <script type="module">
        import { CreateMLCEngine, prebuiltAppConfig } from "https://esm.run/@mlc-ai/web-llm@0.2.78";

        let engine = null;
        let currentModel = "{SELECTED_MODEL_ID}";

        window.runWebLLM = async function() {
          const btn = document.getElementById('genBtn');
          const textEl = document.getElementById('text');
          const spinnerEl = document.getElementById('spinner');

          btn.disabled = true;
          spinnerEl.style.display = 'inline-block';

          try {
            if (!navigator.gpu) {
              throw new Error("WebGPU não suportado neste navegador. Use Chrome ou Edge no Desktop.");
            }

            if (!engine) {
              textEl.innerText = `Carregando modelo ${currentModel} do servidor local...`;
              
              const hostOrigin = window.parent.location.origin;
              const localModelUrl = hostOrigin + "/app/static/models/" + currentModel;
              
              const MODEL_LIB_MAP = {
                "Llama-3.2-1B-Instruct-q4f16_1-MLC": "Llama-3.2-1B-Instruct-q4f16_1-ctx4k-webgpu.wasm",
                "Qwen2.5-1.5B-Instruct-q4f16_1-MLC": "Qwen2.5-1.5B-Instruct-q4f16_1-ctx4k-webgpu.wasm",
                "Phi-3.5-mini-instruct-q4f16_1-MLC": "Phi-3.5-mini-instruct-q4f16_1-ctx4k-webgpu.wasm",
                "Llama-3.1-8B-Instruct-q4f32_1-MLC": "Llama-3.1-8B-Instruct-q4f32_1-ctx4k-webgpu.wasm",
              };
              const libFile = MODEL_LIB_MAP[currentModel];

              const customAppConfig = {
                model_list: [
                  {
                    model: localModelUrl,
                    model_id: currentModel,
                    model_lib: libFile
                      ? "https://raw.githubusercontent.com/mlc-ai/binary-mlc-llm-libs/main/" + libFile
                      : undefined,
                  },
                  ...prebuiltAppConfig.model_list
                ]
              };

              try {
                engine = await CreateMLCEngine(currentModel, {
                  appConfig: customAppConfig,
                  initProgressCallback: (p) => { textEl.innerText = p.text; }
                });
              } catch(errLocal) {
                console.warn("Local static route fetch failed, falling back to CDN:", errLocal);
                textEl.innerText = `Carregando da CDN externa...`;
                engine = await CreateMLCEngine(currentModel, {
                  appConfig: prebuiltAppConfig,
                  initProgressCallback: (p) => { textEl.innerText = p.text; }
                });
              }
            }

            textEl.innerText = "Gerando estrutura JSON...";
            
            // Search for parent textarea content by class
            let promptText = "";
            let targetTextarea = null;
            try {
              const textareas = window.parent.document.querySelectorAll('.stTextArea textarea');
              if (textareas && textareas.length > 0) {
                promptText = textareas[0].value;
              }
              if (textareas && textareas.length > 1) {
                targetTextarea = textareas[1];
              }
            } catch(e) {
              console.warn("Could not access parent textareas:", e);
            }

            if (!promptText) {
              textEl.innerText = "Erro: Nenhum texto de treino encontrado. Digite seu treino na Etapa 1.";
              btn.disabled = false;
              spinnerEl.style.display = 'none';
              return;
            }

            const reply = await engine.chat.completions.create({
              messages: [
                { 
                  role: "system", 
                  content: `Você é um assistente de IA especialista em planilhas de treino. 
Sua tarefa é extrair treinos de textos não-estruturados.
Regras OBRIGATÓRIAS:
1. Responda APENAS com um JSON válido, sem NENHUM texto adicional antes ou depois.
2. A hierarquia do JSON DEVE ser estritamente: Rotina -> array "workouts" -> array "exercises" -> array "sets". NUNCA coloque "sets" diretamente dentro de um workout. Cada workout tem vários exercises, e cada exercise tem vários sets.
3. Formato esperado exato: {"name": "Nome da Rotina", "workouts": [{"title": "Nome do Treino (ex: Upper)", "exercises": [{"name": "Supino", "sets": [{"type": "normal", "reps": 10, "weight_kg": 0}]}]}]}
4. Se houver variação de repetições (ex: "8-12 repetições" ou "10 a 15"), extraia apenas o valor MAIOR (ex: 12 ou 15) como um NÚMERO (nunca como texto).
5. Se o usuário não mencionar a carga/peso, defina weight_kg estritamente como o número 0.
6. Se houver mais de um grupo muscular ou divisão citada (ex: Upper e Lower, ou Treino A e Treino B), crie múltiplos objetos distintos dentro da lista "workouts".
7. Crie os objetos "sets" de acordo com a quantidade de séries pedidas (ex: "3 séries" -> array com 3 objetos).`
                },
                { role: "user", content: promptText }
              ],
              temperature: 0.1,
              max_tokens: 8192
            });

            const rawText = reply.choices[0].message.content;
            const jsonMatch = rawText.match(/\{[\s\S]*\}/);
            const cleanJson = jsonMatch ? jsonMatch[0] : rawText;

            textEl.innerText = "Concluído! Preenchendo Etapa 2 automaticamente...";

            // Auto-populate Step 2 textarea in parent Streamlit window
            try {
              if (targetTextarea) {
                
                const valueSetter = Object.getOwnPropertyDescriptor(targetTextarea, 'value')?.set;
                const prototype = Object.getPrototypeOf(targetTextarea);
                const prototypeSetter = Object.getOwnPropertyDescriptor(prototype, 'value')?.set;
                
                if (prototypeSetter && valueSetter !== prototypeSetter) {
                  prototypeSetter.call(targetTextarea, cleanJson);
                } else if (valueSetter) {
                  valueSetter.call(targetTextarea, cleanJson);
                } else {
                  targetTextarea.value = cleanJson;
                }
                
                targetTextarea.dispatchEvent(new Event('input', { bubbles: true }));
                targetTextarea.dispatchEvent(new Event('change', { bubbles: true }));
              }
            } catch(errSync) {
              console.warn("Could not auto-populate parent textarea:", errSync);
            }
          } catch (err) {
            textEl.innerText = "Erro: " + err.message;
          }

          btn.disabled = false;
          spinnerEl.style.display = 'none';
        };
      </script>
    </body>
    </html>
    """.replace("{SELECTED_MODEL_ID}", selected_model_id)

    components.html(webllm_html, height=220)

st.divider()

st.subheader("2. Revisão & Envio para o Hevy")

cleaned_json_text = extract_json_from_llm_response(st.session_state.llm_result)
try:
    parsed_json = json.loads(cleaned_json_text)
    
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
                    config = Config(hevy_api_key=st.session_state.hevy_api_key)
                    importer = ProgramImporter(config)
                    
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
