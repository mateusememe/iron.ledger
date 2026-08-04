import os
import shutil
import requests

MODELS = [
    "mlc-ai/Llama-3.2-1B-Instruct-q4f16_1-MLC",
    "mlc-ai/Qwen2.5-1.5B-Instruct-q4f16_1-MLC",
]

HTTP_TIMEOUT = 30  # seconds


def list_repo_files(repo_id: str) -> list:
    """List all files in a HuggingFace repo, recursing into subdirectories."""
    tree_url = f"https://huggingface.co/api/models/{repo_id}/tree/main"
    all_files = []

    def _walk(path: str = "") -> None:
        url = tree_url if not path else f"{tree_url}/{path}"
        res = requests.get(url, timeout=HTTP_TIMEOUT)
        if res.status_code != 200:
            print(f"  ✗ Error listing {url}: {res.status_code}")
            return
        for item in res.json():
            if item["type"] == "directory":
                _walk(item["path"])
            elif item["type"] == "file":
                all_files.append(item)

    _walk()
    return all_files


def download_repo(repo_id: str, target_dir: str) -> None:
    print(f"Checking/Downloading model {repo_id} -> {target_dir}")
    os.makedirs(target_dir, exist_ok=True)

    items = list_repo_files(repo_id)
    if not items:
        print(f"  ✗ No files found for {repo_id}")
        return

    for item in items:
        filename = item["path"]
        expected_size = item.get("size")

        if filename.endswith(".md") or filename.startswith("."):
            continue

        file_url = f"https://huggingface.co/{repo_id}/resolve/main/{filename}"
        dest_path = os.path.join(target_dir, filename)

        # Create subdirectories if needed
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        # Check cache: verify both existence AND size
        if os.path.exists(dest_path):
            if expected_size is not None and os.path.getsize(dest_path) != expected_size:
                print(f"  ⚠ [Truncated] {filename} ({os.path.getsize(dest_path)} != {expected_size}), re-downloading...")
                os.remove(dest_path)
            else:
                print(f"  ✓ [Cached] {filename}")
                continue

        print(f"  ↓ Downloading {filename}...")
        r = requests.get(file_url, stream=True, timeout=HTTP_TIMEOUT)
        if r.status_code == 200:
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                    f.write(chunk)
            # Post-download integrity check
            if expected_size is not None and os.path.getsize(dest_path) != expected_size:
                print(f"  ✗ Size mismatch after download: {filename} ({os.path.getsize(dest_path)} != {expected_size})")
                os.remove(dest_path)
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
