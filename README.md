# jupiterlaser.com — Site Redesign

Complete redesign of **Jupiter Laser & Regenerative Medicine** (Abacoa Podiatry & Leg Vein Center's advanced-treatment division). Fully static, framework-free, deployable on any host — built for speed, conversions, and search.

## What's in the box

- **33 pages**: home, 5 service pages + hub, 8 condition pages + hub, 45+ question FAQ, blog with 4 articles, about/doctor/technology/reviews/service-areas cluster, new patients, contact, telehealth, privacy, accessibility, 404
- **Interactive features**: "Where does it hurt?" clickable foot map, 5-question treatment-fit quiz, live FAQ search + category filters, testimonial slider, animated counters, scroll-reveal animations, mobile call bar (sticky Call Now / Book Online)
- **SEO**: unique titles/descriptions, canonical URLs, JSON-LD on every page (MedicalClinic, Physician, MedicalCondition, MedicalTherapy, FAQPage, BlogPosting, BreadcrumbList), OpenGraph/Twitter cards + generated share image, `sitemap.xml`, `robots.txt`, `llms.txt` for AI assistants, geo meta for local search
- **Migration safety**: legacy URLs preserved or 301-redirected — see [`MIGRATION.md`](MIGRATION.md) **(read this before launch)**

## Structure

```
_src/
  template.html      shared chrome (head, header, nav, footer, sitewide schema)
  build.py           builds pages → site root, generates sitemap + redirects
  og_image.py        regenerates assets/img/og-image.png (needs Pillow)
  pages/*.html       one file per page: JSON meta block + body HTML
assets/
  css/main.css       the whole design system
  js/main.js         all interactivity (vanilla JS, no dependencies)
  img/               logo, favicon, og-image
<page folders>/      generated output — pretty URLs (/services/mls-laser-therapy/)
```

## Editing

1. Edit a file in `_src/pages/` (or `_src/template.html` for header/footer changes)
2. Run `python3 _src/build.py`
3. Commit both the source and the regenerated output

Preview locally: `python3 -m http.server 8000` → http://localhost:8000
(Absolute paths mean the site must be served from a root, not a subfolder — any real host, Netlify, or a custom-domain GitHub Pages setup works.)

## Deploying

**This repo deploys to Vercel** — project `abacoapodiatry` under the `thedesignofman` team, git-connected to `Design-of-Man/abacoapodiatry`.

- Production branch is **`main`**. Pushing to `main` deploys to production; any other branch gets a preview URL.
- **There is no build command.** Vercel serves the committed repo root as static files. `python3 _src/build.py` runs on *your* machine and its output is committed — see [Editing](#editing). A push whose generated pages weren't rebuilt and committed ships the old pages.
- `vercel.json` carries the 301s and security/cache headers. `_redirects` (Netlify) and `.htaccess` (Apache) are kept in sync for portability but are inert on Vercel.

The site remains a plain static bundle, so any static host still works. For GitHub Pages, use a **custom domain** — project-subpath URLs would break the absolute links.

## ⚠️ Pre-launch checklist (do these before pointing the domain)

Ordered by what cannot be undone if it is missed.

- [ ] **Secure Search Console ownership *before* the current SEO/Ads vendor is terminated.**
      Add owner-level verification on the `jupiterlaser.com` property via a **DNS TXT
      record** — it survives the host change, an HTML-file or meta-tag method does not.
      Do not delete or recreate the property; it holds the history this whole migration
      exists to protect. If the vendor owns the only verification and leaves first, that
      history is not recoverable. See [`MIGRATION.md`](MIGRATION.md) step 2.
- [ ] **Crawl the old site and close the redirect map.** The 19 redirects in `vercel.json`
      came from search research, not from a crawl, so any URL that ranks today and is not
      in that map will 404 on launch. This is the only remaining item that can actually
      cost rankings — [`MIGRATION.md`](MIGRATION.md) step 1 has the command.
- [ ] **Read [`MIGRATION.md`](MIGRATION.md)** — the no-lost-leads cutover plan
- [ ] **Verify office hours with the office.** The site, `llms.txt` and the schema's
      `openingHoursSpecification` all currently say Mon–Thu 8 AM–5 PM, Fri 8 AM–2 PM,
      closed for lunch 12:30–1:30. Those came from research, not from the practice.
      Confirm them, and if they are wrong update `_src/template.html`,
      `_src/pages/faq.html`, `llms.txt` and the schema together — four places, easy to
      half-fix.
- [ ] **Replace the patient testimonials on `_src/pages/reviews.html`** (marked
      `LAUNCH TODO`) with verified reviews used with permission — Google Business Profile
      reviews are ideal: public, attributable and already in the practice's name. The
      homepage block was removed for the same reason and can come back once verified.
      **This gates the cutover.** Publishing patient testimonials that cannot be sourced
      is not a polish item for a medical practice.
- [ ] **Enable Web Analytics** on the Vercel project. The lead instrumentation
      (`call_click`, `form_submit`, `appointment_cta`) is live in `assets/js/main.js` but
      collects nothing until the toggle is on; custom events need a Pro plan. Turn it on
      *before* cutover so there is a pre-launch baseline to compare against.
- [ ] **Confirm services offered** (telehealth page, PRP, stem cell) match what the practice currently offers
- [x] ~~Add real photos~~ — Dr. Cedeno, Dr. Mustafa and the logo are installed.
- [ ] **Remaining photos**: drop `office.jpg` and `mls-laser.jpg` into
      `assets/img/photos/` (see the README there for sizes). Both are referenced but
      absent; the gold monogram fallback in `assets/css/main.css` covers them, so they
      degrade rather than break. `dr-cedeno.jpg` is already in the repo.
- [x] ~~**Make the hero video durable.**~~ Done — the encodes are committed under
      `assets/video/` (desktop + mobile, MP4 and WebM), so no deploy-time fetch is
      involved. `_src/vercel-build.sh` and its `HERO_VIDEO_URL` variable are dead
      leftovers from the Dropbox approach; nothing runs them (there is no build
      command) and the variable is not read anywhere.
- [x] ~~**Wire the contact form.**~~ Done — `_src/pages/contact.html` posts to
      `formsubmit.co/ajax/AbacoaPodiatry@gmail.com`. There is no `YOUR_FORM_ID`
      left anywhere in the repo, and `assets/js/main.js` fires the `form_submit`
      analytics event only on a confirmed send.
- [ ] Update `sameAs` links in `_src/template.html` with the practice's real Facebook/Instagram/Google Business Profile URLs
- [ ] Rebuild (`python3 _src/build.py`) after any of the above
