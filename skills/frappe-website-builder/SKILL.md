---
name: frappe-website-builder
description: Load this skill when building or editing public-facing websites on the Frappe Framework / ERPNext v15 — marketing sites, landing pages, or multilingual web portals using the classic server-rendered website module (Jinja www pages, Web Templates, Website Settings, Website Theme). Enforces reuse of built-in Frappe elements over new ones, SEO best practices for high Google scores, and design that is useful to AI crawlers and human AI researchers alike.
---

# Frappe Website Builder

Build fast, SEO-strong, AI-friendly websites on the Frappe Framework v15 using the classic server-rendered website module — never a client-side SPA for public content.

## Core Principle: Reuse, Do Not Reinvent

Before writing any new component, check what the framework already provides. In order of preference:

1. Built-in doctypes and configuration: Website Settings, Website Theme, Web Page, Web Template, Redirect, Banner.
2. Built-in Jinja infrastructure: the base.html template block system, standard web templates shipped with Frappe, available Jinja global functions and macros.
3. Existing app assets and previously created web templates in the target app.
4. Only then: new files — and when new files are unavoidable, follow the established structure exactly.

Never introduce a new CSS framework, JavaScript framework, or component library into the website module. If the user explicitly asks for a Vue/frappe-ui portal, treat that as an application project, not a website project, and say so.

## Architecture

- Websites live in a custom Frappe app, version controlled, never as modifications to frappe or erpnext core.
- Public pages are Jinja templates in the app's www/ directory. Each page is <name>.html (or .md for content-heavy pages) with an optional <name>.py exposing get_context(context).
- All templates extend the site's base template and fill its defined blocks (typically title, meta, breadcrumbs, page_content, script, style). Do not build standalone HTML shells.
- Reusable markup is implemented as Web Templates (doctype records or standard templates in the app's templates/ directory) and included via the framework's include mechanisms.
- Route mapping goes in hooks.py under website_route_rules; keep URLs clean, lowercase, hyphenated, and stable. Breaking an old URL requires a Redirect record or a 301 in the web server configuration.
- Branding, colors, and typography go into a Website Theme (SCSS variables and includes), not scattered inline styles. Keep the visual language aligned with the frappe-ui design system (frappeui.com) in spirit: restrained color palette, consistent spacing scale, accessible contrast.
- If uncertain about a v15 API or template block, verify against the curated links in references.md before inventing a mechanism.

## SEO Requirements (Google)

Every public page must satisfy:

- Unique, descriptive <title> (roughly 50–60 characters) via the title block or context.
- Unique meta description (roughly 150–160 characters) describing the page's actual content.
- Canonical URL on every page; noindex on non-indexable or utility pages.
- Semantic HTML5 structure: one header, one nav, one main, one footer per page; exactly one h1; hierarchical headings that mirror the content outline.
- Open Graph and Twitter card tags for social sharing.
- Descriptive anchor text for internal links; no "click here". Internal links from every page to the most important pages.
- Images with meaningful alt text, explicit dimensions, and optimized file sizes.
- sitemap.xml: Frappe generates it automatically from published pages — verify after deployment that all public routes appear and utility routes do not.
- robots.txt served from a www/robots.txt template; do not block CSS or JS assets; explicitly allow reputable AI crawlers (see below).
- Performance: rely on server-rendered HTML, bench build for bundled/minified assets, avoid render-blocking resources, keep third-party scripts to a minimum.

## Structured Data (JSON-LD)

Inject schema.org JSON-LD through the page context into the meta/head area:

- Organization (or LocalBusiness where applicable) on the home page, with name, logo, URL, contact, and social profiles.
- WebSite with the site name on the home page.
- BreadcrumbList on nested pages.
- The most specific applicable type per page: Product, Service, Article, FAQPage, ContactPage, etc.
- Validate every deployed page with Google's Rich Results Test and keep the markup truthful — never mark up content that is not visible on the page.

## AI Friendliness

Optimize for both machine and human "AI researchers":

For AI crawlers and generative engines (GEO/AEO):
- Publish www/llms.txt following the llmstxt.org convention: site overview and structured, curated links to key pages in Markdown. Optionally link an llms-full.txt with the complete flattened content.
- Allow AI crawlers (GPTBot, ClaudeBot, PerplexityBot, and similar) in robots.txt unless the client prohibits it.
- Serve all substantive content as plain server-rendered HTML; nothing important may exist only behind JavaScript.
- Write answer-first content: lead with the direct answer or summary, then detail. Use clear headings, short paragraphs, lists, and tables where they carry structure.
- Keep prose in clean semantic HTML; avoid content trapped in images, canvases, or unlabeled widgets.
- Keep URLs stable and readable; descriptive slugs over IDs.

For human AI researchers and future developers:
- Keep the app structured along framework conventions so any Frappe developer can navigate it.
- Every page's get_context and every custom template carries a brief comment explaining its purpose and data sources.
- Maintain a README in the app documenting the site's page inventory, route map, language structure, and any deliberate deviation from this skill's defaults.
- Name files, templates, and context variables descriptively; no cryptic abbreviations.

## Multilingual (DE/EN default)

- Structure content under language path prefixes (for example /de/… and /en/…) using www/ subdirectories plus website_route_rules, or one page tree with translated counterparts linked explicitly — choose one pattern per project and document it.
- Set the site default language in Website Settings; translate UI strings with Frappe's translation mechanism (__() in Jinja and Python, translation exports via bench).
- Localize slugs; do not machine-translate URL segments.
- Every page must declare its language (<html lang="…">) and carry hreflang alternate links to all language variants plus x-default.
- Localize meta titles, descriptions, JSON-LD, and llms.txt content — never leave one language's metadata on the other's pages.

## Workflow

1. Clarify the site's purpose, audience, and target language(s) if not already known.
2. Inspect the existing app before creating anything: list current www/ pages, web templates, themes, and hooks. Reuse before creating.
3. Build page by page: context function, template extending the base template, content, meta block, JSON-LD.
4. Wire global elements: Website Settings (brand, footer, header items), Website Theme, robots.txt, llms.txt, redirects.
5. Before declaring the work complete, walk through seo-ai-checklist.md and verify every applicable item; fix gaps or report them explicitly.
6. Use references.md for bench commands, verification steps, and the curated official documentation links.
