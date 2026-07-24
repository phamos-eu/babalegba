# Babalegba

**Babalegba** is a collective knowledge base app for Frappe and ERPNext development.
It serves as a centralized platform where users can:

- Share **ideas, findings, and solutions** to keep knowledge confined within the team.
- Collaborate on **requirements**, refining them from simple to complex solutions.
- Work **independently of specific AI providers** by centralizing knowledge.
- Enable **novices to access expert knowledge** without direct interaction.

The app will be installed on a central system where all team members can contribute.

---

## Frappe v16 Compatibility
This app is designed for **Frappe Framework v16**. Follow the [official documentation](https://frappeframework.com/docs/user/en) for development.

### Adding Features
To extend this app, you can add:

1. **DocTypes** in `babalegba/doctype/{doctype}/`:
   - `{doctype}.json` (metadata)
   - `{doctype}.py` (server logic)
   - `{doctype}.js` (client logic)

2. **API Endpoints** in `babalegba/api/{module}.py`.

3. **Translations** in `babalegba/translations/de.csv`:
   - Use `_("...")` for Python strings.
   - Use `__("...")` for JavaScript strings.

---

## License
This app is licensed under the **GNU Affero General Public License v3 (AGPLv3)**.
See [license.txt](license.txt) for the full license text.
