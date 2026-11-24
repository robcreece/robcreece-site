#!/usr/bin/env python3
"""Static site generator for robcreece.com. Reads pages.json, writes dist/."""
import links
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

MARQ = "".join(f"<span>{t}</span>" for t in ["Simple offers.","Honest copy.","Organic traffic.","Your first online sale.","No guru required.","Built in one chat with Claude."])

import hashlib
CSSV = hashlib.md5((root / "assets/style.css").read_bytes()).hexdigest()[:8]

FOOT_MAGNETS = "".join(f'<li><a href="/{m["slug"]}/">{m["title"]}</a></li>' for m in magnets)
def foot_offers():
    return "".join(f'<li><a href="/{o["slug"]}/">{o["title"]}</a></li>' for o in cfg.get("offers", []))

def extra_ld(path, title=""):
    import json as _j
    out = []
    if path == "/":
        out.append({"@context": "https://schema.org", "@type": "WebSite", "name": site["name"], "url": site["domain"] + "/", "inLanguage": "en-US"})
        out.append({"@context": "https://schema.org", "@type": "Person", "name": "Rob Reece", "url": site["domain"] + "/", "jobTitle": "Solo marketer", "image": site["domain"] + "/assets/rob.jpg", "worksFor": {"@type": "Organization", "name": "5 Solas Marketing"}, "sameAs": [site["cultlike_url"]], "description": "Helps broke beginners get their first online sale with simple offers, honest copy and organic traffic."})
    for o in cfg.get("offers", []):
        if path == f"/{o['slug']}/":
            out.append({"@context": "https://schema.org", "@type": "Product", "name": o["title"], "description": o["sub"], "brand": {"@type": "Brand", "name": "Rob Reece"}, "offers": {"@type": "Offer", "price": o["price"].replace("$", ""), "priceCurrency": "USD", "availability": "https://schema.org/InStock", "url": site["domain"] + path}})
    import links as _l
    _bc = _l.crumbs(path, title.split(" | ")[0], site["domain"]) if path != "/" and not path.startswith(("/welcome/", "/thanks/", "/r/")) else None
    if _bc: out.append(_bc)
    return "".join(f'<script type="application/ld+json">{_j.dumps(x)}</script>' for x in out)

def layout(title, desc, body, path, noindex=False):
    robots = '<meta name="robots" content="noindex,nofollow">' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">{robots}
<link rel="canonical" href="{site['domain']}{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{site['domain']}{path}"><meta property="og:site_name" content="{e(site['name'])}"><meta property="og:image" content="{site['domain']}/assets/rob.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{site['domain']}/assets/rob.jpg">{site.get('head_extra','')}{extra_ld(path, title)}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rye&family=Oswald:wght@400;600;700&family=Special+Elite&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css?v={CSSV}">
<script async src="{site['emailit_script']}"></script>
</head><body>
<nav><div class="wrap"><a class="logo" href="/"><span>{e(site['name'])}</span></a><div class="navmenu"><a class="link" href="/#pain">The problem</a><a class="link" href="/#fix">The fix</a><a class="link" href="/#free">Free stuff</a><a class="link" href="/blog/">Blog</a><a class="link" href="/videos/">Videos</a><a class="join" href="/#free">Free tools</a></div></div></nav>
<div class="marquee"><div class="track">{MARQ}{MARQ}</div></div>
{body}
<footer><div class="wrap fgrid">
<div class="fcol"><a class="logo" href="/"><span>{e(site['name'])}</span></a><p class="fabout">Simple offers. Honest copy. Organic traffic. Helping broke beginners get their first online sale.</p><p class="fmail"><a href="mailto:rob@robcreece.com">rob@robcreece.com</a></p></div>
<div class="fcol"><h4>Free tools</h4><ul>{FOOT_MAGNETS}</ul></div>
<div class="fcol"><h4>Products</h4><ul>{foot_offers()}</ul></div>
<div class="fcol"><h4>Learn</h4><ul><li><a href="/blog/">Blog</a></li><li><a href="/videos/">Videos</a></li><li><a href="{site['cultlike_url']}">CultLike Marketing</a></li></ul><h4 style="margin-top:22px">Legal</h4><ul><li><a href="/privacy/">Privacy Policy</a></li><li><a href="/terms/">Terms of Use</a></li><li><a href="/refunds/">Refund Policy</a></li><li><a href="/earnings-disclaimer/">Earnings Disclaimer</a></li><li><a href="/contact/">Contact</a></li></ul></div>
</div><div class="wrap fbase"><span>&copy; 2026 5 Solas Marketing. Rob Reece. All rights reserved.</span><span>No income is guaranteed. Results vary. <a href="/earnings-disclaimer/">Read the disclaimer</a>.</span></div></footer>
</body></html>"""

def form_block(m):
    if m["form_token"]:
        return f'<div data-emailit-form="{m["form_token"]}"></div>'
    return '<p><strong>Form coming soon.</strong></p>'

# ---------- hub ----------
from urllib.parse import quote
offers = cfg.get("offers", [])
import links as _lk
_lp = _lk.load_posts()[:3]
blog_section = ""
if _lp:
    _cards = "".join(f'<a class="card" href="/blog/{p["slug"]}/"><h3>{e(p["title"])}</h3><p>{e(p["desc"])}</p><span class="mono">Read it</span></a>' for p in _lp)
    blog_section = f'<section id="blog" class="light"><div class="wrap"><span class="mono">From the blog</span><h2>Short reads. Real fixes.</h2><div class="grid">{_cards}</div><p style="margin-top:24px"><a class="btn" href="/blog/">All posts</a> <a class="link" href="/videos/">Watch the videos</a></p></div></section>'
offer_section = ""
if offers:
    o0 = offers[0]
    offer_section = f'''<section id="build" class="blood"><div class="wrap narrow"><span class="mono">Build your own</span><h2>Want a site like this one?</h2><p style="color:#cfcabb;max-width:620px">I built this site, its free tools and the signup flow in one chat with Claude. I packaged the process so you can do the same.</p><p style="margin-top:24px"><a class="btn" href="/{o0["slug"]}/">See the {e(o0["title"])}</a></p></div></section>'''

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

<section id="pain" class="light"><div class="wrap narrow">
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

<section id="free" class="light"><div class="wrap">
<span class="mono">Start here</span>
<h2>{h["free_title"]}</h2>
<p style="color:#cfcabb;max-width:620px">{h["free_sub"]}</p>
<div class="grid">{cards}</div>
</div></section>

{offer_section}
{blog_section}<section id="about"><div class="wrap aboutgrid">
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
</div></section><section><div class="wrap narrow">{links.related(f"/{m['slug']}/", m['slug'], magnets, cfg.get('offers', []))}</div></section>"""
    d = dist / m["slug"]; d.mkdir()
    (d / "index.html").write_text(layout(f"{m['title']} | Rob Reece", m["sub"], body, f"/{m['slug']}/"))

    tbody = """<section class="thanks"><div class="wrap narrow">
<span class="mono">One more step</span>
<h1>Go check your email now.</h1>
<p class="lead" style="margin:20px 0">Your free download is on its way. It should land in a minute or two.</p>
<ol class="bullets" style="margin:0 0 20px 20px;line-height:1.7">
<li><strong>Open your inbox.</strong> Look for an email from Rob Reece.</li>
<li><strong>Not there? Check Spam and Promotions.</strong> Drag it to your main inbox so you keep getting what I send.</li>
<li><strong>Hit reply and say hi.</strong> One word is fine. It tells your email provider I'm a real person, and I read every reply myself.</li>
</ol>
<p style="color:var(--mute)">Your access link is inside that email.</p>
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
    def buy_url(arm=None):
        r = f"{site.get('checkout_return_base', site['domain'])}/welcome/{o['welcome_token']}/" + (f"?arm={arm}" if arm else "")
        u = f"https://checkout.dodopayments.com/buy/{o['product_id']}?quantity=1&redirect_url={quote(r, safe='')}"
        return u + (f"&metadata_arm={arm}&metadata_funnel={o['slug']}" if arm else "")
    buy = buy_url()
    bd = root / "dist" / "buy" / o["slug"]; bd.mkdir(parents=True, exist_ok=True)
    (bd / "index.html").write_text(f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><title>Redirecting to checkout</title><meta http-equiv="refresh" content="0;url={e(buy)}"><p>Taking you to checkout... <a href="{e(buy)}">Continue</a></p><script>location.replace({json.dumps(buy)})</script>')
    inc = "".join(f"<li>{e(x)}</li>" for x in o["includes"])
    needs = "".join(f"<li>{e(x)}</li>" for x in o["needs"])
    notf = "".join(f"<li>{e(x)}</li>" for x in o["not_for"])
    bon = "".join(f"<li>{e(x)}</li>" for x in o.get("bonuses", []))
    bon_html = f'<ul class="bullets">{bon}</ul>' if bon else ""
    proof_html = f'<p class="lead"><strong>Proof:</strong> {e(o["proof"])}</p>' if o.get("proof") else ""
    faq_html = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in o.get("faq", []))
    faq_html = f"<h2>Quick answers</h2>{faq_html}" if faq_html else ""
    guar_html = f'<div class="pricebox"><span class="mono">Risk-free</span><span>{e(o["guarantee"])} <a href="/refunds/">Full refund policy</a>.</span></div>' if o.get("guarantee") else ""
    cross_html = f'<p class="lead">{e(o["cross"][0])} <a href="{e(o["cross"][1])}">{e(o["cross"][2])}</a></p>' if o.get("cross") else ""
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
<h2>What you get</h2><ul class="bullets">{inc}</ul>{bon_html}{proof_html}
<div class="pricebox"><span class="mono">Today</span><strong>{e(o['price'])}</strong><span>One-time payment. Instant access.</span>{cta.replace('<span class="price">'+e(o["price"])+'</span>','')}</div>
{guar_html}{cross_html}<h2>What you need</h2><ul class="bullets">{needs}</ul>
<h2>Who it's not for</h2><ul class="bullets">{notf}</ul>{faq_html}
{links.related(f"/{o['slug']}/", None, magnets, [x for x in offers if x['slug'] != o['slug']])}
<p class="foot">One-time payment of {e(o['price'])}. Checkout is handled by Dodo Payments. See the <a href="/refunds/">Refund Policy</a>, <a href="/terms/">Terms</a> and <a href="/earnings-disclaimer/">Earnings Disclaimer</a>. {e(o.get('foot', 'This is a set of instructions and files for an AI assistant. No sales or income are guaranteed.'))}</p>
</div></section>"""
    d = dist / o["slug"]; d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(layout(f"{o['title']} | Rob Reece", o["sub"], body, f"/{o['slug']}/"))
    for arm in o.get("arms", []):  # A/B test copies: same page, checkout tagged with the arm
        ad = d / arm; ad.mkdir(parents=True, exist_ok=True)
        (ad / "index.html").write_text(layout(f"{o['title']} | Rob Reece", o["sub"], body.replace(e(buy), e(buy_url(arm))), f"/{o['slug']}/", noindex=True))
    # welcome page (noindex, unguessable path)
    w = dist / "welcome" / o["welcome_token"]; w.mkdir(parents=True, exist_ok=True)
    if o["slug"] in ("launchpad", "launchpad-bundle"):
        zipbtn = f'<p><a class="btn" href="/welcome/{o["welcome_token"]}/{o["zip"]}">Download the starter kit (zip)</a></p>'
        shutil.copy(root / "assets/product" / o["zip"], w / o["zip"])
        inner = f"""<h2>Start here</h2>
<ol class="steps"><li>Read the Click Guide below so you know which steps are yours.</li><li>Download the starter kit and unzip it.</li><li>Open a new Claude chat and paste the master prompt. Tell Claude you have the starter kit.</li></ol>
{zipbtn}
<h2>The master prompt</h2>{prompt_box(rd('router-prompt.txt'), 'mp')}
<h2>Click Guide</h2>{rd('click-guide.html')}
<h2>Rollback Card</h2>{rd('rollback-card.html')}"""
        if o["slug"] == "launchpad-bundle":
            inner += f"""<h2>Part 2: Email Add-on. The Stage 6 prompt</h2><p>Paste this into your Launchpad chat once your site is live on your own domain. Fill in the [BRACKETS].</p>{prompt_box(rd('addon-prompt.txt'), 'ap')}{rd('addon-templates.html')}"""
    elif o["slug"] == "overlay-agency":
        import overlay
        shutil.copy(root / "assets/product/overlay-agency.pdf", w / "overlay-agency.pdf")
        inner = overlay.web_html(f"/welcome/{o['welcome_token']}/overlay-agency.pdf")
        inner += """<script>(function(){var a=new URLSearchParams(location.search).get('arm');var q='utm_source=robcreece&utm_medium=guide&utm_campaign=overlay-agency'+(a?'&utm_content='+encodeURIComponent(a):'');document.querySelectorAll('a.grafsy-link').forEach(function(l){l.href=l.href.split('?')[0]+'?'+q;});})();</script>"""
    else:
        inner = f"""<h2>The Stage 6 prompt</h2><p>Paste this into your Launchpad chat once your site is live on your own domain. Fill in the [BRACKETS].</p>{prompt_box(rd('addon-prompt.txt'), 'ap')}{rd('addon-templates.html')}"""
    up = ""
    if o.get("upsell"):
        u = next(x for x in offers if x["slug"] == o["upsell"])
        up = f'<div class="formbox" style="margin-top:40px"><span class="mono">Next step, when you are ready</span><h3 style="color:#0e0e0e">{e(u["title"])}</h3><p>{e(u["sub"])}</p><p style="margin-top:14px"><a class="btn" href="/{u["slug"]}/">See the {e(u["title"])} ({e(u["price"])})</a></p></div>'
    wbody = f"""<section class="res"><div class="wrap narrow"><span class="mono">Thank you</span><h1>{e(o['welcome_title'])}</h1><p class="sub">Bookmark this page. Dodo also emailed you a link to it.</p>{inner}{up}<p class="foot">Questions? Reply to any email from Rob.</p></div></section>"""
    (w / "index.html").write_text(layout(f"{o['welcome_title']} | Rob Reece", "Your purchase.", wbody, f"/welcome/{o['welcome_token']}/", noindex=True))

import links
import blog, videos, links
blog_urls = blog.build(root, dist, layout, magnets, form_block, site, cfg.get("offers", []))
site["_offers"] = cfg.get("offers", [])
video_urls = videos.build(root, dist, layout, magnets, form_block, site, cfg.get("offers", []))
import legal
legal_urls = legal.build(root, dist, layout, site)
(dist / "google9705e5d26db173ef.html").write_text("google-site-verification: google9705e5d26db173ef.html")
import subprocess, datetime
try:
    LASTMOD = subprocess.run(["git", "log", "-1", "--format=%cs"], capture_output=True, text=True, cwd=root).stdout.strip() or datetime.date.today().isoformat()
except Exception:
    LASTMOD = datetime.date.today().isoformat()
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended", "Bingbot", "Googlebot"]
priv = "Disallow: /thanks/\nDisallow: /r/\nDisallow: /welcome/\nDisallow: /buy/\n"
robots = "User-agent: *\nAllow: /\n" + priv + "\n" + "".join(f"User-agent: {b_}\nAllow: /\n{priv}\n" for b_ in AI_BOTS) + f"Sitemap: {site['domain']}/sitemap.xml\n"
(dist / "robots.txt").write_text(robots)
urls = ["/"] + blog_urls + video_urls + legal_urls + [f"/{m['slug']}/" for m in magnets] + [f"/{o['slug']}/" for o in offers]
def lm(u):
    if u.startswith("/blog/") and u != "/blog/":
        for p_ in json.loads((root / "blog/posts.json").read_text())["posts"]:
            if f"/blog/{p_['slug']}/" == u: return p_["date"]
    return LASTMOD
(dist / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{site['domain']}{u}</loc><lastmod>{lm(u)}</lastmod></url>" for u in urls) + "</urlset>")
# llms.txt: a plain-text guide for AI search and assistants
ll = [f"# {site['name']}", "", "> Rob Reece helps broke beginners get their first online sale with simple offers, honest copy and organic traffic. Solo marketer, no sales calls, no ad budget. Brand: 5 Solas Marketing. Related brand: CultLike Marketing.", "", "## Free tools"]
ll += [f"- [{m['title']}]({site['domain']}/{m['slug']}/): {m['card_blurb']}" for m in magnets]
ll += ["", "## Products"] + [f"- [{o['title']}]({site['domain']}/{o['slug']}/) ({o['price']}): {o['sub']}" for o in offers]
ll += ["", "## Blog and videos", f"- [Blog]({site['domain']}/blog/)", f"- [Videos]({site['domain']}/videos/)"]
ll += [f"- [{p_['title']}]({site['domain']}/blog/{p_['slug']}/): {p_['desc']}" for p_ in json.loads((root / "blog/posts.json").read_text())["posts"]]
ll += ["", "## Policies", f"- [Privacy]({site['domain']}/privacy/)", f"- [Terms]({site['domain']}/terms/)", f"- [Refunds]({site['domain']}/refunds/)", f"- [Contact]({site['domain']}/contact/)", "", "## About", f"- [Home]({site['domain']}/)", f"- [CultLike Marketing]({site['cultlike_url']})", ""]
(dist / "llms.txt").write_text("\n".join(ll))
# IndexNow key file (proves site ownership to Bing, Yandex and others)
ik = cfg["site"].get("indexnow_key")
if ik:
    (dist / f"{ik}.txt").write_text(ik)
print("built", len(list(dist.rglob('*.html'))), "pages")
