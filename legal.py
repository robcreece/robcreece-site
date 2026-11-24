"""Legal pages: privacy, terms, refunds, earnings disclaimer, contact. Plain-English, matched to how this site works."""
import html
import links
e = html.escape
UPDATED = "November 24, 2026"
BIZ = "5 Solas Marketing"
MAIL = "rob@robcreece.com"

PAGES = {
 "privacy": ("Privacy Policy", "How robcreece.com collects, uses and protects your information.", """
<p>This site is run by Rob Reece of {BIZ} (&ldquo;I&rdquo;, &ldquo;me&rdquo;). This policy explains what I collect and what I do with it. Questions: <a href="mailto:{MAIL}">{MAIL}</a>.</p>
<h2>What I collect</h2>
<ul class="bullets"><li>Your name and email address, when you sign up for a free tool or my email list.</li>
<li>Purchase details (name, email, product, amount), when you buy. Your card details go to the payment processor, never to me.</li>
<li>Messages you send me, such as email replies.</li>
<li>Basic technical data your browser sends to any website, such as IP address and device type, handled by my hosting and email providers.</li></ul>
<h2>How I use it</h2>
<ul class="bullets"><li>To send you the free tool or product you asked for.</li>
<li>To email you tips and offers. Every email has an unsubscribe link and I honor it.</li>
<li>To answer your questions, process refunds and keep records.</li>
<li>To keep the site working and secure.</li></ul>
<p>I do not sell your personal information.</p>
<h2>Who handles your data</h2>
<p>I use a few services to run the site. They process data only to provide their service to me:</p>
<ul class="bullets"><li><strong>Dodo Payments</strong>: checkout and payment processing.</li>
<li><strong>Emailit</strong>: sign-up forms and email delivery.</li>
<li><strong>Cloudflare and GitHub</strong>: website hosting and delivery.</li>
<li><strong>YouTube</strong>: embedded videos. I use the privacy-enhanced embed, and YouTube loads only when you press play.</li></ul>
<h2>Cookies</h2>
<p>I do not set advertising or tracking cookies on this site. Third-party services I use, such as the payment checkout, may set cookies they need to work.</p>
<h2>How long I keep it</h2>
<p>I keep email list data until you unsubscribe or ask me to delete it. I keep purchase and refund records as long as needed for taxes, accounting and legal reasons.</p>
<h2>Your choices</h2>
<p>You can unsubscribe from any email, and you can ask me to see, fix or delete your data by emailing <a href="mailto:{MAIL}">{MAIL}</a>. If you are in a place with privacy laws that give you more rights (such as the EU, UK or California), I will honor those rights too.</p>
<h2>Children</h2>
<p>This site is for adults. I do not knowingly collect information from children under 13.</p>
<h2>Changes</h2>
<p>If I change this policy I will update the date above.</p>"""),
 "terms": ("Terms of Use", "The terms for using robcreece.com and buying from it.", """
<p>By using this site or buying from it, you agree to these terms. The site is run by Rob Reece of {BIZ}.</p>
<h2>What I sell</h2>
<p>I sell digital information products: guides, prompts, templates and checklists for use with an AI assistant. Nothing is shipped. You get access by email or a download link after purchase. Free tools are free, with no purchase needed.</p>
<h2>What you need</h2>
<p>Some products need things I do not provide, such as your own AI assistant account, a domain name or an email tool. Those cost extra and have their own terms. I am not responsible for third-party services.</p>
<h2>Payments</h2>
<p>Checkout is handled by Dodo Payments. Prices are shown before you pay. Taxes may be added where required.</p>
<h2>Your license</h2>
<p>When you buy, you get a personal license to use the product for your own projects and business. You may not resell, share, repost or give away the product files or prompts. You may use what you build with them however you like.</p>
<h2>Refunds</h2>
<p>See the <a href="/refunds/">Refund Policy</a>.</p>
<h2>No guarantee of results</h2>
<p>I share what I know in good faith, but I cannot promise any result. See the <a href="/earnings-disclaimer/">Earnings Disclaimer</a>.</p>
<h2>Acceptable use</h2>
<p>Do not use my products or emails to send spam, break the law, or mislead people.</p>
<h2>Limit of liability</h2>
<p>The site and products are provided &ldquo;as is.&rdquo; To the fullest extent the law allows, I am not liable for indirect or consequential losses, and my total liability for any claim is limited to the amount you paid for the product involved.</p>
<h2>Changes and law</h2>
<p>I may update these terms and will change the date below. These terms are governed by the laws of the State of Texas, without regard to conflict-of-law rules.</p>
<h2>Contact</h2>
<p><a href="mailto:{MAIL}">{MAIL}</a></p>"""),
 "refunds": ("Refund Policy", "Every paid product has its own refund window, from 14 to 90 days. It is stated on the product page.", """
<p>I want you to feel safe buying from me. Refund windows are not the same for every product. Each paid product has its own guarantee, anywhere from 14 to 90 days, and it is written on that product's page before you buy.</p>
<h2>Which window applies to you</h2>
<p>The guarantee shown on the product page at the time you bought is the one that applies. Your receipt email comes from that same purchase, so you can always check the product page or ask me.</p>
<h2>Current guarantees</h2>
<ul>
<li>The Launchpad and anything bought with it: 30 days. Follow the steps in the Click Guide. If you do not end up with a live site, reply to any email from me within 30 days of buying and I will refund you in full. No hoops.</li>
<li>The Overlay Agency: 30 days. If the guide is not useful to you, reply to any email from me within 30 days.</li>
<li>Any other paid product: the window on its page, 14 to 90 days.</li>
</ul>
<h2>If something is broken</h2>
<p>If a product is broken, missing or not what I described, email me within its refund window and I will make it right or refund you.</p>
<h2>How to ask</h2>
<p>Email <a href="mailto:{MAIL}">{MAIL}</a> from the address you used to buy, with your order details. Refunds go back to your original payment method through the payment processor and usually show up within 5 to 10 business days, depending on your bank.</p>
<h2>Free tools</h2>
<p>Free tools cost nothing, so there is nothing to refund.</p>"""),
 "earnings-disclaimer": ("Earnings Disclaimer", "No promise of income or results.", """
<p>I teach simple ways to write offers, copy and posts, and to build a basic website with an AI assistant. I cannot and do not promise that you will make any sales or any money.</p>
<ul class="bullets"><li>Any example, number or story on this site is for illustration, not a promise or a typical result.</li>
<li>Your results depend on your effort, your offer, your market, your skills and many things I cannot control.</li>
<li>Some people who follow my material will make no money.</li>
<li>Nothing here is legal, tax, financial or investment advice. Talk to a qualified professional for that.</li></ul>
<p>You are responsible for your own decisions and results.</p>"""),
 "contact": ("Contact", "How to reach Rob Reece.", """
<p>Questions, refund requests or privacy requests? Email me.</p>
<p><a class="btn" href="mailto:{MAIL}">{MAIL}</a></p>
<p>I read every message myself and usually reply within a couple of business days.</p>
<p>{BIZ}</p>{ADDR}"""),
}

def build(root, dist, layout, site):
    addr = site.get("business_address", "")
    paths = []
    for slug, (title, desc, body) in PAGES.items():
        inner = body.replace("{BIZ}", BIZ).replace("{MAIL}", MAIL).replace("{ADDR}", f"<p>{e(addr)}</p>" if addr else "")
        page = f'<section class="res"><div class="wrap narrow"><span class="mono">Legal</span><h1>{e(title)}</h1><p class="sub">Last updated {UPDATED}</p>{inner}{links.legal_nav(None, slug)}</div></section>'
        d = dist / slug; d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(layout(f"{title} | Rob Reece", desc, page, f"/{slug}/"))
        paths.append(f"/{slug}/")
    return paths
