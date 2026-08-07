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

Any static host. Recommended: **Netlify** (drag-and-drop or connect this repo; `_redirects` handles the 301s automatically) or Apache-style hosting (`.htaccess` included). For GitHub Pages, use a **custom domain** (project-subpath URLs would break absolute links).

## ⚠️ Pre-launch checklist (do these before pointing the domain)

- [ ] **Read [`MIGRATION.md`](MIGRATION.md)** — the no-lost-leads cutover plan
- [ ] **Verify office hours** — the site says Mon–Fri 8:30 AM–5:00 PM (taken as a best guess; confirm with the office and update `_src/template.html` + `_src/pages/faq.html` + schema if different)
- [ ] **Replace placeholder testimonials** on the home page, reviews page (marked with `LAUNCH TODO` comments in `_src/pages/home.html` and `_src/pages/reviews.html`) with real patient reviews used with permission
- [ ] **Wire the contact form**: create a free form at formspree.io and replace `YOUR_FORM_ID` in `_src/pages/contact.html` (until then, the form politely tells visitors to call)
- [ ] **Confirm services offered** (telehealth page, PRP, stem cell) match what the practice currently offers
- [ ] **Add real photos** when available — office, staff, Dr. Cedeno headshot (currently initials avatar), the MLS laser
- [ ] Update `sameAs` links in `_src/template.html` with the practice's real Facebook/Instagram/Google Business Profile URLs
- [ ] Rebuild (`python3 _src/build.py`) after any of the above
