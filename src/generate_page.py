import os

from src.md_functions import markdown_to_html_node, extract_title
from src.htmlnode import ParentNode


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    for entry in os.listdir(dir_path_content):
            new_dir_path_content = os.path.join(dir_path_content, entry)
            new_dest_dir_path = os.path.join(dest_dir_path, entry)
    
            if os.path.isfile(new_dir_path_content) and new_dir_path_content.endswith("md"):
                generate_page(new_dir_path_content, template_path, new_dest_dir_path.replace(".md", ".html"))
                
            elif os.path.isdir(new_dir_path_content):
                os.mkdir(new_dest_dir_path)
                generate_pages_recursive(new_dir_path_content, template_path, new_dest_dir_path) 



def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown_text = f.read()
    with open(template_path) as f:
        html_template = f.read()

    html_content = markdown_to_html_node(markdown_text).to_html()
    title = extract_title(markdown_text)

    html_template = html_template.replace("{{ Title }}", title)
    html_template = html_template.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, mode="w") as f:
        f.write(html_template)
