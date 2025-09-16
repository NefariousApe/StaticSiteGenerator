import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_init_with_args(self):
        node = HTMLNode("p", "Hello", [1, 2], {"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [1, 2])
        self.assertEqual(node.props, {"class": "text"})

    def test_init_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_props_to_html_single(self):
        node = HTMLNode(props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(props={"class": "main", "id": "section1"})
        html = node.props_to_html()
        self.assertIn(' class="main"', html)
        self.assertIn(' id="section1"', html)

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_repr_output(self):
        node = HTMLNode("div", "content", [], {"class": "box"})
        expected = 'Tag: div\nValue=content\nChildren: []\nProps:  class="box"'
        self.assertEqual(repr(node), expected)

class TestLeafNode(unittest.TestCase):
    def test_init_with_args(self):
        node = LeafNode("p","Hello World",{"href": "https://www.google.com"})
        self.assertEqual(node.value, "Hello World")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"href": "https://www.google.com"})

    def test_init_defaults(self):
        node = LeafNode(None, None)
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

class TestParentNode(unittest.TestCase):
    def test_leaf_node_to_html_with_tag(self):
        node = LeafNode("p", "Hello World", {"class": "text"})
        expected = '<p class="text">Hello World</p>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_node_to_html_without_tag(self):
        node = LeafNode(None, "Plain text")
        expected = "Plain text"
        self.assertEqual(node.to_html(), expected)

    def test_leaf_node_raises_without_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_to_html_single_child(self):
        child = LeafNode("span", "child text")
        parent = ParentNode("div", [child])
        expected = "<div><span>child text</span></div>"
        self.assertEqual(parent.to_html(), expected)

    def test_parent_node_to_html_nested_children(self):
        grandchild = LeafNode("b", "bold text")
        child = ParentNode("p", [grandchild])
        parent = ParentNode("div", [child])
        expected = "<div><p><b>bold text</b></p></div>"
        self.assertEqual(parent.to_html(), expected)

    def test_parent_node_raises_missing_tag(self):
        child = LeafNode("span", "child text")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parent_node_raises_missing_children(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parent_node_raises_empty_children(self):
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parent_node_with_props(self):
        child = LeafNode("span", "child text")
        parent = ParentNode("div", [child], {"id": "container", "class": "wrapper"})
        html = parent.to_html()
        self.assertIn('<div id="container" class="wrapper">', html)
        self.assertTrue(html.endswith("</div>"))
if __name__ == "__main__":
    unittest.main()