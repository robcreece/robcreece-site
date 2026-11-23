#!/usr/bin/env python3
"""Static site generator for robcreece.com. Reads pages.json, writes dist/."""
import json, shutil, html, sys
from pathlib import Path

root = Path(__file__).parent
cfg = json.loads((root / "pages.json").read_text())
site = cfg["site"]
magnets = [m for m in cfg["magnets"] if not m.get("hidden")]  # set "hidden": true in pages.json to pull a magnet offline
dist = root / "dist"
if dist.exists():
    shutil.rmtree(dist)
(dist / "assets").mkdir(parents=True)
shutil.copy(root / "assets/style.css", dist / "assets/style.css")
shutil.copy(root / "assets/rob.jpg", dist / "assets/rob.jpg")

e = html.escape

def layout(title, desc, body, path, noindex=False):
    robots = '<meta name="robots" content="noindex,nofollow">' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">{robots}
<link rel="canonical" href="{site['domain']}{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Space+Grotesk:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
<script async src="{site['emailit_script']}"></script>
</head><body>
<nav><div class="wrap"><a class="logo" href="/">{e(site['name'])}</a><div><a class="link" href="/#pain">The problem</a><a class="link" href="/#fix">The fix</a><a class="link" href="/#free">Free stuff</a></div></div></nav>
{body}
<footer><div class="wrap"><span>&copy; 2026 5 Solas Marketing. Rob Reece.</span><span><a href="{site['cultlike_url']}">CultLike Marketing</a></span></div></footer>
</body></html>"""

def form_block(m):
    if m["form_token"]:
        return f'<div data-emailit-form="{m["form_token"]}"></div>'
    return '<p><strong>Form coming soon.</strong></p>'

# ---------- hub ----------
from urllib.parse import quote
offers = cfg.get("offers", [])
offer_section = ""
if offers:
    o0 = offers[0]
    offer_section = f'''<section id="build"><div class="wrap narrow"><span class="mono">Build your own</span><h2>Want a site like this one?</h2><p style="color:#cfcabb;max-width:620px">I built this site, its free tools and the signup flow in one chat with Claude. I packaged the process so you can do the same.</p><p style="margin-top:24px"><a class="btn" href="/{o0["slug"]}/">See the {e(o0["title"])}</a></p></div></section>'''

h = cfg["hub"]
pains = "".join(f'<div class="pain">{p}</div>' for p in h["pains"])
fixes = "".join(f'<div class="card"><h3>{c["title"]}</h3><p>{c["text"]}</p></div>' for c in h["fix_cards"])
about_paras = "".join(f'<p style="margin-top:14px">{p}</p>' for p in h["about"])

cards = "".join(
    f'<a class="card" href="/{m["slug"]}/" style="text-decoration:none"><span class="mono">{e(m["tag"])}</span><h3>{e(m["title"])}</h3><p>{e(m["card_blurb"])}</p><span class="mono">Get it free →</span></a>'
    for m in magnets)

bc_links = "".join(f'<li><a href="/{m["slug"]}/"><span>{e(m["title"])}</span><span class="mono">Free →</span></a></li>' for m in magnets)

hub = f"""
<section class="hero"><div class="wrap herogrid">
<div>
<span class="mono">{h["eyebrow"]}</span>
<h1>{h["headline"]}</h1>
<p class="lead">{h["lead"]}</p>
<a class="btn" href="#free">Grab the free tools</a> &nbsp; <a class="btn ghost" href="#pain">See if this is you</a>
</div>
<aside class="bizcard">
<img src="/assets/rob.jpg" alt="{h["photo_alt"]}" width="1000" height="800">
<div class="bc-body">
<h3>{site["name"]}</h3>
<p class="mono">{h["card_role"]}</p>
<p class="bc-line">{h["card_line"]}</p>
<ul class="bc-links">
{bc_links}
</ul>
<a class="bc-cult" href="{site['cultlike_url']}">{h["brand_link_label"]} →</a>
</div>
</aside>
</div></section>

<section id="pain"><div class="wrap narrow">
<span class="mono">{h["pain_eyebrow"]}</span>
<h2>{h["pain_title"]}</h2>
{pains}
<p style="margin-top:24px;color:#cfcabb">{h["pain_close"]}</p>
</div></section>

<section id="fix"><div class="wrap">
<span class="mono">The fix</span>
<h2>{h["fix_title"]}</h2>
<div class="grid">{fixes}</div>
<p style="margin-top:30px"><a class="btn" href="{site['cultlike_url']}">{h["fix_button"]}</a></p>
</div></section>

<section id="free"><div class="wrap">
<span class="mono">Start here</span>
<h2>{h["free_title"]}</h2>
<p style="color:#cfcabb;max-width:620px">{h["free_sub"]}</p>
<div class="grid">{cards}</div>
</div></section>

{offer_section}
<section id="about"><div class="wrap aboutgrid">
<img src="/assets/rob.jpg" alt="{site["name"]}" loading="lazy" width="1000" height="800">
<div>
<span class="mono">About</span>
<h2>{h["about_title"]}</h2>
{about_paras}
<p style="margin-top:24px"><a class="btn" href="#free">Start with a free tool</a></p>
</div>
</div></section>
"""
(dist / "index.html").write_text(layout("Rob Reece | Get your first online sale", "Simple offers, honest copy, and organic traffic for broke beginners seeking their first online sale.", hub, "/"))

# ---------- magnets + thank-you ----------
for m in magnets:
    bl = "".join(f"<li>{e(b)}</li>" for b in m["bullets"])
    body = f"""<section class="hero squeeze"><div class="wrap herogrid">
<div><span class="mono">{e(m['tag'])}</span>
<h1>{e(m['headline'])}</h1>
<p class="lead">{e(m['sub'])}</p>
<ul class="bullets">{bl}</ul></div>
<div><div class="cover"><span class="mono">{e(m['tag'])}</span><strong>{e(m['title'])}</strong><em>by Rob Reece</em></div>
<div class="formbox"><span class="mono">{e(m['cta'])}</span>{form_block(m)}</div>
<p style="margin-top:12px;color:var(--mute);font-size:14px">No spam. Unsubscribe any time.</p></div>
</div></section>"""
    d = dist / m["slug"]; d.mkdir()
    (d / "index.html").write_text(layout(f"{m['title']} | Rob Reece", m["sub"], body, f"/{m['slug']}/"))

    deliver = f'<p><a class="btn" href="{e(m["delivery_url"])}">{e(m["delivery_label"])}</a></p>' if m["delivery_url"] else ""
    nxt = f'<p style="margin-top:18px"><a class="btn ghost" href="{e(m["next_url"])}">{e(m["next_label"])}</a></p>' if m.get("next_url") and m["next_url"] != "#" else ""
    tbody = f"""<section class="thanks"><div class="wrap narrow">
<span class="mono">You're in</span>
<h1>{e(m['thanks_headline'])}</h1>
<p class="lead" style="margin:20px 0">{e(m['thanks_body'])}</p>
{deliver}{nxt}
</div></section>"""
    t = dist / "thanks" / m["slug"]; t.mkdir(parents=True)
    (t / "index.html").write_text(layout(f"Thank you | {m['title']}", "Thanks for signing up.", tbody, f"/thanks/{m['slug']}/", noindex=True))

# ---------- freebie resource pages + PDFs ----------
import freebies
(dist / "downloads").mkdir(exist_ok=True)
for pdf in (root / "assets/downloads").glob("*.pdf"):
    shutil.copy(pdf, dist / "downloads" / pdf.name)
for slug in freebies.DATA:
    d = dist / "r" / slug; d.mkdir(parents=True)
    ttl = freebies.DATA[slug]["title"]
    (d / "index.html").write_text(layout(f"{ttl} | Rob Reece", freebies.DATA[slug]["subtitle"], freebies.web_body(slug, f"/downloads/{slug}.pdf" if (root / "assets/downloads" / f"{slug}.pdf").exists() else None), f"/r/{slug}/", noindex=True))

# ---------- paid offers: sales pages + welcome (delivery) pages ----------
L = root / "launchpad" / "rendered"
def rd(n): return (L / n).read_text()
def prompt_box(txt, pid):
    return f'<pre class="promptbox" id="{pid}">{e(txt)}</pre><p><button class="btn" onclick="navigator.clipboard.writeText(document.getElementById(\'{pid}\').innerText);this.textContent=\'Copied\'">Copy the prompt</button></p>'
for o in offers:
    ret = f"{site.get('checkout_return_base', site['domain'])}/welcome/{o['welcome_token']}/"
    buy = f"https://checkout.dodopayments.com/buy/{o['product_id']}?quantity=1&redirect_url={quote(ret, safe='')}"
    bd = root / "dist" / "buy" / o["slug"]; bd.mkdir(parents=True, exist_ok=True)
    (bd / "index.html").write_text(f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><title>Redirecting to checkout</title><meta http-equiv="refresh" content="0;url={e(buy)}"><p>Taking you to checkout... <a href="{e(buy)}">Continue</a></p><script>location.replace({json.dumps(buy)})</script>')
    inc = "".join(f"<li>{e(x)}</li>" for x in o["includes"])
    needs = "".join(f"<li>{e(x)}</li>" for x in o["needs"])
    notf = "".join(f"<li>{e(x)}</li>" for x in o["not_for"])
    vid = o.get("video_url", "")
    if vid:
        vsl = f'<div class="vsl"><video controls playsinline preload="metadata" src="{e(vid)}"></video></div>'
    else:
        vsl = ""
    cta = f'<p class="ctarow"><span class="price">{e(o["price"])}</span><a class="btn" href="{e(buy)}">{e(o["button"])}</a></p>'
    body = f"""<section class="res landing"><div class="wrap narrow">
<span class="mono">{e(o['tag'])}</span>
<h1>{e(o['headline'])}</h1>
<p class="sub">{e(o['sub'])}</p>
{vsl}{cta}
<h2>What you get</h2><ul class="bullets">{inc}</ul>
<div class="pricebox"><span class="mono">Today</span><strong>{e(o['price'])}</strong><span>One-time payment. Instant access.</span>{cta.replace('<span class="price">'+e(o["price"])+'</span>','')}</div>
<h2>What you need</h2><ul class="bullets">{needs}</ul>
<h2>Who it's not for</h2><ul class="bullets">{notf}</ul>
<p class="foot">One-time payment of {e(o['price'])}. Checkout is handled by Dodo Payments. This is a set of instructions and files for an AI assistant. No sales or income are guaranteed.</p>
</div></section>"""
    d = dist / o["slug"]; d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(layout(f"{o['title']} | Rob Reece", o["sub"], body, f"/{o['slug']}/"))
    # welcome page (noindex, unguessable path)
    w = dist / "welcome" / o["welcome_token"]; w.mkdir(parents=True, exist_ok=True)
    if o["slug"] == "launchpad":
        zipbtn = f'<p><a class="btn" href="/welcome/{o["welcome_token"]}/{o["zip"]}">Download the starter kit (zip)</a></p>'
        shutil.copy(root / "assets/product" / o["zip"], w / o["zip"])
        inner = f"""<h2>Start here</h2>
<ol class="steps"><li>Read the Click Guide below so you know which steps are yours.</li><li>Download the starter kit and unzip it.</li><li>Open a new Claude chat and paste the master prompt. Tell Claude you have the starter kit.</li></ol>
{zipbtn}
<h2>The master prompt</h2>{prompt_box(rd('router-prompt.txt'), 'mp')}
<h2>Click Guide</h2>{rd('click-guide.html')}
<h2>Rollback Card</h2>{rd('rollback-card.html')}"""
    else:
        inner = f"""<h2>The Stage 6 prompt</h2><p>Paste this into your Launchpad chat once your site is live on your own domain. Fill in the [BRACKETS].</p>{prompt_box(rd('addon-prompt.txt'), 'ap')}{rd('addon-templates.html')}"""
    up = ""
    if o.get("upsell"):
        u = next(x for x in offers if x["slug"] == o["upsell"])
        up = f'<div class="formbox" style="margin-top:40px"><span class="mono">Next step, when you are ready</span><h3 style="color:#0e0e0e">{e(u["title"])}</h3><p>{e(u["sub"])}</p><p style="margin-top:14px"><a class="btn" href="/{u["slug"]}/">See the {e(u["title"])} ({e(u["price"])})</a></p></div>'
    wbody = f"""<section class="res"><div class="wrap narrow"><span class="mono">Thank you</span><h1>{e(o['welcome_title'])}</h1><p class="sub">Bookmark this page. Dodo also emailed you a link to it.</p>{inner}{up}<p class="foot">Questions? Reply to any email from Rob.</p></div></section>"""
    (w / "index.html").write_text(layout(f"{o['welcome_title']} | Rob Reece", "Your purchase.", wbody, f"/welcome/{o['welcome_token']}/", noindex=True))

(dist / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /thanks/\nDisallow: /r/\nDisallow: /welcome/\nSitemap: {site['domain']}/sitemap.xml\n")
urls = ["/"] + [f"/{m['slug']}/" for m in magnets] + [f"/{o['slug']}/" for o in offers]
(dist / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{site['domain']}{u}</loc></url>" for u in urls) + "</urlset>")
print("built", len(list(dist.rglob('*.html'))), "pages")
