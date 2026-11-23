"""The Overlay Agency guide: one source for the welcome page (HTML) and the PDF."""
import html
from pathlib import Path

e = html.escape
GRAFSY = "https://grafsy.app/"

TITLE = "The Overlay Agency"
SUB = "Start a one-person video graphics service this week. Your clients film. Software adds the graphics. You find the clients and deliver the file."

# Each section: (heading, [blocks]); block = ("p", text) | ("b", bold, rest) | ("ol"/"ul"/"check", [items]) | ("q", quote) | ("table", [rows])
SECTIONS = [
    ("Read this first", [
        ("b", "I co-own Grafsy, the software this guide uses.", "That's why the guide is $4. I earn if you buy the tool, so weigh everything here with that in mind."),
        ("b", "No income promises.", "I don't know your niche, your effort or your prices. This is a method. The math is yours to check."),
    ]),
    ("1. The service", [
        ("p", "You sell one thing: a graphics pass on a video the client already filmed."),
        ("p", "They send you a finished talking video. You send back the same video with on-screen graphics timed to what they say."),
        ("b", "Before:", "A coach talks to camera for 12 minutes. Nothing on screen changes. It looks like a webcam recording."),
        ("b", "After:", "Same 12 minutes. When she hits a key point, a callout appears on screen to back it up. It looks like someone produced it."),
        ("p", "That's the whole job. You don't film. You don't cut. You don't learn motion graphics."),
        ("h", "Your three tasks"),
        ("ol", ["Find people who post plain talking videos.", "Run their video through the software and watch the result.", "Deliver the file and get paid."]),
        ("b", "Why someone pays you for this:", "they don't want to do it. They want to record, hand it off and get back something that looks finished. Same reason people pay to have a lawn mowed when they own a mower."),
    ]),
    ("2. Who buys", [
        ("p", "Your buyer already posts talking videos on a schedule, and those videos are plain."),
        ("ul", ["Video podcasts and interview shows", "Coaches and consultants on YouTube", "Course creators with lesson videos", "Businesses with explainer videos", "Editors and small agencies who want to hand off the graphics work"]),
        ("h", "Three filters. You want a yes on all three."),
        ("ol", ["They speak English on camera. Grafsy is English-first right now.",
                "Their videos run several minutes. The software is built mainly for medium and long videos. Shorts work too, but long videos mean bigger jobs.",
                "They post on a schedule. Weekly posters turn into repeat work. One-off posters don't."]),
        ("h", "Find 20 leads today"),
        ("ol", ["Search YouTube for your niche plus \"podcast\" or \"coach.\"", "Filter by upload date: this month.", "Open the videos where nothing on screen changes.",
                "Write down the name, the channel and one way to reach them. Check the channel's About tab, then Facebook, Instagram or LinkedIn."]),
        ("b", "Example:", "Search \"real estate investing podcast.\" Filter to this month. You find a show with two people talking, weekly uploads and no graphics. That's a lead. Do it 19 more times."),
    ]),
    ("3. The free 60-second sample pitch", [
        ("p", "Don't describe the service. Show it on their own video."),
        ("b", "Why the scripts below say \"because\":", "In Ellen Langer's 1978 copy-machine study, people asking to cut in line got a yes 60% of the time with no reason and 94% of the time with one. For a small ask, almost any reason worked. For a big ask, only a real reason helped. So every ask here comes with a true reason."),
        ("h", "Step 1. Ask for a clip (small ask)"),
        ("q", "Hey [name], watched your episode on [topic]. Could you send me any 60-second clip from it? Asking because I add on-screen graphics to videos like yours, and I'd rather show you than describe it. Free, no strings."),
        ("p", "Compare that with what everyone else sends:"),
        ("q", "Hi, I run a video agency and would love to hop on a quick call to discuss your content needs."),
        ("p", "The first one asks for a clip and gives a reason. The second one asks for 30 minutes and gives none."),
        ("h", "Step 2. Make the sample"),
        ("p", "Upload the clip to Grafsy. A 60-second clip uses one minute of your allowance. Download the result and watch all of it before you send it. If the graphics miss, don't send it. Ask for a different clip."),
        ("h", "Step 3. Send it back and ask for the job (big ask)"),
        ("q", "Here's your clip with graphics on it. Want me to do the full episode? It's $[price] because that covers the processing and me checking every graphic before you see it."),
        ("p", "This is the big ask, so the reason has to be real. Use the true reason for your price. Don't invent one."),
        ("h", "Step 4. Follow up once"),
        ("p", "Three days later:"),
        ("q", "Did you get a chance to watch the clip?"),
        ("p", "Then move on. Send ten samples before you decide whether this works for you."),
    ]),
    ("4. Pricing", [
        ("p", "Know your floor before you quote. Processing minutes are your only hard cost."),
        ("p", "Once your plan's included minutes are gone, top-up packs run from $9 for 10 minutes to $75 for 120 minutes. That works out to about $0.63 to $0.90 per minute of video."),
        ("table", [["Client video length", "Your cost in minutes, at top-up rates"], ["5 minutes", "about $3 to $5"], ["10 minutes", "about $6 to $9"], ["30 minutes", "about $19 to $27"], ["60 minutes", "about $38 to $54"]]),
        ("p", "Add your time on top: uploading, watching the full result and delivering."),
        ("b", "Price by the finished minute.", "It's easy for the client to understand, and your price grows with your cost."),
        ("b", "Example (arithmetic, not a promise):", "At $10 per finished minute, a 10-minute video is a $100 job that uses about $6 to $9 of minutes. Pick your own number. I can't tell you what your market will pay."),
        ("h", "Four rules"),
        ("ol", ["Charge per video or per finished minute. Never hourly.",
                "Quote 48 to 72 hours for delivery. Processing time isn't guaranteed, so give yourself room.",
                "Tell clients up front that the graphics are template-style and placed by AI. You can't hand-pick fonts or positions right now.",
                "Decide your redo policy before you quote. A re-run uses minutes again."]),
        ("p", "When the first video lands well, offer a monthly bundle, such as four videos a month. Weekly posters are who you went looking for in section 2."),
    ]),
    ("5. Get Grafsy", [
        ("grafsy", "Get Grafsy because it's the one part of this you can't do by hand without learning motion graphics. And yes, I co-own it."),
        ("p", "Every plan is a one-time payment. Client work is allowed on all of them."),
        ("table", [["Plan", "One-time price", "Minutes included"], ["Starter", "$79", "10"], ["Creator", "$149", "30"], ["Agency", "$299", "90"], ["Agency Pro", "$999", "500"]]),
        ("b", "Start with Starter.", "Ten minutes is ten 60-second samples. That tells you whether the pitch works before you spend more. Top up or move to a bigger plan when a client says yes."),
        ("h", "Know the limits before you sell, so you never overpromise"),
        ("ul", ["Minutes don't renew. When they're gone, you buy top-ups in the dashboard.",
                "\"Lifetime\" means access for as long as the product operates. It doesn't mean unlimited processing.",
                "You can't manually set fonts, sizes, positions or timing right now.",
                "Face avoidance is optional and not guaranteed. Watch every video before you deliver it.",
                "There's no guaranteed processing time.",
                "You download an MP4. Save your own copy right away. Don't count on the file staying in your account.",
                "It's English-first for now."]),
        ("p", "Prices and limits are from grafsy.app, checked November 12, 2026. Check the site before you buy, because they can change."),
    ]),
    ("Start today", [
        ("check", ["List 20 leads using section 2", "Get Grafsy Starter", "Send 10 clip requests with the Step 1 script",
                   "Run each clip you get back, watch it, then send it", "Quote the full video with a real because", "Follow up once after three days"]),
    ]),
]


def web_html(pdf_url):
    out = [f'<p class="lead">{e(SUB)}</p>', f'<p><a class="btn" href="{e(pdf_url)}">Download the PDF</a></p>']
    for head, blocks in SECTIONS:
        out.append(f"<h2>{e(head)}</h2>")
        for b in blocks:
            k = b[0]
            if k == "p": out.append(f"<p>{e(b[1])}</p>")
            elif k == "h": out.append(f"<h3>{e(b[1])}</h3>")
            elif k == "b": out.append(f"<p><strong>{e(b[1])}</strong> {e(b[2])}</p>")
            elif k == "q": out.append(f'<blockquote class="quote">{e(b[1])}</blockquote>')
            elif k in ("ol", "ul"): out.append(f'<{k} class="steps">' + "".join(f"<li>{e(x)}</li>" for x in b[1]) + f"</{k}>")
            elif k == "check": out.append('<ul class="steps">' + "".join(f"<li>&#9744; {e(x)}</li>" for x in b[1]) + "</ul>")
            elif k == "table":
                rows = b[1]
                out.append("<table>" + "<tr>" + "".join(f"<th>{e(c)}</th>" for c in rows[0]) + "</tr>" + "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in rows[1:]) + "</table>")
            elif k == "grafsy":
                out.append(f"<p>{e(b[1])}</p>")
                out.append(f'<p><a class="btn grafsy-link" href="{GRAFSY}">See Grafsy plans</a></p>')
    return "\n".join(out)


def build_pdf(path):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem

    ink, gold, mute = colors.HexColor("#0B0C0E"), colors.HexColor("#9A7A2E"), colors.HexColor("#555555")
    base = ParagraphStyle("base", fontName="Helvetica", fontSize=11, leading=16, textColor=ink, spaceAfter=8)
    h1 = ParagraphStyle("h1", parent=base, fontName="Helvetica-Bold", fontSize=26, leading=30, spaceAfter=10)
    sub = ParagraphStyle("sub", parent=base, fontSize=12.5, leading=18, textColor=gold, spaceAfter=18)
    h2 = ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=16, leading=20, spaceBefore=14, spaceAfter=8)
    h3 = ParagraphStyle("h3", parent=base, fontName="Helvetica-Bold", fontSize=12, spaceBefore=6, spaceAfter=4)
    quote = ParagraphStyle("q", parent=base, leftIndent=14, borderPadding=(6, 8, 6, 8), backColor=colors.HexColor("#F3EFE4"), spaceBefore=4, spaceAfter=12)
    foot = ParagraphStyle("f", parent=base, fontSize=9, textColor=mute)

    def lst(items, kind):
        bt = "bullet" if kind != "ol" else "1"
        return ListFlowable([ListItem(Paragraph(e(x), base), leftIndent=14) for x in items], bulletType=bt, start=("1" if kind == "ol" else ("☐" if kind == "check" else "•")), leftIndent=16)

    story = [Paragraph(TITLE, h1), Paragraph(e(SUB), sub)]
    for head, blocks in SECTIONS:
        story.append(Paragraph(e(head), h2))
        for b in blocks:
            k = b[0]
            if k == "p": story.append(Paragraph(e(b[1]), base))
            elif k == "h": story.append(Paragraph(e(b[1]), h3))
            elif k == "b": story.append(Paragraph(f"<b>{e(b[1])}</b> {e(b[2])}", base))
            elif k == "q": story.append(Paragraph(e(b[1]), quote))
            elif k in ("ol", "ul", "check"): story.append(lst(b[1], k)); story.append(Spacer(1, 6))
            elif k == "grafsy": story.append(Paragraph(e(b[1]) + f' <link href="{GRAFSY}" color="#9A7A2E">grafsy.app</link>', base))
            elif k == "table":
                t = Table(b[1], hAlign="LEFT")
                t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 10.5), ("FONT", (0, 1), (-1, -1), "Helvetica", 10.5),
                                       ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ECE6D6")), ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
                                       ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
                story += [t, Spacer(1, 10)]
    story += [Spacer(1, 18), Paragraph("By Rob Reece &middot; robcreece.com &middot; 5 Solas Marketing. Rob Reece co-owns Grafsy. No income or sales are guaranteed.", foot)]

    def pg(c, d):
        c.setFont("Helvetica", 8.5); c.setFillColor(mute)
        c.drawString(0.9 * inch, 0.55 * inch, "The Overlay Agency  |  robcreece.com")
        c.drawRightString(letter[0] - 0.9 * inch, 0.55 * inch, f"Page {d.page}")

    doc = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.85 * inch, bottomMargin=0.85 * inch, title=TITLE, author="Rob Reece")
    doc.build(story, onFirstPage=pg, onLaterPages=pg)


if __name__ == "__main__":
    build_pdf(Path(__file__).parent / "assets/product/overlay-agency.pdf")
    print("pdf ok")
