import unittest

from block_splitters import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        # Heading tests
        assert block_to_block_type("# Heading 1") == BlockType.HEADING
        assert block_to_block_type("## Heading 2") == BlockType.HEADING
        assert block_to_block_type("###### Heading 6") == BlockType.HEADING
        # Edge case: More than 6 # should be paragraph
        assert block_to_block_type("####### Not a heading") == BlockType.PARAGRAPH
        # Edge case: No space after # should be paragraph
        assert block_to_block_type("#Not a heading") == BlockType.PARAGRAPH

        # Code block tests
        assert block_to_block_type("```\ncode block\n```") == BlockType.CODE
        assert block_to_block_type("```python\ndef hello():\n    print('world')\n```") == BlockType.CODE
        # Edge case: Missing closing backticks
        assert block_to_block_type("```\ncode without closing") == BlockType.PARAGRAPH

        # Quote tests
        assert block_to_block_type(">This is a quote") == BlockType.QUOTE
        assert block_to_block_type(">Line 1\n>Line 2") == BlockType.QUOTE
        # Edge case: Not every line starts with >
        assert block_to_block_type(">Line 1\nLine 2") == BlockType.PARAGRAPH

        # Unordered list tests
        assert block_to_block_type("- Item 1") == BlockType.UNORDERED_LIST
        assert block_to_block_type("- Item 1\n- Item 2\n- Item 3") == BlockType.UNORDERED_LIST
        # Edge case: Not every line starts with -
        assert block_to_block_type("- Item 1\nText") == BlockType.PARAGRAPH
        # Edge case: No space after -
        assert block_to_block_type("-Item 1")

        # Basic ordered list
        assert block_to_block_type("1. Item 1") == BlockType.ORDERED_LIST
        
        # Multi-item ordered list
        assert block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3") == BlockType.ORDERED_LIST
        
        # Edge case: Correctly numbered but missing space
        assert block_to_block_type("1.Item 1\n2.Item 2") == BlockType.PARAGRAPH
        
        # Edge case: Not properly incremented
        assert block_to_block_type("1. Item 1\n3. Item 2") == BlockType.PARAGRAPH
        
        # Edge case: Not starting with 1
        assert block_to_block_type("2. Item 1\n3. Item 2") == BlockType.PARAGRAPH
        
        # Edge case: Mixed content
        assert block_to_block_type("1. Item 1\nNormal text") == BlockType.PARAGRAPH
        
        # Edge case: Longer ordered list
        assert block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3\n4. Item 4\n5. Item 5") == BlockType.ORDERED_LIST
if __name__ == "__main__":
    unittest.main()
