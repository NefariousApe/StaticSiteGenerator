from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def is_quote_block(block):
    for line in block.split("\n"):
        if not line.startswith(">"):
            return False
    return True

def is_unordered_list(block):
    for line in block.split("\n"):
        if not line.startswith("- "):
            return False
    return True

def is_ordered_list(block):
    num = 1
    for line in block.split("\n"):
        if not line.startswith(f"{num}. "):
            return False
        num += 1
    return True

def detect_block_type(markdown_block):
    match markdown_block:
        case s if re.match(r"^#{1,6} ", s):
            return BlockType.HEADING
        case s if s.startswith("```") and s.endswith("```") and len(s) >= 6:
            return BlockType.CODE
        case s if is_quote_block(s):
            return BlockType.QUOTE
        case s if is_unordered_list(s):
            return BlockType.UNORDERED_LIST
        case s if is_ordered_list(s):
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH



def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        block = block.strip()
        if block:
            cleaned_blocks.append(block)
    return cleaned_blocks


def main():
   block = "1. First\n2. Second\n3. Third"
   print(detect_block_type(block))

if __name__ == "__main__":
    main()