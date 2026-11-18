# KaamFlow — Frontend Demo

KaamFlow is a frontend-first job and customer workspace concept for small service businesses: repair technicians, electricians, plumbers, cleaning teams and similar operators.

## Included in this version

- Responsive business dashboard
- Summary cards for jobs, revenue, pending payments and completion
- Recent jobs table and today's schedule
- Business performance chart (illustrative sample data)
- Recent activity feed
- Create-job modal with form validation
- Browser-side job row insertion and counters
- Search across demo jobs with Ctrl/Cmd + K shortcut
- Live date labels and current-date default for new jobs
- CSV export of visible (filtered) job rows
- Secondary navigation sections for jobs, schedule, customers, quotes/invoices, reports and settings

## Run locally

No build tools or package installation are required.

1. Download or clone this repository.
2. Open the `kaamflow/` folder.
3. Open `index.html` in a modern browser.

For a more consistent local preview, use the VS Code Live Server extension, or any static file server.

## Important demo limitations

This is a frontend prototype only. It does not include a backend, database, authentication, real payment processing, live WhatsApp messaging, or cloud persistence. New jobs are added in the current page session and are not stored permanently. Dashboard figures and chart values are sample data for demonstration.

## Project structure

```
kaamflow/
├── index.html
├── styles.css
├── app.js
└── README.md
```

## Product direction

The intended workflow is:

Customer request → quote and appointment → job execution → before/after proof → invoice → payment follow-up.

Future versions can add role-based access, persistent storage, customer history, real calendar integrations and messaging after the product requirements and infrastructure are decided.
