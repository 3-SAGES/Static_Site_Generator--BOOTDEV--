import unittest
from src.split_nodes import split_nodes_image, split_nodes_links
from src.textnode import TextNode, TextType

class TestSplitNodesImagesLniks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_single(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_no_image(self):
        node = TextNode("This is just plain text, nothing to split.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is just plain text, nothing to split.", TextType.TEXT)],
            new_nodes,
        )

    def test_split_images_starts_with_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) starts the text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" starts the text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and another [second link](https://blog.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://blog.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_no_link(self):
        node = TextNode("This is just plain text, no links here.", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [TextNode("This is just plain text, no links here.", TextType.TEXT)],
            new_nodes,
        )

    def test_split_links_ignores_images(self):
        # split_nodes_links should NOT treat an image as a link
        node = TextNode(
            "This has an ![image](https://i.imgur.com/zjjcJKZ.png) but no real link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [TextNode(
                "This has an ![image](https://i.imgur.com/zjjcJKZ.png) but no real link",
                TextType.TEXT,
            )],
            new_nodes,
        )

    def test_split_images_ignores_links(self):
        # split_nodes_image should NOT pick up a plain link
        node = TextNode(
            "This has a [link](https://boot.dev) but no image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode(
                "This has a [link](https://boot.dev) but no image",
                TextType.TEXT,
            )],
            new_nodes,
        )

    def test_split_images_and_links_mixed(self):
        node = TextNode(
            "Here is a [link](https://boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png) together",
            TextType.TEXT,
        )
        image_nodes = split_nodes_image([node])
        link_nodes = split_nodes_links([node])

        self.assertListEqual(
            [
                TextNode("Here is a [link](https://boot.dev) and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" together", TextType.TEXT),
            ],
            image_nodes,
        )
        self.assertListEqual(
            [
                TextNode("Here is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and an ![image](https://i.imgur.com/zjjcJKZ.png) together", TextType.TEXT),
            ],
            link_nodes,
        )