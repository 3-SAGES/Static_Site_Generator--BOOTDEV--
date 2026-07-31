from src.textnode import TextNode, TextType
from src.extract_markdown import extract_markdown_links, extract_markdown_images


def text_to_textnodes(text: str) -> list[TextNode]:
    types = [
    ("**", TextType.BOLD),
    ("_", TextType.ITALIC),
    ("`", TextType.CODE),
    ] 
    nodes = [TextNode(text, TextType.TEXT)]

    for delimiter, text_type in types:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)

    return nodes


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue 
        
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(f"invalid markdown syntax: unmatched delimiter {delimiter!r}")

        for i, text in enumerate(sections):
            if text == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for image_alt, image_url in extract_markdown_images(remaining_text):
            before_text, remaining_text  = remaining_text.split(f"![{image_alt}]({image_url})", 1)
            if before_text != "":
                new_nodes.append(TextNode(before_text, TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for link_txt, link_url in extract_markdown_links(remaining_text):
            before_text, remaining_text = remaining_text.split(f"[{link_txt}]({link_url})", 1)
            if before_text != "":
                new_nodes.append(TextNode(before_text, TextType.TEXT))
            new_nodes.append(TextNode(link_txt, TextType.LINK, link_url))

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes