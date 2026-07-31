import unittest
from src.htmlnode import HTMLNode


class TextHTMLNode(unittest.TestCase):
    def test_all_defaults_to_None(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr(self):
        node = HTMLNode("a", "just text", [HTMLNode(tag="a", props={}), HTMLNode()], {"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(
        repr(node),
        "HTMLNode(a, just text, [HTMLNode(a, None, None, {}), HTMLNode(None, None, None, None)], {'href': 'https://boot.dev', 'target': '_blank'})"
        )

    def test_props_to_html_none(self):
        node = HTMLNode(tag="p")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(tag = "a", props = {})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(tag="a", value = "just text", props={"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev" target="_blank"')


if __name__ == "__main__":
    unittest.main()