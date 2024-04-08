from enum import Enum

class BlockType(Enum):
    heading = '#'
    paragraph = ''
    code = '```'
    quote = '>'
    unordered_list_asterisk = '*'
    unordered_list_dash = '-'
    ordered_list = '.'
    unordered_list = '*-'

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [x.strip() for x in blocks]
    return blocks

def block_to_block_type(block):
    first_char = block[0]
    
    if first_char == BlockType.heading.value:
        return BlockType.heading.name
    elif first_char == BlockType.quote.value:
        return BlockType.quote.name
    elif first_char == BlockType.unordered_list_asterisk.value:
        return BlockType.unordered_list.name
    elif first_char == BlockType.unordered_list_dash.value:
        return BlockType.unordered_list.name
    
    # check if it is code block
    if len(block) < len(2 * BlockType.code.value):
        if block[:3] == block[-3:] and block[:3] == BlockType.code.value:
            return BlockType.code.name
        
    second_char = block[1]
    lines = block.split('\n')

    if second_char == BlockType.ordered_list.value and first_char == '1':
        for i, line in enumerate(lines, start=1):
            if line[0] != str(i) or line[1] != BlockType.ordered_list.value:
                return BlockType.paragraph.name
        return BlockType.ordered_list.name
    else:
        return BlockType.paragraph.name
            