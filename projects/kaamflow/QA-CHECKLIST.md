# KaamFlow — Frontend QA Checklist

Use this checklist when opening the demo in a current desktop or mobile browser. The app is static HTML/CSS/JavaScript and does not require a build step.

## Launch
- [ ] Open `index.html` in a modern browser.
- [ ] Confirm the KaamFlow dashboard loads without a blank screen.
- [ ] Confirm the sidebar, top bar, metric cards, jobs table, schedule, and activity panels appear.
- [ ] Check the browser console for JavaScript errors.

## Navigation
- [ ] Open Overview.
- [ ] Open Jobs and return to Overview.
- [ ] Open Quotes, Schedule, Customers, Invoices, Reports, and Settings.
- [ ] Confirm the breadcrumb and page heading update for each view.
- [ ] On a narrow screen, open and close the mobile sidebar.

## Jobs
- [ ] Open Create new job.
- [ ] Try submitting with required fields empty; browser validation should prevent submission.
- [ ] Create a job with a title, customer, date, service type, and amount.
- [ ] Confirm the new job appears in the Jobs list and Overview.
- [ ] Search by job title and customer.
- [ ] Filter by each available job status.
- [ ] Change a job status using its row action.
- [ ] Refresh the page and confirm browser-local job data remains.

## Quotes
- [ ] Open Quotes.
- [ ] Confirm sample quotes and their statuses appear.
- [ ] Mark a quote as approved.
- [ ] Confirm its status updates.
- [ ] Refresh the page and confirm the demo approval remains in the same browser.

## Customers and schedule
- [ ] Open Customers and confirm customer cards are derived from job records.
- [ ] Open Schedule and confirm the sample month and job labels render.
- [ ] Check the calendar layout at desktop and mobile widths.

## Invoices and reports
- [ ] Open Invoices.
- [ ] Use Print on a sample invoice and confirm a print-preview window opens when pop-ups are allowed.
- [ ] Use Export CSV and confirm a CSV file downloads.
- [ ] Open Reports and confirm the page clearly labels figures as illustrative demo figures.

## Responsive layout and accessibility
- [ ] Check at approximately 1440px desktop width.
- [ ] Check at approximately 768px tablet width.
- [ ] Check at approximately 390px mobile width.
- [ ] Confirm there is no unintended horizontal page overflow.
- [ ] Use keyboard Tab to reach navigation links, buttons, and form fields.
- [ ] Confirm form labels and button accessible names are present.

## Known demo constraints
- Data is stored in the current browser using localStorage; it is not shared across users or devices.
- Sample figures are illustrative and are not calculated from a live business account.
- Quote approval is a local demo action only.
- Invoice print is a simple preview, not a tax-compliant invoice service.
- No real message, payment, or external API is sent.
