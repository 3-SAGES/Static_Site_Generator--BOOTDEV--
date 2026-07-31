import unittest
from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node1 = TextNode("TEXT", TextType.ITALIC, "www.www.ww")
        node2 = TextNode("TEXT", TextType.IMAGE, "www.www.ww")
        self.assertNotEqual

    def test_url_defaults_to_none(self):
        node = TextNode("Just text", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_url_is_set(self):
        node = TextNode("Link text", TextType.LINK, "https://boot.dev")
        self.assertEqual(node.url, "https://boot.dev")

    def test_repr(self):
        node = TextNode("Hi", TextType.TEXT, "https://x.com")
        self.assertEqual(
            repr(node),
            "TextNode(Hi, text, https://x.com)"
        )

    
if __name__ == "__main__":
    unittest.main()