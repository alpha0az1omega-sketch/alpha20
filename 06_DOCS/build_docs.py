#!/usr/bin/env python3
"""Converts whitepaper.md to a styled, self-contained HTML file."""
import re
from pathlib import Path

def md_to_html(md_text):
    html = []
    in_code = False
    in_list = False
    
    for line in md_text.splitlines():
        # Gestion des blocs de code
        if line.strip().startswith("```"):
            in_code = not in_code
            if in_code:
                html.append("<pre><code>")
            else:
                html.append("</code></pre>")
            continue
            
        if in_code:
            html.append(line.replace("<", "&lt;").replace(">", "&gt;"))
            continue

        # Gestion des listes
        if line.startswith("- "):
            if not in_list:
                html.append("<ul>")
                in_list = True
            content = line[2:]
            # Gras dans les listes
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            html.append(f"<li>{content}</li>")
            continue
        else:
            if in_list:
                html.append("</ul>")
                in_list = False

        # Gras inline
        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)

        # Titres
        if line.startswith("# "):
            html.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            html.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("### "):
            html.append(f"<h3>{line[4:]}</h3>")
        elif line.strip() == "---":
            html.append("<hr/>")
        elif line.strip() == "":
            continue
        else:
            html.append(f"<p>{line}</p>")
            
    if in_list:
        html.append("</ul>")
        
    return "\n".join(html)

def main():
    src = Path("06_DOCS/whitepaper.md")
    dst = Path("06_DOCS/whitepaper.html")
    md = src.read_text()
    body = md_to_html(md)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ALPHA-20 Whitepaper</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 0 20px; color: #333; }}
h1 {{ border-bottom: 2px solid #eaeaea; padding-bottom: 10px; font-size: 2em; }}
h2 {{ border-bottom: 1px solid #eaeaea; padding-bottom: 5px; margin-top: 30px; font-size: 1.5em; }}
h3 {{ font-size: 1.2em; margin-top: 20px; }}
code {{ background: #f5f5f5; padding: 2px 4px; border-radius: 4px; font-family: monospace; font-size: 0.9em; }}
pre {{ background: #f5f5f5; padding: 15px; border-radius: 6px; overflow-x: auto; }}
ul {{ padding-left: 20px; }}
li {{ margin-bottom: 8px; }}
hr {{ border: 0; border-top: 1px solid #eaeaea; margin: 30px 0; }}
strong {{ color: #111; }}
</style>
</head>
<body>
{body}
</body>
</html>"""
    dst.write_text(html)
    print(f"wrote {dst} ({dst.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
