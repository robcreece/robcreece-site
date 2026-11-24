# Adding a video page
1. Copy the example entry in videos.json, set "draft": false.
2. Fill in: title, h1, desc (under 155 chars), youtube_id (the part after v=), date, duration (ISO, e.g. PT8M30S), magnet (a freebie slug), summary, takeaways, chapters [[seconds,"label"]], body, faq, transcript.
3. Run `python3 build.py` and push. The page gets the embed, VideoObject/BlogPosting/FAQ schema, sitemap entry and a freebie CTA automatically.
