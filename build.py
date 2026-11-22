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
cards = "".join(
    f'<a class="card" href="/{m["slug"]}/" style="text-decoration:none"><span class="mono">{e(m["tag"])}</span><h3>{e(m["title"])}</h3><p>{e(m["card_blurb"])}</p><span class="mono">Get it free →</span></a>'
    for m in magnets)

bc_links = "".join(f'<li><a href="/{m["slug"]}/"><span>{e(m["title"])}</span><span class="mono">Free →</span></a></li>' for m in magnets)

hub = f"""
<section class="hero"><div class="wrap herogrid">
<div>
<span class="mono">Rob Reece · Solo marketer</span>
<h1>Your first online sale<br>doesn't need a guru.</h1>
<p class="lead">I help broke beginners get their first online sale with simple offers, honest copy, and organic traffic. No sales calls. No ad budget. No fake lifestyle.</p>
<a class="btn" href="#free">Grab the free tools</a> &nbsp; <a class="btn ghost" href="#pain">See if this is you</a>
</div>
<aside class="bizcard">
<img src="/assets/rob.jpg" alt="Rob Reece at his desk in front of the Cult Like Marketing banner" width="1000" height="800">
<div class="bc-body">
<h3>Rob Reece</h3>
<p class="mono">Solo marketer · CultLike Marketing</p>
<p class="bc-line">Simple offers. Honest copy. Organic traffic.</p>
<ul class="bc-links">
{bc_links}
</ul>
<a class="bc-cult" href="{site['cultlike_url']}">cultlikemarketing.com →</a>
</div>
</aside>
</div></section>

<section id="pain"><div class="wrap narrow">
<span class="mono">Sound familiar?</span>
<h2>You've done everything you were told to do.</h2>
<div class="pain">You've bought the course and still have no sale.</div>
<div class="pain">You post every day and nobody buys.</div>
<div class="pain">You don't know what to sell, or who to sell it to.</div>
<div class="pain">Your content reads like every other AI post, and people scroll past.</div>
<div class="pain">You're afraid of DMs and sales calls, so you hide.</div>
<p style="margin-top:24px;color:#cfcabb">That isn't a talent problem. It's a clarity problem. Fix the offer, the words, and the conversation, and sales follow.</p>
</div></section>

<section id="fix"><div class="wrap">
<span class="mono">The fix</span>
<h2>Small offers. Sharp words. Real conversations.</h2>
<div class="grid">
<div class="card"><h3>Pick a small offer</h3><p>A simple, low-priced product that solves one problem, so your first buyer says yes fast.</p></div>
<div class="card"><h3>Write like a human</h3><p>Direct-response copy that sounds like you at the kitchen table, not like a robot reading a script.</p></div>
<div class="card"><h3>Sell without calls</h3><p>Organic Facebook posts and friendly DMs. That's how I sell, and it's how I teach it.</p></div>
</div>
<p style="margin-top:30px"><a class="btn" href="{site['cultlike_url']}">See CultLike Marketing</a></p>
</div></section>

<section id="free"><div class="wrap">
<span class="mono">Start here</span>
<h2>Free tools. Steal them.</h2>
<p style="color:#cfcabb;max-width:620px">Pick one. Enter your email. It lands in your inbox.</p>
<div class="grid">{cards}</div>
</div></section>

<section id="about"><div class="wrap aboutgrid">
<img src="/assets/rob.jpg" alt="Rob Reece" loading="lazy" width="1000" height="800">
<div>
<span class="mono">About</span>
<h2>I'm Rob.</h2>
<p>I'm a solo marketer. I build small offers, write the copy, and sell through organic Facebook posts and messages. No sales calls, ever.</p>
<p style="margin-top:14px">I'm also a husband, a dad of a big family, and a minister. I run experiments in the open and hand you what works.</p>
<p style="margin-top:24px"><a class="btn" href="#free">Start with a free tool</a></p>
</div>
</div></section>
"""
(dist / "index.html").write_text(layout("Rob Reece | Get your first online sale", "Simple offers, honest copy, and organic traffic for broke beginners seeking their first online sale.", hub, "/"))

# ---------- magnets + thank-you ----------
for m in magnets:
    bl = "".join(f"<li>{e(b)}</li>" for b in m["bullets"])
    body = f"""<section class="hero"><div class="wrap narrow">
<span class="mono">{e(m['tag'])}</span>
<h1>{e(m['headline'])}</h1>
<p class="lead">{e(m['sub'])}</p>
<ul class="bullets">{bl}</ul>
<div class="formbox"><span class="mono">{e(m['cta'])}</span>{form_block(m)}</div>
<p style="margin-top:14px;color:var(--mute);font-size:14px">No spam. Unsubscribe any time.</p>
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
    (d / "index.html").write_text(layout(f"{ttl} | Rob Reece", freebies.DATA[slug]["subtitle"], freebies.web_body(slug, f"/downloads/{slug}.pdf"), f"/r/{slug}/", noindex=True))

(dist / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /thanks/\nDisallow: /r/\nSitemap: {site['domain']}/sitemap.xml\n")
urls = ["/"] + [f"/{m['slug']}/" for m in magnets]
(dist / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{site['domain']}{u}</loc></url>" for u in urls) + "</urlset>")
print("built", len(list(dist.rglob('*.html'))), "pages")
