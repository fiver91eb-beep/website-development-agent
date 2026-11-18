# KaamFlow — Manual QA Checklist

Run the static prototype by opening `index.html` in a modern browser.

## Navigation
- [ ] Overview opens by default.
- [ ] Jobs, Schedule, Customers, Invoices, Reports and Settings open from the sidebar.
- [ ] Current page label and active navigation item update.
- [ ] Mobile menu opens and closes the sidebar.

## Jobs
- [ ] Recent jobs render on the overview.
- [ ] Jobs page search filters by job title, customer and ID.
- [ ] Status filter narrows the list.
- [ ] Create-job modal opens and closes.
- [ ] Required fields prevent an empty job submission.
- [ ] Saving a job adds it to the list and updates the navigation count.
- [ ] Job status action changes the selected job status.
- [ ] Created jobs remain after refreshing the same browser.

## Customers and schedule
- [ ] Customer cards are derived from the job sample data.
- [ ] Calendar view displays the November 2026 sample month.
- [ ] Schedule data is presented clearly on desktop and mobile.

## Invoices and reports
- [ ] Invoice rows are generated from sample jobs.
- [ ] Print action opens a printable invoice preview (allow pop-ups).
- [ ] CSV export downloads a CSV file.
- [ ] Reports clearly indicate that the metrics are illustrative demo figures.

## Responsive and accessibility checks
- [ ] Layout works at desktop, tablet and narrow mobile widths.
- [ ] Buttons and form fields can be reached by keyboard.
- [ ] Modal has dialog semantics and a visible close control.
- [ ] Toast feedback is announced through a live region.

## Release note
This is a manual checklist. Do not mark an item as passed until it has been tested in a browser on the target device.
