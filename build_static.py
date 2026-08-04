import os
import json

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def collect_files():
    files_dict = {}
    
    # 1. Collect Iron Ledger core module
    for root, _, files in os.walk("iron_ledger"):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                files_dict[filepath] = read_file(filepath)
                
    # 2. Collect Web app files
    files_dict["app.py"] = read_file("web/app.py")
    
    return files_dict

def build_index_html():
    files = collect_files()
    
    # Escape </script> inside inlined Python source to prevent HTML breakage
    files_json = json.dumps(files).replace("</", "<\\/")
    
    # Create the Stlite HTML template
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
  <title>Iron Ledger Web</title>
  <!-- Load Stlite -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.55.1/build/stlite.css" />
  <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.55.1/build/stlite.js"></script>
</head>
<body>
  <div id="root"></div>
  <script>
    const files = {files_json};
    
    stlite.mount({{
      requirements: ["requests", "python-dotenv"],
      entrypoint: "app.py",
      files: files,
    }}, document.getElementById("root"));
  </script>
</body>
</html>
"""
    
    os.makedirs("dist", exist_ok=True)
    with open("dist/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Static build successful! Files written to dist/index.html")

if __name__ == "__main__":
    build_index_html()
