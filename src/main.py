import sys
import os
import shutil
from src.copy_files import copy_files_rec
from src.generate_page import generate_pages_recursive

def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_path = os.path.join(BASE_DIR, "docs")
    static_path = os.path.join(BASE_DIR, "static")

    if os.path.exists(docs_path):
        shutil.rmtree(docs_path)
    os.mkdir(docs_path)

    if not os.path.exists(static_path):
        raise FileNotFoundError(f"No static directory at {static_path}")
    copy_files_rec(static_path, docs_path)

    from_path = os.path.join(BASE_DIR, "content")
    template_path = os.path.join(BASE_DIR, "template.html")
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"
    generate_pages_recursive(from_path, template_path, docs_path, base_path)

if __name__ == "__main__":  
    main()