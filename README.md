# robcreece.com static site
Add a lead magnet: add an entry to pages.json (copy one), create an Emailit embed form (duplicate an existing one,
set redirect to https://robcreece.com/thanks/<slug>/), paste its public token into form_token, set delivery_url,
run `python3 build.py`, upload dist/ contents.
