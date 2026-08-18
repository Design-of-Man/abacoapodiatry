# Disabled pages

`build.py` only globs `_src/pages/*.html`, so anything parked here is kept in
the repo, kept in git history, and simply not built or published.

## services-stemcell.html

Pulled from the live site on 2026-08-18 at Dr. Cedeno's request. His stated
reason was that it "pushes the site down on Google"; the sharper reasons to
keep it down are that stem-cell clinic marketing is an active FDA/FTC
enforcement area, and that Google Ads restricts unproven cellular therapies --
which matters because running ads is on the roadmap.

It is parked rather than deleted because he asked for it back "on standby" for
when he wants it edited.

### Putting it back

1. `git mv _src/pages-disabled/services-stemcell.html _src/pages/`
2. Remove the `/services/stem-cell-therapy` row from `_src/redirect-map.tsv` --
   `build.py` hard-fails if a redirect source is also a built page, which is the
   check that stops a page shipping to a URL that 301s away from it.
3. Repoint the inbound links currently aimed at `/services/regenerative-medicine/`
   back, if that is wanted: `home.html`, `faq.html`, `technology.html`,
   `services-index.html`, `services-regen.html`, both `post-stem-cell-*.html`,
   `template.html` (two nav entries), `assets/js/assistant.js`, `llms.txt`.
4. Rebuild and run `_dev/preflight.py`.
