# EMAIL ADD-ON: MODULE C PROMPT

Use after your site is live on your own domain. Paste into the same Claude chat (or a new one) and say which email tool you chose.

---

Stage 6, Email. My domain is [YOUR DOMAIN]. My email tool is [TOOL]. My freebie page is [LINK].

Follow my rules: never type my passwords or codes, ask before anything irreversible, don't invent facts, keep a control sheet.

1. **Audit first.** Look up the current DNS records for my domain. List which ones relate to email (MX, SPF, DKIM, DMARC). Tell me if I already have an email provider on this domain. If so, plan to coexist with it: only one SPF record is allowed, so merge instead of adding a second.
2. **Add sending records** the tool asks for. Show me each record before you add it. Mark email records "DNS only" if the domain is on Cloudflare. After adding, run the tool's verify button and tell me the result.
3. **DMARC.** Start with a monitoring policy (p=none) and an address I can read. Explain in one line what it does.
4. **Form.** Create a signup form. Set its redirect to my thank-you page. Add the form's embed code to my freebie page and rebuild the site.
5. **Verification.** If the tool says my workspace is unverified, fill in the request honestly: how people opt in, what I send, rough volume. Stop before the compliance checkboxes so I can tick them.
6. **Emails.** Write the delivery email and a 5-email welcome series using the templates I give you (below). Adjust to my voice. Keep one idea per email. Include an unsubscribe link in every one.
7. **Test.** Send a test to me only. Wait for me to confirm it arrived and isn't in spam. Then set up the automation.
8. **Handover.** Tell me what is live, what is waiting on approval, and how to check results.

## Welcome series templates (edit to your voice, fill the [BRACKETS] with real details)

**Email 1 (right after signup). Subject: Your [FREEBIE NAME] is here**
Hi [FIRST NAME],
Here's your [FREEBIE NAME]: [LINK].
Start with [ONE THING TO DO FIRST]. It takes about [TIME].
One question: what are you trying to get done right now? Just hit reply. I read every one.
[YOUR NAME]

**Email 2 (day 1). Subject: Did it work?**
Quick check. Did you get to try [FREEBIE NAME]?
The most common sticking point is [COMMON PROBLEM]. The fix is [FIX].
If you're stuck on something else, reply and tell me where.

**Email 3 (day 3). Subject: The mistake I made**
[ONE TRUE STORY about a mistake you made in this area, 4 to 6 sentences, with a real detail.]
What I do now: [LESSON].

**Email 4 (day 5). Subject: One small thing to try this week**
[ONE SPECIFIC ACTION they can do in 15 minutes, with an example.]

**Email 5 (day 7). Subject: Where to go from here**
Recap in two lines.
If you want more help with [PROBLEM], here is [YOUR OFFER, with an honest description and price].
If it's not for you, no problem. Keep the free stuff.

Rules for your emails: no fake urgency, no income claims, no testimonials you can't prove, one unsubscribe link in each.
