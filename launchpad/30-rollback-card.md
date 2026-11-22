# ROLLBACK CARD: UNDO THE DOMAIN SWITCH IN 2 MINUTES

Use this if your site or email stops working after switching nameservers.

1. Open the website where you bought the domain (your registrar). Go to the domain's Nameservers setting.
2. Choose "I'll use my own nameservers" or "Custom", and enter the two nameservers you wrote down **before** the change. (Claude lists them in your control sheet. Save them somewhere safe.)
   If you didn't save them, the registrar's default nameservers are usually shown as "Use default" or "Registrar nameservers". Choose that.
3. Save. It can take from minutes to a few hours to take effect.
4. In the meantime, your free address (yourname.workers.dev) keeps working. Only the custom domain is affected.
5. Tell Claude what happened and paste any error. It will compare your DNS records and fix what's missing.

Tips
- Switch nameservers when you have time to watch it, not right before a launch.
- Check that DNSSEC is off at your registrar before you switch (turning it on again later is optional).
- Keep a screenshot of your old DNS records.
