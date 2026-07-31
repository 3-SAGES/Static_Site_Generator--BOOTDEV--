import unittest
from src.htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_repr(self):
        node = LeafNode("a", "just text", {"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(
        repr(node),
        "LeafNode(a, just text, {'href': 'https://boot.dev', 'target': '_blank'})"
        )