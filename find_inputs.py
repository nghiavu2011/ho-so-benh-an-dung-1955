with open("body_html.txt", "r", encoding="utf-8") as f:
    html = f.read()

import re
inputs = re.findall(r"<input[^>]*>", html)
print("Found inputs:")
for inp in inputs:
    print(inp)

semantics = re.findall(r"<flt-semantics[^>]*>", html)
print(f"\nFound {len(semantics)} flt-semantics tags.")
for sem in semantics[:20]:
    print(sem[:200])
