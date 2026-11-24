"""Blog: every page leads to a freebie. Index + posts, with a freebie CTA at top, middle and end."""
import html, json
from pathlib import Path
import links

e = html.escape


def blocks(body, cta_mid, skip_url=None):
    out, n_p, used = [], 0, set()
    for kind, val in body:
        if kind == "h2":
            out.append(f"<h2>{e(val)}</h2>")
        elif kind == "ul":
            out.append('<ul class="bullets">' + "".join(f"<li>{links.autolink(e(x), used, skip_url)}</li>" for x in val) + "</ul>")
        else:
            out.append(f"<p>{links.autolink(e(val), used, skip_url)}</p>")
            n_p += 1
            if n_p == 2:
                out.append(cta_mid)
    return "".join(out)


def build(root, dist, layout, magnets, form_block, site, offers=()):
    data = json.loads((root / "blog" / "posts.json").read_text())
    by = {m["slug"]: m for m in magnets}
    default = by.get(data["default_magnet"]) or magnets[0]
    posts = sorted(data["posts"], key=lambda p: p["date"], reverse=True)
    for p in posts:
        m = by.get(p.get("magnet")) or default  # fallback: a post always leads to a freebie
        p["_m"] = m
        mid = f'<aside class="inline-cta"><span class="mono">Free: {e(m["title"])}</span><p>{e(m["card_blurb"])}</p><a class="btn" href="#get-free">{e(m["cta"])}</a></aside>'
        top = f'<a class="topbar" href="#get-free"><span class="mono">Free</span> {e(m["title"])}: {e(m["card_blurb"])} <span class="arrow">Get it &darr;</span></a>'
        end = f'<div class="formbox" id="get-free"><span class="mono">Free: {e(m["title"])}</span><h3 style="color:#0b0908">{e(m["headline"])}</h3><p>{e(m["sub"])}</p>{form_block(m)}<p style="margin-top:10px;font-size:14px">No spam. Unsubscribe any time.</p></div>'
        body = f'''{top}<section class="res post"><div class="wrap narrow">
<p class="mono crumbs"><a href="/">Home</a> / <a href="/blog/">Blog</a> / {e(p["date"])}</p>
<h1>{e(p["title"])}</h1>
{blocks(p["body"], mid, f"/blog/{p['slug']}/")}
{end}
{links.related(f"/blog/{p['slug']}/", m["slug"], magnets, offers)}
<p class="foot"><a href="/blog/">&larr; More posts</a></p>
</div></section>'''
        d = dist / "blog" / p["slug"]; d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(layout(f"{p['title']} | Rob Reece", p["desc"], body, f"/blog/{p['slug']}/"))
    # index: freebie first, then posts, each card tagged with its freebie
    cards = "".join(f'<a class="card" href="/blog/{p["slug"]}/"><span class="mono">Free with this: {e(p["_m"]["title"])}</span><h3>{e(p["title"])}</h3><p>{e(p["desc"])}</p><span class="mono">Read it</span></a>' for p in posts)
    d_m = default
    idx = f'''<section class="hero"><div class="wrap narrow"><span class="mono">The blog</span><h1>Simple offers. Honest copy. Real sales.</h1>
<p class="lead">Short posts for beginners who want a first online sale. Every one comes with a free tool.</p>
<div class="formbox"><span class="mono">Start here: {e(d_m["title"])}</span><p>{e(d_m["card_blurb"])}</p>{form_block(d_m)}</div></div></section>
<section><div class="wrap"><h2>Latest posts</h2><div class="grid">{cards}</div><p style="margin-top:28px">Prefer to watch? See the <a href="/videos/">videos</a>. Or browse all the <a href="/#free">free tools</a>.</p></div></section>'''
    d = dist / "blog"; d.mkdir(exist_ok=True)
    (d / "index.html").write_text(layout("Blog | Rob Reece", "Short posts on simple offers, honest copy and organic traffic. Each one comes with a free tool.", idx, "/blog/"))
    return ["/blog/"] + [f"/blog/{p['slug']}/" for p in posts]
