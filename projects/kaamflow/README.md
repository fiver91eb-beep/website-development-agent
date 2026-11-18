# KaamFlow — Service Business Workspace

KaamFlow is a responsive, frontend-only demo dashboard concept for local service businesses such as repair teams, electricians, plumbers, cleaning services and HVAC technicians.

## Demo features
- Business overview with jobs, completion, revenue and outstanding-payment summary cards
- Job manager with search and status filters
- Quote pipeline with sample estimates and interactive approval status
- Create-job modal with browser-local persistence
- Customer directory generated from demo jobs
- Monthly calendar view
- Sample invoice list, printable invoice view and CSV export
- Reports and workspace settings screens
- Responsive desktop and mobile layouts

## Run locally
No build step, package manager or backend is required.

1. Download or clone this repository.
2. Open `index.html` in a modern browser.

## Project files
- `index.html` — app structure and views
- `styles.css` — responsive styling
- `app.js` — sample data and demo interactions

## Documentation
- `PRODUCT-SPEC.md` — target users, problem hypothesis, workflow, scope, limitations, and validation plan
- `QA-CHECKLIST.md` — manual checks for navigation, jobs, quotes, customers, invoices, and responsive layouts

## Important demo limitations
This is a frontend prototype. It does not include authentication, a shared database, real payment processing, live WhatsApp messaging, server-side storage or multi-user synchronization. Jobs and quote approval updates in the demo are stored in the current browser using localStorage. All dashboard financial figures and customer records are illustrative sample data.

## Suggested next steps
1. Review the dashboard and mobile layout.
2. Replace sample business details and currency for the intended market.
3. Validate the workflow with a few real service-business owners.
4. Only after validating demand, plan integrations and a secure backend.

## License
No license has been added yet. Choose a license before distributing or selling the source code.