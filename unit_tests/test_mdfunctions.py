import unittest
import textwrap
from src.md_functions import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = textwrap.dedent("""
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """)

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace(self):
        self.assertEqual(markdown_to_blocks("\n\n   \n\n"), [])

    def test_single_block(self):
        md = "Just one paragraph with no blank lines"
        self.assertEqual(markdown_to_blocks(md), ["Just one paragraph with no blank lines"])

    def test_leading_and_trailing_newlines(self):
        md = "\n\n# Heading\n\nSome text\n\n\n"
        self.assertEqual(markdown_to_blocks(md), ["# Heading", "Some text"])

    def test_excessive_blank_lines_between_blocks(self):
        md = "First block\n\n\n\n\nSecond block"
        self.assertEqual(markdown_to_blocks(md), ["First block", "Second block"])

    def test_blank_line_with_trailing_spaces(self):
        md = "First block\n\n   \n\nSecond block"
        self.assertEqual(markdown_to_blocks(md), ["First block", "Second block"])

    def test_multiline_block_preserved(self):
        md = "- item one\n- item two\n- item three\n\nAfter the list"
        self.assertEqual(
            markdown_to_blocks(md),
            ["- item one\n- item two\n- item three", "After the list"],
        )        



class TestBlockToBlockType(unittest.TestCase):
    # --- headings ---
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_heading_seven_hashes_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Nope"), BlockType.PARAGRAPH)

    def test_heading_without_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    # --- code ---
    def test_code_block(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_with_language(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_bare_fence_is_paragraph(self):
        self.assertEqual(block_to_block_type("```"), BlockType.PARAGRAPH)

    def test_unclosed_fence_is_paragraph(self):
        self.assertEqual(block_to_block_type("```\nprint('hi')"), BlockType.PARAGRAPH)

    # --- quote ---
    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> quoted"), BlockType.QUOTE)

    def test_quote_multiline(self):
        block = "> line one\n> line two\n> line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_one_line_missing_marker(self):
        block = "> line one\nline two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- unordered list ---
    def test_unordered_list(self):
        block = "- one\n- two\n- three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("-one\n-two"), BlockType.PARAGRAPH)

    def test_unordered_list_one_line_unmarked(self):
        self.assertEqual(block_to_block_type("- one\ntwo"), BlockType.PARAGRAPH)

    # --- ordered list ---
    def test_ordered_list(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_single_item(self):
        self.assertEqual(block_to_block_type("1. only"), BlockType.ORDERED_LIST)

    def test_ordered_list_not_starting_at_one(self):
        block = "2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_skipping_number(self):
        block = "1. one\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_decimal_number_is_paragraph(self):
        self.assertEqual(block_to_block_type("1.5 million in revenue"), BlockType.PARAGRAPH)

    # --- paragraph ---
    def test_plain_paragraph(self):
        self.assertEqual(block_to_block_type("Just some text"), BlockType.PARAGRAPH)

    def test_multiline_paragraph(self):
        block = "Line one of the paragraph\nline two of the paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_containing_inline_markdown(self):
        block = "This has **bold** and `code` but is still a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)