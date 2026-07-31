import os
import shutil
from src.copy_files import copy_files_rec
from src.generate_page import generate_pages_recursive

def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    public_path = os.path.join(BASE_DIR, "public")
    static_path = os.path.join(BASE_DIR, "static")

    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir(public_path)

    if not os.path.exists(static_path):
        raise FileNotFoundError(f"No static directory at {static_path}")
    copy_files_rec(static_path, public_path)

    from_path = os.path.join(BASE_DIR, "content")
    template_path = os.path.join(BASE_DIR, "template.html")
    generate_pages_recursive(from_path, template_path, public_path)

if __name__ == "__main__":  
    main()