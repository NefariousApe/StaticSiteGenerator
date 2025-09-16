import unittest
from textnode import TextNode, TextType
from markdown_to_nodes import split_nodes, split_nodes_image, split_nodes_link

class TestSplitNodes(unittest.TestCase):
    def test_basic_code_conversion(self):
        
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        result = split_nodes([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL)
        ]
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result, expected)
    
    def test_multiple_delimiters(self):
        
        node = TextNode("Normal `code` more normal `another code`", TextType.NORMAL)
        result = split_nodes([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Normal ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" more normal ", TextType.NORMAL),
            TextNode("another code", TextType.CODE),
        ]
        
        self.assertEqual(len(result), 4)
        self.assertEqual(result, expected)
    
    def test_bold_conversion(self):
        
        node = TextNode("This has **bold text** in it", TextType.NORMAL)
        result = split_nodes([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This has ", TextType.NORMAL),
            TextNode("bold text", TextType.BOLD),
            TextNode(" in it", TextType.NORMAL)
        ]
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result, expected)
    
    def test_italic_conversion(self):
        
        node = TextNode("This has _italic text_ in it", TextType.NORMAL)
        result = split_nodes([node], "_", TextType.ITALIC)
        
        expected = [
            TextNode("This has ", TextType.NORMAL),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" in it", TextType.NORMAL)
        ]
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result, expected)
    
    def test_no_delimiters(self):
        
        node = TextNode("This has no special formatting", TextType.NORMAL)
        result = split_nodes([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This has no special formatting", TextType.NORMAL)
        ]
        
        self.assertEqual(len(result), 1)

        self.assertEqual(result[0], expected[0])
    
    def test_empty_string(self):
        
        node = TextNode("", TextType.NORMAL)
        result = split_nodes([node], "`", TextType.CODE)
        
        expected = [
        ]
        
        self.assertEqual(len(result), 0)
        self.assertEqual(result, expected)
    
    def test_only_delimiters(self):
        
        node = TextNode("``", TextType.NORMAL)
        result = split_nodes([node], "`", TextType.CODE)
        
        expected = []
        
        self.assertEqual(len(result), 0)
        self.assertEqual(result, expected)
    
    def test_delimiter_at_start(self):
        
        node = TextNode("`code` after", TextType.NORMAL)
        result = split_nodes([node], "`", TextType.CODE)
        
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" after", TextType.NORMAL)
        ]
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result, expected)
    
    def test_delimiter_at_end(self):
        
        node = TextNode("before `code`", TextType.NORMAL)
        result = split_nodes([node], "`", TextType.CODE)
        
        expected = [
            TextNode("before ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
        ]
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result, expected)
    
    def test_non_normal_text_type(self):
        
        node = TextNode("This is already `code`", TextType.BOLD)
        result = split_nodes([node], "`", TextType.CODE)
        
        
        expected = [
            TextNode("This is already `code`", TextType.BOLD)
        ]
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result, expected)
    
    def test_multiple_nodes(self):
        
        node1 = TextNode("First `code`", TextType.NORMAL)
        node2 = TextNode("Second *bold*", TextType.NORMAL)
        node3 = TextNode("Already formatted", TextType.ITALIC)
        
        
        result = split_nodes([node1, node2, node3], "`", TextType.CODE)
        
        expected = [
            TextNode("First ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode("Second *bold*", TextType.NORMAL),
            TextNode("Already formatted", TextType.ITALIC)
        ]
        
        self.assertEqual(len(result), 4)
        self.assertEqual(result, expected)
        
        
        result = split_nodes([node1, node2, node3], "*", TextType.BOLD)
        
        expected = [
            TextNode("First `code`", TextType.NORMAL),
            TextNode("Second ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode("Already formatted", TextType.ITALIC)
        ]
        
        self.assertEqual(len(result), 4)
        self.assertEqual(result, expected)
    
    def test_uneven_delimiters(self):
        
        node = TextNode("This has `unmatched delimiters", TextType.NORMAL)
        
        with self.assertRaises(Exception) as context:
            split_nodes([node], "`", TextType.CODE)
        
        self.assertTrue("invalid markdown, formatted section not closed" in str(context.exception))

    def test_nested_delimiters_not_supported(self):
        
        # Since the function doesn't support nesting, `a`b`c` would be split into:
        # NORMAL(""), CODE("a"), NORMAL("`b`c")
        node = TextNode("`a`b`c`", TextType.NORMAL)
        result = split_nodes([node], "`", TextType.CODE)
        
        expected = [
            TextNode("a", TextType.CODE),
            TextNode("b", TextType.NORMAL),
            TextNode("c", TextType.CODE),
        ]
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result, expected)
        
    def test_adjacent_delimiters(self):
        
        node = TextNode("Text ``double backticks`` end", TextType.NORMAL)
        result = split_nodes([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Text ", TextType.NORMAL),
            TextNode("double backticks", TextType.NORMAL),
            TextNode(" end", TextType.NORMAL)
        ]
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result, expected)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(

                [TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )],

            new_nodes,
        )

    def test_image_at_front_or_back(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(

                [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )],

            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(

                [TextNode("This is text with an ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                )],

            new_nodes,
        )

    def test_link_at_front_or_back(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(

                [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                )],

            new_nodes,
        )

    def test_no_link_or_image(self):
        node = TextNode("There is nothing here", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("There is nothing here", TextType.NORMAL)], new_nodes)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("There is nothing here", TextType.NORMAL)], new_nodes)

    def test_empty(self):
        new_nodes = split_nodes_image([])
        self.assertListEqual(new_nodes, [])
        new_nodes = split_nodes_link([])
        self.assertListEqual(new_nodes, [])

    def test_adjancent_and_same(self):
        node = TextNode("[link here](https://google.com)[link here](https://google.com)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("link here", TextType.LINK, "https://google.com"), 
                               TextNode("link here", TextType.LINK, "https://google.com")],new_nodes)


if __name__ == "__main__":
    unittest.main()