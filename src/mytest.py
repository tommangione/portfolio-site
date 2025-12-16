from htmlnode import ParentNode, LeafNode

block = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""

lines = block.splitlines()
code_text = "\n".join(lines[1:-1]) + "\n"
code_node = LeafNode("code", code_text)
print(ParentNode("pre", [code_node]).to_html())
