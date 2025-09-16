import unittest
from markdown_to_blocks import markdown_to_blocks, BlockType, detect_block_type

class TestMarkdownToBlocks(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
        def test_markdown_empty(self):
             md = ""
             blocks = markdown_to_blocks(md)
             self.assertEqual(blocks, [])

        def test_markdown_to_blocks_newlines(self):
            md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )


class TestBlockTypeDetection(unittest.TestCase):
    def test_heading_blocks(self):
        self.assertEqual(detect_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(detect_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(detect_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(detect_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(detect_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(detect_block_type("###### Heading 6"), BlockType.HEADING)
        
        self.assertEqual(detect_block_type("# Heading with numbers 123!"), BlockType.HEADING)
        self.assertEqual(detect_block_type("## Another heading-with-dashes"), BlockType.HEADING)
        
        self.assertEqual(detect_block_type("# "), BlockType.HEADING)
        
        self.assertEqual(detect_block_type("#No space after hash"), BlockType.PARAGRAPH)
        self.assertEqual(detect_block_type("####### Too many hashes"), BlockType.PARAGRAPH)
        self.assertEqual(detect_block_type(" # Space before hash"), BlockType.PARAGRAPH)
    
    def test_code_blocks(self):
        code_block = "```\nprint('hello')\n```"
        self.assertEqual(detect_block_type(code_block), BlockType.CODE)
        
        code_block_with_lang = "```python\nprint('hello')\nprint('world')\n```"
        self.assertEqual(detect_block_type(code_block_with_lang), BlockType.CODE)
        
        empty_code_block = "```\n```"
        self.assertEqual(detect_block_type(empty_code_block), BlockType.CODE)
        
        self.assertEqual(detect_block_type("```"), BlockType.PARAGRAPH)
        
        self.assertEqual(detect_block_type("``code``"), BlockType.PARAGRAPH)
        self.assertEqual(detect_block_type("```no closing"), BlockType.PARAGRAPH)
    
    def test_quote_blocks(self):
        self.assertEqual(detect_block_type("> This is a quote"), BlockType.QUOTE)
        
        multi_quote = "> This is line 1\n> This is line 2\n> This is line 3"
        self.assertEqual(detect_block_type(multi_quote), BlockType.QUOTE)
        
        quote_with_empty = "> Line 1\n>\n> Line 3"
        self.assertEqual(detect_block_type(quote_with_empty), BlockType.QUOTE)
        
        invalid_quote = "> First line\nSecond line without >"
        self.assertEqual(detect_block_type(invalid_quote), BlockType.PARAGRAPH)
        
        self.assertEqual(detect_block_type(">No space"), BlockType.QUOTE)
    
    def test_unordered_list_blocks(self):
        self.assertEqual(detect_block_type("- Item 1"), BlockType.UNORDERED_LIST)
        
        multi_list = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(detect_block_type(multi_list), BlockType.UNORDERED_LIST)
        
        long_list = "- This is a longer list item with more text\n- Another item"
        self.assertEqual(detect_block_type(long_list), BlockType.UNORDERED_LIST)
        
        invalid_list = "- Item 1\nItem 2 without dash"
        self.assertEqual(detect_block_type(invalid_list), BlockType.PARAGRAPH)
        
        self.assertEqual(detect_block_type("-No space"), BlockType.PARAGRAPH)
    
    def test_ordered_list_blocks(self):
        self.assertEqual(detect_block_type("1. First item"), BlockType.ORDERED_LIST)
        
        ordered_list = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(detect_block_type(ordered_list), BlockType.ORDERED_LIST)
        
        long_ordered = "1. Item one\n2. Item two\n3. Item three\n4. Item four\n5. Item five"
        self.assertEqual(detect_block_type(long_ordered), BlockType.ORDERED_LIST)
        
        wrong_start = "2. Second item\n3. Third item"
        self.assertEqual(detect_block_type(wrong_start), BlockType.PARAGRAPH)
        
        skip_numbers = "1. First\n3. Third"
        self.assertEqual(detect_block_type(skip_numbers), BlockType.PARAGRAPH)
        
        mixed_invalid = "1. First item\nNot numbered\n2. Second item"
        self.assertEqual(detect_block_type(mixed_invalid), BlockType.PARAGRAPH)
        
        self.assertEqual(detect_block_type("1.No space"), BlockType.PARAGRAPH)
        
        multi_digit = "1. First\n2. Second\n10. Tenth\n11. Eleventh"
        self.assertEqual(detect_block_type(multi_digit), BlockType.PARAGRAPH)
    
    def test_paragraph_blocks(self):
        self.assertEqual(detect_block_type("This is a simple paragraph."), BlockType.PARAGRAPH)
        
        multi_para = "This is line 1 of paragraph.\nThis is line 2 of paragraph."
        self.assertEqual(detect_block_type(multi_para), BlockType.PARAGRAPH)
        
        special_para = "This paragraph has special chars: !@#$%^&*()"
        self.assertEqual(detect_block_type(special_para), BlockType.PARAGRAPH)
        
        self.assertEqual(detect_block_type(""), BlockType.PARAGRAPH)
        
        self.assertEqual(detect_block_type("123456"), BlockType.PARAGRAPH)
        
        mixed = "Some text\n# But this looks like heading\nBut it's mixed"
        self.assertEqual(detect_block_type(mixed), BlockType.PARAGRAPH)
    
    def test_edge_cases(self):
        self.assertEqual(detect_block_type("#"), BlockType.PARAGRAPH)
        self.assertEqual(detect_block_type(">"), BlockType.QUOTE)
        self.assertEqual(detect_block_type("-"), BlockType.PARAGRAPH)
        
        self.assertEqual(detect_block_type("1"), BlockType.PARAGRAPH)
        self.assertEqual(detect_block_type("1."), BlockType.PARAGRAPH)
        
        self.assertEqual(detect_block_type("# Heading"), BlockType.HEADING)
        
        long_heading = "# " + "A" * 1000
        self.assertEqual(detect_block_type(long_heading), BlockType.HEADING)


if __name__ == "__main__":
    unittest.main()