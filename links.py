"""Internal linking helpers: related-content blocks, in-body auto-links, breadcrumbs data, legal cross-links."""
import html, json, re
from pathlib import Path

e = html.escape
ROOT = Path(__file__).parent

# first mention of these phrases inside post/video body text becomes a link
REL = ' rel="sponsored noopener"'
AUTOLINK = [
    ("The Robot Tells", "/robot-tells/"), ("Robot Tells", "/robot-tells/"),
    ("AI Word List", "/ai-word-list/"),
    ("DM Reply Builder", "/dm-reply-builder/"),
    ("One-Prompt Website", "/one-prompt-website/"),
    ("One-Chat Launchpad", "/launchpad/"), ("Launchpad", "/launchpad/"),
    ("Overlay Agency", "/overlay-agency/"),
    ("Grafsy", "https://grafsy.app/?utm_source=robcreece&utm_medium=video&utm_campaign=claude-vs-grafsy"),
]


def autolink(text_escaped, used, skip_url=None):
    """Link the first mention of each target page (once per page, never to itself). Operates on escaped text with no tags."""
    for phrase, url in AUTOLINK:
        if url in used or url == skip_url:
            continue
        pat = re.compile(r"(?<![\w/>-])" + re.escape(e(phrase)) + r"(?![\w-])")
        if pat.search(text_escaped):
            text_escaped = pat.sub(lambda m: f'<a href="{url}"{REL if url.startswith("http") else ""}>{m.group(0)}</a>', text_escaped, count=1)
            used.add(url)
    return text_escaped


def load_posts():
    d = json.loads((ROOT / "blog" / "posts.json").read_text())
    return sorted(d["posts"], key=lambda p: p["date"], reverse=True)


def load_videos():
    d = json.loads((ROOT / "videos" / "videos.json").read_text())
    return sorted([v for v in d["videos"] if not v.get("draft")], key=lambda v: v["date"], reverse=True)


def related(current_url, magnet_slug, magnets, offers):
    """'Keep going' block: other posts + videos (same freebie first), the other free tools, and the paid products."""
    posts = [("/blog/%s/" % p["slug"], p["title"], p.get("magnet")) for p in load_posts()]
    vids = [("/videos/%s/" % v["slug"], v["title"], v.get("magnet")) for v in load_videos()]
    content = [x for x in posts + vids if x[0] != current_url]
    content.sort(key=lambda x: 0 if x[2] == magnet_slug else 1)
    read = "".join(f'<li><a href="{u}">{e(t)}</a></li>' for u, t, _ in content[:4])
    tools = "".join(f'<li><a href="/{m["slug"]}/">{e(m["title"])}</a></li>' for m in magnets if m["slug"] != magnet_slug)
    prods = "".join(f'<li><a href="/{o["slug"]}/">{e(o["title"])}</a> ({e(o["price"])})</li>' for o in offers if not o.get("funnel_only"))
    cols = []
    if read:
        cols.append(f'<div><h3>Keep reading</h3><ul class="bullets">{read}<li><a href="/blog/">All posts</a></li><li><a href="/videos/">All videos</a></li></ul></div>')
    cols.append(f'<div><h3>More free tools</h3><ul class="bullets">{tools}</ul></div>')
    cols.append(f'<div><h3>When you are ready for more</h3><ul class="bullets">{prods}</ul></div>')
    return '<aside class="related"><h2>Keep going</h2><div class="grid">' + "".join(cols) + "</div></aside>"


def crumbs(path, title, domain):
    """BreadcrumbList data for a path. title is the page title without the site suffix."""
    seg = [s for s in path.strip("/").split("/") if s]
    if not seg:
        return None
    items = [("Home", "/")]
    if seg[0] in ("blog", "videos") and len(seg) > 1:
        items.append(({"blog": "Blog", "videos": "Videos"}[seg[0]], f"/{seg[0]}/"))
    items.append((title, path))
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": domain + u} for i, (n, u) in enumerate(items)]}


def legal_nav(pages, current):
    names = {"privacy": "Privacy Policy", "terms": "Terms of Use", "refunds": "Refund Policy", "earnings-disclaimer": "Earnings Disclaimer", "contact": "Contact"}
    li = "".join(f'<a href="/{s}/">{n}</a>' for s, n in names.items() if s != current)
    return f'<p class="legalnav">Also see: {li} <a href="/">Home</a></p>'
