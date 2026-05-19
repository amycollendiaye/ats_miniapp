from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")


def inline_markdown(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    return text


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    in_code = False
    code_lines: list[str] = []
    list_stack: list[int] = []

    def close_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph.clear()

    def close_lists(target_indent: int = -1) -> None:
        while list_stack and list_stack[-1] >= target_indent:
            output.append("</ul>")
            list_stack.pop()

    for raw_line in lines:
        line = raw_line.rstrip()

        if line.startswith("```"):
            close_paragraph()
            close_lists()
            if in_code:
                output.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
                code_lines.clear()
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(raw_line)
            continue

        if not line.strip():
            close_paragraph()
            close_lists()
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            close_paragraph()
            close_lists()
            level = len(heading.group(1))
            output.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            continue

        bullet = re.match(r"^(\s*)[-*]\s+(.+)$", raw_line)
        if bullet:
            close_paragraph()
            indent = len(bullet.group(1))
            if not list_stack or indent > list_stack[-1]:
                output.append("<ul>")
                list_stack.append(indent)
            elif indent < list_stack[-1]:
                close_lists(indent + 1)
            output.append(f"<li>{inline_markdown(bullet.group(2))}</li>")
            continue

        numbered = re.match(r"^\s*\d+\.\s+(.+)$", raw_line)
        if numbered:
            close_paragraph()
            close_lists()
            output.append(f"<p class=\"numbered\">{inline_markdown(numbered.group(1))}</p>")
            continue

        paragraph.append(line.strip())

    close_paragraph()
    close_lists()
    if in_code:
        output.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
    return "\n".join(output)


def wrap_document(body: str, title: str) -> str:
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <style>
    @page {{ size: A4; margin: 18mm 16mm; }}
    * {{ box-sizing: border-box; }}
    body {{
      color: #17202a;
      font-family: "Segoe UI", Arial, sans-serif;
      font-size: 11pt;
      line-height: 1.55;
      margin: 0;
    }}
    h1 {{
      border-bottom: 2px solid #1f6feb;
      color: #0b2f5b;
      font-size: 25pt;
      margin: 0 0 18pt;
      padding-bottom: 10pt;
    }}
    h2 {{
      break-after: avoid;
      color: #124577;
      font-size: 17pt;
      margin: 24pt 0 8pt;
    }}
    h3 {{
      break-after: avoid;
      color: #1d5f8f;
      font-size: 13.5pt;
      margin: 18pt 0 6pt;
    }}
    h4, h5, h6 {{ break-after: avoid; color: #2a5b78; margin: 14pt 0 5pt; }}
    p {{ margin: 0 0 9pt; }}
    ul {{ margin: 0 0 9pt 18pt; padding: 0; }}
    li {{ margin: 0 0 4pt; }}
    code {{
      background: #f2f5f8;
      border: 1px solid #d8e0e8;
      border-radius: 3px;
      color: #223;
      font-family: Consolas, "Courier New", monospace;
      font-size: 9.5pt;
      padding: 0 3px;
    }}
    pre {{
      background: #f7f9fb;
      border: 1px solid #d8e0e8;
      border-radius: 6px;
      break-inside: avoid;
      margin: 10pt 0 12pt;
      overflow-wrap: anywhere;
      padding: 10pt;
      white-space: pre-wrap;
    }}
    pre code {{ background: transparent; border: 0; padding: 0; }}
    .numbered {{
      margin-left: 14pt;
      position: relative;
    }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


def main() -> int:
    source = ROOT / "DOCUMENTATION_TECHNIQUE_FR.md"
    html_output = ROOT / "DOCUMENTATION_TECHNIQUE_FR.html"
    pdf_output = ROOT / "DOCUMENTATION_TECHNIQUE_FR.pdf"
    user_data = ROOT / ".edge-pdf-profile"

    html_output.write_text(
        wrap_document(markdown_to_html(source.read_text(encoding="utf-8")), "Documentation technique - TCMPP Boilerplate"),
        encoding="utf-8",
    )

    if not EDGE.exists():
        print(f"Microsoft Edge introuvable: {EDGE}", file=sys.stderr)
        return 1

    subprocess.run(
        [
            str(EDGE),
            "--headless=new",
            "--disable-gpu",
            f"--user-data-dir={user_data}",
            f"--print-to-pdf={pdf_output}",
            str(html_output.resolve().as_uri()),
        ],
        check=True,
    )
    print(pdf_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
