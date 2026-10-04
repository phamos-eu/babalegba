# SEO and AI Friendliness Checklist

Walk through every applicable item before declaring a website task complete. Report any item that cannot be verified and why.

## Per-Page SEO

- [ ] Unique <title>, roughly 50–60 characters, descriptive, front-loaded keywords.
- [ ] Unique meta description, roughly 150–160 characters, accurately summarizing the page.
- [ ] Canonical URL present and correct.
- [ ] Exactly one h1; heading hierarchy (h1 → h2 → h3) mirrors content outline; no skipped levels.
- [ ] Semantic landmarks: header, nav, main, footer each used once per page.
- [ ] Open Graph tags: og:title, og:description, og:image, og:url, og:type.
- [ ] Twitter card tag present.
- [ ] All images have meaningful alt text, explicit dimensions, optimized size.
- [ ] Internal links use descriptive anchor text; important pages linked from related pages.
- [ ] No broken internal or external links.
- [ ] noindex on utility, thank-you, or staging pages; indexable pages clean of it.

## Structured Data

- [ ] Organization JSON-LD on home page (name, logo, URL, contact, social profiles).
- [ ] WebSite JSON-LD on home page.
- [ ] BreadcrumbList on nested pages.
- [ ] Most specific applicable type per page (Product, Service, Article, FAQPage, ContactPage, …).
- [ ] Markup only for content actually visible on the page.
- [ ] Validated with Google's Rich Results Test (report the result).

## Site-Level SEO

- [ ] sitemap.xml contains all public routes and excludes utility routes.
- [ ] robots.txt present; does not block CSS/JS assets; sitemap referenced.
- [ ] Staging or draft sites excluded from indexing; production fully indexable.
- [ ] Old URLs that changed have 301 redirects (Redirect records or web server config).
- [ ] 404 behavior verified: serves a proper 404 status code with a helpful page.
- [ ] Assets bundled and minified via bench build; no render-blocking scripts above the fold.
- [ ] Mobile rendering verified; no horizontal scrolling; tap targets adequate.

## AI Friendliness (GEO/AEO)

- [ ] llms.txt published at site root following the llmstxt.org convention.
- [ ] AI crawlers (GPTBot, ClaudeBot, PerplexityBot, and similar) allowed in robots.txt unless the client prohibits it.
- [ ] All substantive content present in server-rendered HTML, not behind JavaScript.
- [ ] Answer-first content structure: direct answer or summary first, then detail.
- [ ] Clean, readable prose in semantic HTML; no content trapped in images or canvases.
- [ ] Stable, descriptive slugs; no ID-based URLs.

## Multilingual (when applicable)

- [ ] Language path structure (e.g., /de/, /en/) consistent and documented.
- [ ] <html lang="…"> matches each page's language.
- [ ] hreflang alternates for every language variant plus x-default, all self-consistent.
- [ ] Meta titles, descriptions, JSON-LD, and llms.txt localized per language.
- [ ] Language switcher points to the equivalent page, not the other language's home page.

## AI-Researcher Friendliness (human readers)

- [ ] App README documents the page inventory, route map, language structure, and deliberate deviations.
- [ ] Templates and context functions carry brief purpose comments.
- [ ] File, template, and variable names are descriptive.
- [ ] No orphaned or unused templates left behind after refactoring.

## Design (frappe-ui standards)

- [ ] Visual language follows the frappe-ui design system in spirit: restrained palette, consistent spacing, accessible contrast (WCAG AA minimum).
- [ ] Branding implemented via Website Theme (SCSS variables), not scattered inline styles.
- [ ] Reused Frappe built-ins wherever possible; no new CSS/JS framework introduced.
- [ ] Reusable markup extracted into Web Templates instead of duplicated per page.
