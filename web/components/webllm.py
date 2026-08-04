import os
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while developing,
# and True when deploying to GitHub Pages/Stlite so it uses the local files.
_RELEASE = True

if not _RELEASE:
    # If not release, you'd typically run a dev server for the component
    _component_func = components.declare_component(
        "webllm",
        url="http://localhost:3001",
    )
else:
    # In release mode (or Stlite), point to the local component folder
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "webllm_component")
    _component_func = components.declare_component("webllm", path=build_dir)

def webllm_generate(prompt=None, key=None):
    """
    Creates a new instance of the WebLLM component.
    
    Parameters
    ----------
    prompt: str or None
        The prompt to send to the WebLLM engine.
    key: str or None
        An optional key that uniquely identifies this component.
        
    Returns
    -------
    dict
        A dictionary containing the status ("ready", "success", "error")
        and the result text if successful.
    """
    component_value = _component_func(prompt=prompt, key=key, default=None)
    return component_value
