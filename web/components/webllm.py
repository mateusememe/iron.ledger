import os
import streamlit.components.v1 as components

# Point to the local component folder safely
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "webllm_component")

_component_func = None

try:
    if os.path.exists(build_dir):
        _component_func = components.declare_component("webllm", path=build_dir)
except Exception as e:
    _component_func = None

def webllm_generate(prompt=None, key=None):
    """
    Safely creates an instance of the WebLLM component.
    Returns a status dict or None if component is not ready/available.
    """
    if _component_func is None:
        return {"status": "error", "error": "WebLLM component files not found."}
    
    try:
        return _component_func(prompt=prompt, key=key, default=None)
    except Exception as e:
        return {"status": "error", "error": str(e)}
