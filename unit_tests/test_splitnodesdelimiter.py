import unittest

from textnode import TextNode, TextType
from src.split_nodes import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        node = TextNode("plain text, nothing special", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("plain text, nothing special", TextType.TEXT)])

    def test_single_bold_pair(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_code_delimiter(self):
        node = TextNode("Run `print(x)` now", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("Run ", TextType.TEXT),
                TextNode("print(x)", TextType.CODE),
                TextNode(" now", TextType.TEXT),
            ],
        )

    def test_multiple_pairs_same_node(self):
        node = TextNode("**a** and **b**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("a", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
            ],
        )

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This is *unmatched", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC)

    def test_non_text_node_passed_through_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_mixed_list_of_nodes(self):
        nodes = [
            TextNode("plain ", TextType.TEXT),
            TextNode("already italic", TextType.ITALIC),
            TextNode("some `code` here", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("plain ", TextType.TEXT),
                TextNode("already italic", TextType.ITALIC),
                TextNode("some ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_empty_string_node(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [])

    def test_delimiter_at_start_and_end(self):
        node = TextNode("**bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("bold", TextType.BOLD)])


if __name__ == "__main__":
    unittest.main()