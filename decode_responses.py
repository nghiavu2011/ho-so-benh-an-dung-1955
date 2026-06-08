import json, binascii

with open(r"D:\\antigravity_scratch\\real_estate_scoring\\sql\\Ho So Benh An Dung 1955\\captured_responses.json", "r", encoding="utf-8") as f:
    data = json.load(f)

summary = []
for entry in data:
    url = entry.get("url", "")
    body_hex = entry.get("body", "")
    try:
        body_bytes = binascii.unhexlify(body_hex)
        # Try utf-8 decode, replace errors
        body_text = body_bytes.decode("utf-8", errors='replace')
    except Exception as e:
        body_text = f"[decode error: {e}]"
    summary.append({"url": url, "preview": body_text[:200]})

# Write summary to artifact
with open(r"C:\\Users\\NMteam\\.gemini\\antigravity\\brain\\be399287-a6e0-4d98-a2d1-0882a3d79cea\\extracted_summary.md", "w", encoding="utf-8") as out:
    out.write("# Extracted API Response Preview\n\n")
    for s in summary:
        out.write(f"## URL: {s['url']}\n\n")
        out.write(f"```
{s['preview']}
```\n\n")

print("Extraction complete, preview saved.")
