# References: Commands, Verification, and Documentation Links

## Bench Commands

| Task | Command |
|---|---|
| Create a new app | bench new-app <app_name> |
| Install app on site | bench --site <site> install-app <app_name> |
| Start development server | bench start |
| Build bundled assets | bench build --app <app_name> |
| Clear cache | bench --site <site> clear-cache |
| Migrate (after doctype changes) | bench --site <site> migrate |
| Export translations | bench --site <site> get-untranslated de / bench --site <site> update-translations |

Note: within a sandboxed AI environment a live bench may not be available. If no bench is reachable, produce correct file content for the app repository and clearly tell the user which commands to run in their bench.

## Verification Steps

1. bench start and open the site; verify each page renders fully server-side (view page source; all content must be present without JavaScript).
2. Fetch /sitemap.xml and /robots.txt and check their contents.
3. Run Google's Rich Results Test and a PageSpeed Insights check per key template; report scores.
4. Test both languages (when applicable): route resolution, hreflang consistency, localized metadata.
5. Crawl internal links (for example with a link checker) to catch 404s and redirect chains.

## Curated Documentation Links

Verify framework behavior against these before inventing mechanisms or when uncertain about a v15 API:

- Website module overview: https://docs.frappe.io/framework/user/en/website
- Web pages and templates (Jinja, www directory, get_context): https://docs.frappe.io/framework/user/en/website/page
- Web Templates: https://docs.frappe.io/framework/user/en/website/web-template
- Website Settings: https://docs.frappe.io/framework/user/en/website/website-settings
- Website Theme (SCSS): https://docs.frappe.io/framework/user/en/website/website-theme
- Routing and hooks (website_route_rules): https://docs.frappe.io/framework/user/en/website/routing
- Translations: https://docs.frappe.io/framework/user/en/translations
- frappe-ui design system: https://frappeui.com
- llms.txt convention: https://llmstxt.org
- Google Search Central (SEO fundamentals): https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Google structured data documentation: https://developers.google.com/search/docs/appearance/structured-data
- Google Rich Results Test: https://search.google.com/test/rich-results
- PageSpeed Insights: https://pagespeed.web.dev

If a link above has moved, search docs.frappe.io for the topic name rather than guessing API behavior.
