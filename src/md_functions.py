from enum import Enum
from src.htmlnode import ParentNode, HTMLNode
from src.split_nodes import text_to_textnodes
from src.textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.removeprefix("# ").strip()
    raise Exception("No title was found")

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children_nodes = []

    for block in blocks:
        children_nodes.append(block_to_html_node(block))

    return ParentNode("div", children_nodes)


def block_to_html_node(block: str) -> ParentNode:
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            return ParentNode("p", block_to_children_nodes(block))
        
        case BlockType.HEADING:
            level = len(block) - len(block.lstrip("#"))
            text = block[level + 1:]
            return ParentNode(f"h{level}", block_to_children_nodes(text))
        
        case BlockType.CODE:
            text_node = TextNode(block[4:-3], TextType.CODE)
            return ParentNode("pre", [ParentNode("code", [text_node_to_html_node(text_node)])])
        
        case BlockType.QUOTE:
            lines = block.split("\n")
            stripped = [line.lstrip(">").strip() for line in lines]
            text = " ".join(stripped)
            return ParentNode("blockquote", block_to_children_nodes(text))
        
        case BlockType.UNORDERED_LIST:
            return ParentNode("ul", list_block_to_children_nodes(block, ordered=False))
        
        case BlockType.ORDERED_LIST:
            return ParentNode("ol", list_block_to_children_nodes(block, ordered=True))


def list_block_to_children_nodes(block: str, ordered: bool) -> list[HTMLNode]:
    lines = block.split("\n")
    if ordered:
        texts = [line.removeprefix(f"{n}. ") for n, line in enumerate(lines, start=1)]
    else:
        texts = [line.removeprefix("- ") for line in lines]
    return [ParentNode("li", block_to_children_nodes(text)) for text in texts]

def block_to_children_nodes(block: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(block)
    children_nodes = []
    for node in text_nodes:
        children_nodes.append(text_node_to_html_node(node))
    return children_nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip() != ""]


def block_to_block_type(block: str) -> BlockType:
    HEADINGS = ("# ", "## ", "### ", "#### ", "##### ", "###### ")

    if block.startswith(HEADINGS):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i}. ") for i, line in enumerate(block.split("\n"), start=1)):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
