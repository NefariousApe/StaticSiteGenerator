from markdown_to_blocks import detect_block_type, markdown_to_blocks, BlockType
from htmlnode import ParentNode, LeafNode, HTMLNode
from markdown_to_nodes import text_to_nodes
from textnode import TextNode, TextType
import re
            
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_children = []
    
    for block in blocks:
        block_type = detect_block_type(block)
        html_node = convert_block_to_html(block, block_type)
        html_children.append(html_node)
    
    return ParentNode("div", html_children, None)


def convert_block_to_html(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return create_paragraph_node(block)
        case BlockType.HEADING:
            return create_heading_node(block)
        case BlockType.CODE:
            return create_code_node(block)
        case BlockType.ORDERED_LIST:
            return create_ordered_list_node(block)
        case BlockType.UNORDERED_LIST:
            return create_unordered_list_node(block)
        case BlockType.QUOTE:
            return create_quote_node(block)
        case _:
            raise ValueError(f"Unsupported block type: {block_type}")

def create_paragraph_node(block):
    paragraph_text = " ".join(line.strip() for line in block.split("\n"))
    children = text_to_children(paragraph_text)
    return ParentNode("p", children)


def create_heading_node(block):
    heading_match = re.match(r'^(#{1,6})\s+(.+)', block)
    if not heading_match:
        raise ValueError("Invalid heading format")
    
    level = len(heading_match.group(1))
    heading_text = heading_match.group(2).strip()
    children = text_to_children(heading_text)
    return ParentNode(f"h{level}", children)


def create_code_node(block):
    lines = block.split("\n")
    if len(lines) < 2 or not lines[0].startswith("```") or not lines[-1].strip() == "```":
        raise ValueError("Invalid code block format")
    
    code_content = "\n".join(lines[1:-1])
    code_text_node = TextNode(code_content, TextType.NORMAL)
    code_element = ParentNode("code", [code_text_node.text_node_to_html_node()])
    return ParentNode("pre", [code_element])


def create_ordered_list_node(block):
    lines = block.split("\n")
    list_items = []
    
    for i, line in enumerate(lines, 1):
        item_match = re.match(rf'^{i}\.\s+(.+)', line)
        if not item_match:
            raise ValueError(f"Invalid ordered list item format at line {i}")
        
        item_text = item_match.group(1)
        item_children = text_to_children(item_text)
        list_items.append(ParentNode("li", item_children))
    
    return ParentNode("ol", list_items)


def create_unordered_list_node(block):
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        if not line.startswith("- "):
            raise ValueError("Invalid unordered list item format")
        
        item_text = line[2:].strip()
        item_children = text_to_children(item_text)
        list_items.append(ParentNode("li", item_children))
    
    return ParentNode("ul", list_items)


def create_quote_node(block):
    lines = block.split("\n")
    quote_lines = []
    
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block format")
        clean_line = re.sub(r'^>\s?', '', line)
        quote_lines.append(clean_line)
    
    quote_text = " ".join(quote_lines)
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)


def markdown_to_blocks(markdown):   
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def text_to_children(text):
    text_nodes = text_to_nodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node.text_node_to_html_node()
        children.append(html_node)
    return children




def main():
#     md = """
# This is **bolded** paragraph
# text in a p
# tag here

# This is another paragraph with _italic_ text and `code` here

# """
#     md = """
# > This is a
# > blockquote block

# this is paragraph text

# """
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
    # node = markdown_to_html(md)
    # html = node.to_html()
    # print(html)

if __name__ == "__main__":
    main()