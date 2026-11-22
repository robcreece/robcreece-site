"""Renders freebies.json into: web page body, print/PDF/Google-Doc HTML."""
import html, json
from pathlib import Path

e = html.escape
DATA = json.loads((Path(__file__).parent / "freebies.json").read_text())


def _nl(s):
    return e(s).replace("\n", "<br>")


def content_html(slug):
    d = DATA[slug]
    out = []
    out.append(f'<p class="sub">{e(d["subtitle"])}</p>')
    out += [f"<p>{e(p)}</p>" for p in d["intro"]]

    if "items" in d:
        for i, t in enumerate(d["items"], 1):
            ba = ""
            if t.get("before") and t.get("after"):
                ba = f'<div class="ba"><div class="b"><span>Before</span>{_nl(t["before"])}</div><div class="a"><span>After</span>{_nl(t["after"])}</div></div>'
            out.append(f'<div class="item"><h2><span class="n">{i:02d}</span> {e(t["name"])}</h2><p>{e(t["text"])}</p>{ba}</div>')
    elif slug == "robot-tells":
        for i, t in enumerate(d["tells"], 1):
            out.append(f'''<div class="item"><h2><span class="n">{i:02d}</span> {e(t["name"])}</h2>
<p><b>How to spot it:</b> {e(t["spot"])}</p>
<p><b>30-second fix:</b> {e(t["fix"])}</p>
<div class="ba"><div class="b"><span>Before</span>{_nl(t["before"])}</div><div class="a"><span>After</span>{_nl(t["after"])}</div></div></div>''')
        out.append(f'<h2>{e(d["routine_title"])}</h2><ol class="steps">' + "".join(f"<li>{e(r)}</li>" for r in d["routine"]) + "</ol>")
        out.append(f'<h2>{e(d["score_title"])}</h2><p>{e(d["score"])}</p>')
    if "prompt_block" in d:
        out.append(f'<h2>{e(d["prompt_block"]["title"])}</h2><p>{e(d["prompt_block"]["intro"])}</p><pre class="promptbox" id="pb">{e(d["prompt_block"]["prompt"])}</pre><p><button class="btn" onclick="navigator.clipboard.writeText(document.getElementById(\'pb\').innerText);this.textContent=\'Copied\'">Copy the prompt</button></p>')
    elif "groups" in d:
        for g in d["groups"]:
            chips = "".join(f'<span class="chip">{e(w)}</span>' for w in g["words"])
            out.append(f'''<div class="item"><h2>{e(g["name"])}</h2>
<p>{e(g["job"])}</p><p class="chips">{chips}</p>
<div class="ba"><div class="b"><span>Weak</span>{e(g["weak"])}</div><div class="a"><span>Stronger</span>{e(g["strong"])}</div></div></div>''')
        out.append(f'<h2>{e(d["cut_title"])}</h2><p>{e(d["cut_intro"])}</p><ul class="cut">' + "".join(f'<li><b>{e(c["word"])}</b>: {e(c["why"])}</li>' for c in d["cut"]) + "</ul>")
        out.append(f'<h2>{e(d["placement_title"])}</h2><table>' + "".join(f'<tr><td><b>{e(p["where"])}</b></td><td>{e(p["use"])}</td></tr>' for p in d["placement"]) + "</table>")
        out.append(f'<h2>{e(d["prompt_title"])}</h2><p class="prompt">{e(d["prompt"])}</p>')

    out.append(f'<p class="closer">{e(d["closer"])}</p>')
    out.append('<p class="foot">By Rob Reece &middot; robcreece.com &middot; CultLike Marketing</p>')
    return "\n".join(out)


def web_body(slug, pdf_url):
    d = DATA[slug]
    return f'''<section class="res"><div class="wrap narrow">
<span class="mono">Free resource</span>
<h1>{e(d["title"])}</h1>
{content_html(slug)}
{('<p style="margin-top:34px"><a class="btn" href="' + e(pdf_url) + '">Download the PDF</a></p>') if pdf_url else ""}
{('<p style="margin-top:20px"><a class="btn ghost" href="' + e(d["cta"]["url"]) + '">' + e(d["cta"]["label"]) + '</a></p>') if d.get("cta") else ""}
</div></section>'''


PRINT_CSS = """
@page{size:Letter;margin:0.7in}
*{box-sizing:border-box}
body{font-family:Arial,Helvetica,sans-serif;color:#1a1a1a;font-size:11.5pt;line-height:1.5;margin:0}
h1{font-size:30pt;margin:0 0 4pt;letter-spacing:.5pt;text-transform:uppercase;border-bottom:4px solid #c9a24b;padding-bottom:8pt}
h2{font-size:14pt;margin:16pt 0 4pt;color:#0e0e0e;page-break-after:avoid}
.n{background:#0e0e0e;color:#c9a24b;padding:1pt 6pt;font-size:11pt;margin-right:4pt}
.sub{font-size:13pt;color:#555;margin:6pt 0 12pt}
.item{page-break-inside:avoid;margin-bottom:8pt}
.ba{display:flex;gap:8pt;margin:6pt 0}
.ba>div{flex:1;padding:7pt 9pt;font-size:10.5pt}
.ba span{display:block;font-size:8pt;text-transform:uppercase;letter-spacing:1pt;font-weight:bold;margin-bottom:2pt}
.b{background:#f5e6e6;border-left:3px solid #b03a3a}
.a{background:#e6f1e6;border-left:3px solid #2e7d32}
.chip{display:inline-block;background:#f2ede2;border:1px solid #c9a24b;padding:1pt 7pt;margin:2pt 3pt 2pt 0;font-size:10.5pt}
table{border-collapse:collapse;width:100%}td{border-bottom:1px solid #ddd;padding:5pt 6pt;vertical-align:top}
.prompt{background:#f2ede2;border-left:4px solid #c9a24b;padding:9pt 11pt;font-family:'Courier New',monospace;font-size:10pt}
.promptbox{white-space:pre-wrap;background:#f2ede2;border-left:4px solid #c9a24b;padding:9pt 11pt;font-family:'Courier New',monospace;font-size:9.5pt}
.closer{font-weight:bold;margin-top:16pt}
.foot{color:#777;font-size:9.5pt;margin-top:20pt;border-top:1px solid #ddd;padding-top:8pt}
.steps li,.cut li{margin-bottom:3pt}
"""


def print_html(slug):
    d = DATA[slug]
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>{e(d["title"])}</title><style>{PRINT_CSS}</style></head><body><h1>{e(d["title"])}</h1>{content_html(slug)}</body></html>'
