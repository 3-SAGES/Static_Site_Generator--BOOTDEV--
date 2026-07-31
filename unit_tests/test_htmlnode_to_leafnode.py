import unittest
from src.textnode import text_node_to_html_node, TextNode, TextType

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_exception(self):
        node = TextNode("sample text", None, "www.www.ww")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_img(self):
        node = TextNode("Hot GIFLS in local area", TextType.IMAGE, "www.grannyhub.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "www.grannyhub.com", "alt": "Hot GIFLS in local area"})