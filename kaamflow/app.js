const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const modal = $("#jobModal");
const form = $("#jobForm");
const toast = $("#toast");
let toastTimer;
let jobNumber = 1048;

const dateInputValue = date => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
};
const formatJobDate = value => {
  if (!value) return "Date not set";
  return new Date(`${value}T00:00:00`).toLocaleDateString("en-US", {month:"short", day:"numeric", year:"numeric"});
};
const today = new Date();
$("#todayLabel").textContent = today.toLocaleDateString("en-US", {weekday:"long", day:"numeric", month:"long", year:"numeric"}).toUpperCase();
$("#scheduleDate").textContent = today.toLocaleDateString("en-US", {weekday:"long", month:"long", day:"numeric"});
$("#jobDate").value = dateInputValue(today);

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 2800);
}
function openModal() {
  modal.classList.remove("hidden");
  document.body.style.overflow = "hidden";
  setTimeout(() => $('input[name="title"]', form).focus(), 50);
}
function closeModal() {
  modal.classList.add("hidden");
  document.body.style.overflow = "";
}
$("#newJobBtn").addEventListener("click", openModal);
$("#secondaryAction").addEventListener("click", openModal);
$("#closeModal").addEventListener("click", closeModal);
$("#cancelModal").addEventListener("click", closeModal);
modal.addEventListener("click", e => { if (e.target === modal) closeModal(); });
document.addEventListener("keydown", e => {
  if (e.key === "Escape") closeModal();
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
    e.preventDefault();
    $("#globalSearch").focus();
  }
});

function statusClass(status) {
  if (status === "In progress") return "status-progress";
  if (status === "Scheduled") return "status-scheduled";
  if (status === "Completed") return "status-complete";
  return "status-pending";
}
function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
}
function addJobRow(job) {
  const row = document.createElement("tr");
  const id = "KF-" + (++jobNumber);
  row.dataset.search = [job.title, job.customer, id, job.status].join(" ").toLowerCase();
  row.innerHTML = `<td><div class="job-cell"><span class="job-symbol repair">✧</span><span><b>${escapeHtml(job.title)}</b><small>#${id}</small></span></div></td>
    <td><div class="customer-cell"><b>${escapeHtml(job.customer)}</b><small>New customer</small></div></td>
    <td>${escapeHtml(formatJobDate(job.date))}</td><td><span class="status ${statusClass(job.status)}">${escapeHtml(job.status)}</span></td>
    <td class="amount">$ ${Number(job.amount).toFixed(2)}</td><td><button class="more-button" aria-label="More options">•••</button></td>`;
  $("#jobsTable").prepend(row);
  const count = Number($("#jobNavCount").textContent) + 1;
  $("#jobNavCount").textContent = count;
  $("#totalJobs").textContent = Number($("#totalJobs").textContent) + 1;
}
form.addEventListener("submit", event => {
  event.preventDefault();
  const data = new FormData(form);
  const job = Object.fromEntries(data.entries());
  addJobRow(job);
  form.reset();
  closeModal();
  showToast("Job created successfully — demo data only.");
});
$$("[data-page]").forEach(link => link.addEventListener("click", event => {
  const page = link.dataset.page;
  if (!page) return;
  event.preventDefault();
  if (page === "overview") {
    $("#overviewPage").classList.remove("hidden");
    $("#secondaryPage").classList.add("hidden");
    $("#breadcrumbPage").textContent = "Overview";
  } else {
    const titles = {jobs:"Jobs",calendar:"Schedule",customers:"Customers",quotes:"Quotes & invoices",reports:"Reports",settings:"Settings"};
    const descriptions = {jobs:"Manage every job from request to completion.",calendar:"See appointments and plan your team's day.",customers:"Keep customer details and service history together.",quotes:"Create quotes and keep track of invoice payments.",reports:"Understand how your service business is performing.",settings:"Manage your workspace preferences."};
    $("#overviewPage").classList.add("hidden");
    $("#secondaryPage").classList.remove("hidden");
    $("#secondaryTitle").textContent = titles[page] || "Workspace";
    $("#breadcrumbPage").textContent = titles[page] || "Workspace";
    $("#secondaryDescription").textContent = descriptions[page] || "Manage your workspace.";
    $("#secondaryMessage").textContent = (titles[page] || "Workspace") + " workspace";
  }
  $$(".nav-link").forEach(item => item.classList.toggle("active", item.dataset.page === page));
  $("#sidebar").classList.remove("open");
  window.scrollTo({top:0,behavior:"smooth"});
}));
$("#mobileMenu").addEventListener("click", () => $("#sidebar").classList.toggle("open"));
$("#globalSearch").addEventListener("input", event => {
  const query = event.target.value.trim().toLowerCase();
  let shown = 0;
  $$("#jobsTable tr").forEach(row => {
    const text = (row.dataset.search || row.innerText).toLowerCase();
    row.hidden = query && !text.includes(query);
    if (!row.hidden) shown++;
  });
  if (query) {
    $("#overviewPage").classList.remove("hidden");
    $("#secondaryPage").classList.add("hidden");
    $("#breadcrumbPage").textContent = "Search";
    if (shown === 0) showToast("No matching jobs found.");
  } else if ($("#breadcrumbPage").textContent === "Search") {
    $("#breadcrumbPage").textContent = "Overview";
  }
});
$("#exportBtn").addEventListener("click", () => {
  const rows = [["Job","Customer","Date","Status","Amount"]];
  $$("#jobsTable tr").forEach(row => {
    const cells = $$("td", row);
    if (cells.length && !row.hidden) rows.push([
      cells[0].innerText.replace(/\n/g," "),
      cells[1].innerText.replace(/\n/g," "),
      cells[2].innerText,
      cells[3].innerText,
      cells[4].innerText
    ]);
  });
  const csv = rows.map(row => row.map(value => '"' + String(value).replace(/"/g,'""') + '"').join(",")).join("\n");
  const blob = new Blob([csv], {type:"text/csv;charset=utf-8;"});
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url; anchor.download = "kaamflow-jobs-demo.csv"; anchor.click();
  URL.revokeObjectURL(url);
  showToast("Demo job report exported.");
});
$("#chartRange").addEventListener("change", event => {
  showToast(event.target.value === "six" ? "Showing the last 6 months (sample chart)." : "Showing this year (sample chart).");
});
document.addEventListener("click", event => {
  if (event.target.closest(".more-button")) showToast("More job actions will be available in a future version.");
});
