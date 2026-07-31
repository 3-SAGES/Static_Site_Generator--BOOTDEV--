import unittest

from src.textnode import TextNode, TextType
from src.split_nodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "This is just plain text."
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode("This is just plain text.", TextType.TEXT)])

    def test_bold(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_italic(self):
        text = "This is _italic_ text"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_code(self):
        text = "This is `code` text"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )

    def test_link(self):
        text = "This is text with a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_multiple_images(self):
        text = "![img1](https://a.com/1.png) and ![img2](https://a.com/2.png)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("img1", TextType.IMAGE, "https://a.com/1.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://a.com/2.png"),
            ],
        )

    def test_all_types_combined(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![image](https://i.imgur.com/zjjcJKZ.png) and a "
            "[link](https://boot.dev)"
        )
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_empty_string(self):
        nodes = text_to_textnodes("")
        self.assertEqual(nodes, [])

    def test_unmatched_delimiter_raises(self):
        text = "This has an **unmatched bold"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)


if __name__ == "__main__":
    unittest.main()