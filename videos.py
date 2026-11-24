"""YouTube video pages: embed (click-to-load), SEO blog post, schema.org markup, freebie CTA."""
import html, json
from pathlib import Path
from blog import blocks
import links

e = html.escape


def ts(sec):
    return f"{sec // 60}:{sec % 60:02d}"


def build(root, dist, layout, magnets, form_block, site, offers=()):
    data = json.loads((root / "videos" / "videos.json").read_text())
    by = {m["slug"]: m for m in magnets}
    default = by.get(data["default_magnet"]) or magnets[0]
    vids = sorted([v for v in data["videos"] if not v.get("draft")], key=lambda v: v["date"], reverse=True)
    dom = site["domain"]
    for v in vids:
        m = by.get(v.get("magnet")) or default
        v["_m"] = m
        vid = v["youtube_id"]
        thumb = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
        url = f"{dom}/videos/{v['slug']}/"
        embed = f"https://www.youtube-nocookie.com/embed/{vid}"
        player = f'''<div class="vframe" data-vid="{e(vid)}"><button class="vplay" aria-label="Play video: {e(v["title"])}"><img src="{thumb}" alt="{e(v["title"])}" loading="eager" width="480" height="360"><span class="vbtn">&#9654;</span></button>
<noscript><a href="https://www.youtube.com/watch?v={e(vid)}">Watch on YouTube</a></noscript></div>
<script>document.querySelectorAll('.vframe').forEach(function(f){{f.querySelector('.vplay').addEventListener('click',function(){{var i=document.createElement('iframe');i.src='{embed}?autoplay=1&rel=0';i.allow='accelerometer; autoplay; encrypted-media; picture-in-picture';i.allowFullscreen=true;i.title={json.dumps(v["title"])};f.innerHTML='';f.appendChild(i);}});}});</script>'''
        mid = f'<aside class="inline-cta"><span class="mono">Free: {e(m["title"])}</span><p>{e(m["card_blurb"])}</p><a class="btn" href="#get-free">{e(m["cta"])}</a></aside>'
        top = f'<a class="topbar" href="#get-free"><span class="mono">Free</span> {e(m["title"])}: {e(m["card_blurb"])} <span class="arrow">Get it &darr;</span></a>'
        end = f'<div class="formbox" id="get-free"><span class="mono">Free: {e(m["title"])}</span><h3 style="color:#0b0908">{e(m["headline"])}</h3><p>{e(m["sub"])}</p>{form_block(m)}<p style="margin-top:10px;font-size:14px">No spam. Unsubscribe any time.</p></div>'
        take = '<h2>What you will learn</h2><ul class="bullets">' + "".join(f"<li>{e(t)}</li>" for t in v.get("takeaways", [])) + "</ul>" if v.get("takeaways") else ""
        chap = '<h2>Chapters</h2><ul class="bullets">' + "".join(f'<li><a href="https://www.youtube.com/watch?v={e(vid)}&t={s}s" rel="noopener">{ts(s)}</a> {e(l)}</li>' for s, l in v.get("chapters", [])) + "</ul>" if v.get("chapters") else ""
        faq = ""
        if v.get("faq"):
            faq = "<h2>Quick answers</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in v["faq"])
        tr = f'<details class="transcript"><summary>Read the transcript</summary><p>{e(v["transcript"])}</p></details>' if v.get("transcript") else ""
        ld = [{"@context": "https://schema.org", "@type": "VideoObject", "name": v["title"], "description": v["desc"], "thumbnailUrl": [thumb], "uploadDate": v["date"], "duration": v.get("duration", ""), "embedUrl": embed, "contentUrl": f"https://www.youtube.com/watch?v={vid}", "publisher": {"@type": "Person", "name": site["name"]}},
              {"@context": "https://schema.org", "@type": "BlogPosting", "headline": v["title"], "description": v["desc"], "datePublished": v["date"], "image": thumb, "mainEntityOfPage": url, "author": {"@type": "Person", "name": site["name"]}}]
        if v.get("faq"):
            ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in v["faq"]]})
        ldjson = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in ld)
        body = f'''{top}<section class="res post"><div class="wrap narrow">
<p class="mono crumbs"><a href="/">Home</a> / <a href="/videos/">Videos</a> / {e(v["date"])}</p>
<h1>{e(v["h1"])}</h1>
{player}
<p class="lead">{e(v["summary"])}</p>
{take}{chap}{blocks(v["body"], mid, f"/videos/{v['slug']}/")}{faq}{tr}{end}
{links.related(f"/videos/{v['slug']}/", m["slug"], magnets, offers)}
<p class="foot"><a href="/videos/">&larr; More videos</a></p>
{ldjson}
</div></section>'''
        d = dist / "videos" / v["slug"]; d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(layout(f"{v['title']} | Rob Reece", v["desc"], body, f"/videos/{v['slug']}/"))
    cards = "".join(f'<a class="card vcard" href="/videos/{v["slug"]}/"><img src="https://i.ytimg.com/vi/{e(v["youtube_id"])}/hqdefault.jpg" alt="{e(v["title"])}" loading="lazy" width="480" height="360"><span class="mono">Free with this: {e(v["_m"]["title"])}</span><h3>{e(v["title"])}</h3><p>{e(v["desc"])}</p></a>' for v in vids)
    if not cards:
        cards = "<p>Videos are coming soon.</p>"
    idx = f'''<section class="hero"><div class="wrap narrow"><span class="mono">Videos</span><h1>Watch. Then grab the free tool.</h1>
<p class="lead">Short videos on simple offers, honest copy and getting your first online sale. Every one has a free tool to go with it. Prefer reading? Try the <a href="/blog/">blog</a>.</p>
<div class="formbox"><span class="mono">Start here: {e(default["title"])}</span><p>{e(default["card_blurb"])}</p>{form_block(default)}</div></div></section>
<section><div class="wrap"><h2>Latest videos</h2><div class="grid">{cards}</div></div></section>'''
    d = dist / "videos"; d.mkdir(exist_ok=True)
    (d / "index.html").write_text(layout("Videos | Rob Reece", "Videos on simple offers, honest copy and getting your first online sale, each with a free tool.", idx, "/videos/"))
    return ["/videos/"] + [f"/videos/{v['slug']}/" for v in vids]
