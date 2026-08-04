import os
import shutil
import requests

MODELS = [
    "mlc-ai/Llama-3.2-1B-Instruct-q4f16_1-MLC",
    "mlc-ai/Qwen2.5-1.5B-Instruct-q4f16_1-MLC",
]

def download_repo(repo_id, target_dir):
    print(f"Checking/Downloading model {repo_id} -> {target_dir}")
    os.makedirs(target_dir, exist_ok=True)
    
    tree_url = f"https://huggingface.co/api/models/{repo_id}/tree/main"
    res = requests.get(tree_url)
    if res.status_code != 200:
        print(f"Error fetching repo tree for {repo_id}: {res.status_code}")
        return
        
    items = res.json()
    files = [item["path"] for item in items if item["type"] == "file"]
    
    for filename in files:
        if filename.endswith(".md") or filename.startswith("."):
            continue
            
        file_url = f"https://huggingface.co/{repo_id}/resolve/main/{filename}"
        dest_path = os.path.join(target_dir, filename)
        
        if os.path.exists(dest_path):
            print(f"  ✓ [Cached] {filename}")
            continue
            
        print(f"  ↓ Downloading {filename}...")
        r = requests.get(file_url, stream=True)
        if r.status_code == 200:
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024): # 1MB chunks
                    f.write(chunk)
        else:
            print(f"  ✗ Failed to download {filename}: {r.status_code}")

def main():
    base_dir = os.path.abspath(os.path.join("static", "models"))
    
    # Migrate from old ./models if present
    old_models = os.path.abspath("models")
    if os.path.exists(old_models) and not os.path.exists(base_dir):
        print(f"Moving models from {old_models} to {base_dir}...")
        shutil.move(old_models, base_dir)

    for repo in MODELS:
        model_name = repo.split("/")[-1]
        model_dir = os.path.join(base_dir, model_name)
        download_repo(repo, model_dir)
        
    print("All models ready locally in ./static/models/")

if __name__ == "__main__":
    main()
