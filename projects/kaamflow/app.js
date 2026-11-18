const initialJobs = [
  {id:"KF-1042",title:"AC maintenance",service:"Maintenance",customer:"Olivia Rhye",date:"2026-11-18",time:"09:00 AM",location:"Downtown",status:"In progress",amount:240,icon:"❄",tone:"purple"},
  {id:"KF-1041",title:"Kitchen sink repair",service:"Repair",customer:"Marcus Chen",date:"2026-11-18",time:"11:30 AM",location:"West End",status:"Upcoming",amount:180,icon:"⌁",tone:"orange"},
  {id:"KF-1040",title:"Electrical inspection",service:"Inspection",customer:"Sophia Patel",date:"2026-11-18",time:"02:00 PM",location:"Midtown",status:"Upcoming",amount:320,icon:"ϟ",tone:"blue"},
  {id:"KF-1039",title:"Water heater install",service:"Installation",customer:"James Wilson",date:"2026-11-17",time:"10:00 AM",location:"North Park",status:"Completed",amount:680,icon:"♨",tone:"orange"},
  {id:"KF-1038",title:"Office deep cleaning",service:"Cleaning",customer:"Nora Davis",date:"2026-11-16",time:"08:30 AM",location:"Business District",status:"Completed",amount:450,icon:"✧",tone:"green"},
  {id:"KF-1037",title:"Outdoor lighting",service:"Installation",customer:"Ethan Brooks",date:"2026-11-15",time:"01:00 PM",location:"Riverside",status:"Pending",amount:275,icon:"☼",tone:"blue"},
  {id:"KF-1036",title:"Bathroom pipe repair",service:"Repair",customer:"Ava Thompson",date:"2026-11-14",time:"11:00 AM",location:"Old Town",status:"Completed",amount:195,icon:"⌁",tone:"purple"},
  {id:"KF-1035",title:"Seasonal AC check",service:"Maintenance",customer:"Noah Martin",date:"2026-11-13",time:"03:00 PM",location:"East Side",status:"Completed",amount:150,icon:"❄",tone:"blue"}
];
let jobs = JSON.parse(localStorage.getItem("kaamflow_jobs") || "null") || initialJobs;
const initialQuotes = [
  {id:"QT-2026-018",customer:"Marcus Chen",service:"Kitchen sink repair",date:"2026-11-18",amount:180,status:"Awaiting approval"},
  {id:"QT-2026-017",customer:"Olivia Rhye",service:"AC maintenance package",date:"2026-11-17",amount:420,status:"Approved"},
  {id:"QT-2026-016",customer:"James Wilson",service:"Water heater installation",date:"2026-11-16",amount:680,status:"Awaiting approval"},
  {id:"QT-2026-015",customer:"Nora Davis",service:"Office deep cleaning",date:"2026-11-12",amount:450,status:"Expired"}
];
let quotes = JSON.parse(localStorage.getItem("kaamflow_quotes") || "null") || initialQuotes;
const saveQuotes = () => localStorage.setItem("kaamflow_quotes",JSON.stringify(quotes));
let currentView = "overview";
const $ = (selector) => document.querySelector(selector);
const money = (value) => new Intl.NumberFormat("en-US",{style:"currency",currency:"USD",maximumFractionDigits:0}).format(Number(value)||0);
const saveJobs = () => localStorage.setItem("kaamflow_jobs",JSON.stringify(jobs));
const statusClass = (status) => status.toLowerCase().replaceAll(" ","-");
const dateLabel = (date) => new Date(date+"T12:00:00").toLocaleDateString("en-US",{month:"short",day:"numeric"});
function jobRow(job){
  return `<tr><td><div class="job-name"><span class="job-symbol ${job.tone||"purple"}">${job.icon||"▤"}</span><span><strong>${escapeHTML(job.title)}</strong><small>${job.id} · ${escapeHTML(job.service)}</small></span></div></td><td><div class="customer-cell"><strong>${escapeHTML(job.customer)}</strong><small>${escapeHTML(job.location||"Location not set")}</small></div></td><td>${dateLabel(job.date)}<br><small>${job.time||"Time TBD"}</small></td><td><span class="status status-${statusClass(job.status)}">${job.status}</span></td><td class="amount-cell">${money(job.amount)}</td><td><button class="row-menu" data-job-action="${job.id}" aria-label="Change job status">•••</button></td></tr>`;
}
function escapeHTML(value){return String(value).replace(/[&<>"']/g,char=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));}
function renderOverview(){
  const active=jobs.filter(j=>["In progress","Upcoming","Pending"].includes(j.status)).length;
  const completed=jobs.filter(j=>j.status==="Completed").length;
  $("#activeJobsMetric").textContent=String(12+active-4);
  $("#completedMetric").textContent=String(48+completed-4);
  $("#navJobCount").textContent=String(jobs.length);
  $("#jobsTableBody").innerHTML=jobs.slice(0,5).map(jobRow).join("");
  $("#jobsShowing").textContent=`Showing ${Math.min(5,jobs.length)} of ${jobs.length} jobs`;
  $("#outstandingMetric").textContent=money(2840);
}
function renderJobs(){
  const search=$("#jobSearch")?.value.toLowerCase()||"";
  const filter=$("#jobFilter")?.value||"All";
  const filtered=jobs.filter(j=>(filter==="All"||j.status===filter)&&[j.title,j.customer,j.id,j.service].join(" ").toLowerCase().includes(search));
  const body=$("#allJobsBody");
  if(body) body.innerHTML=filtered.length?filtered.map(jobRow).join(""):`<tr><td colspan="6"><div class="empty-state">No jobs match your search.</div></td></tr>`;
}
const viewInfo={
  jobs:["Jobs","Manage every job from request to completion."],
  quotes:["Quotes","Prepare estimates and track customer approvals."],
  calendar:["Schedule","See your team's upcoming appointments."],
  customers:["Customers","Keep customer details and service history together."],
  invoices:["Invoices","Track quotes, invoices and outstanding payments."],
  reports:["Reports","A simple snapshot of how your business is performing."],
  settings:["Settings","Manage your workspace preferences."]
};
function setView(view){
  currentView=view;
  document.querySelectorAll("[data-view]").forEach(el=>el.classList.toggle("active",el.dataset.view===view));
  $("#overviewView").classList.toggle("hidden",view!=="overview");
  $("#secondaryView").classList.toggle("hidden",view==="overview");
  $("#breadcrumbTitle").textContent=view==="overview"?"Overview":viewInfo[view]?.[0]||"Overview";
  if(view==="overview") return;
  const [title,description]=viewInfo[view]||viewInfo.jobs;
  $("#secondaryTitle").textContent=title;$("#secondaryDescription").textContent=description;
  $("#secondaryNewBtn").classList.toggle("hidden",!["jobs"].includes(view));
  renderSecondary(view);
  $("#sidebar").classList.remove("open");
}
function renderSecondary(view){
  const panel=$("#secondaryPanel");
  if(view==="jobs"){
    panel.innerHTML=`<div class="secondary-toolbar"><input class="search-input" id="jobSearch" placeholder="Search jobs or customers..." aria-label="Search jobs"><select class="filter-select" id="jobFilter" aria-label="Filter jobs"><option>All</option><option>Upcoming</option><option>In progress</option><option>Pending</option><option>Completed</option></select></div><div class="table-wrap"><table class="secondary-table"><thead><tr><th>JOB DETAILS</th><th>CUSTOMER</th><th>SCHEDULE</th><th>STATUS</th><th>AMOUNT</th><th></th></tr></thead><tbody id="allJobsBody"></tbody></table></div>`;
    $("#jobSearch").addEventListener("input",renderJobs);$("#jobFilter").addEventListener("change",renderJobs);renderJobs();
  }else if(view==="quotes"){
    const rows=quotes.map(q=>{const statusClassName=q.status==="Approved"?"status-completed":q.status==="Expired"?"status-upcoming":"status-pending";return `<tr><td><strong>${escapeHTML(q.id)}</strong></td><td>${escapeHTML(q.customer)}</td><td>${escapeHTML(q.service)}</td><td>${dateLabel(q.date)}</td><td><span class="status ${statusClassName}">${escapeHTML(q.status)}</span></td><td class="amount-cell">${money(q.amount)}</td><td>${q.status==="Awaiting approval"?`<button class="outline-button quote-approve" data-quote-action="${escapeHTML(q.id)}">Mark approved</button>`:"—"}</td></tr>`;}).join("");
    panel.innerHTML=`<div class="panel-heading"><div><h2>Quote pipeline</h2><p>Illustrative estimates waiting for a customer decision.</p></div><span class="attention-count">${quotes.filter(q=>q.status==="Awaiting approval").length} awaiting</span></div><div class="table-wrap"><table><thead><tr><th>QUOTE</th><th>CUSTOMER</th><th>SERVICE</th><th>DATE</th><th>STATUS</th><th>ESTIMATE</th><th>ACTION</th></tr></thead><tbody>${rows}</tbody></table></div><p class="subheading" style="margin-top:18px">Demo only: quote approvals are stored in this browser and do not send messages or create real invoices.</p>`;
  }else if(view==="customers"){
    const unique=[...new Map(jobs.map(j=>[j.customer,j])).values()];
    panel.innerHTML=`<div class="customer-grid">${unique.map((j,i)=>`<article class="customer-card"><div class="customer-initial">${escapeHTML(j.customer.split(" ").map(n=>n[0]).join("").slice(0,2))}</div><strong>${escapeHTML(j.customer)}</strong><small>${escapeHTML(j.location||"Location not set")}</small><p class="subheading">${jobs.filter(x=>x.customer===j.customer).length} service job(s)</p></article>`).join("")}</div>`;
  }else if(view==="calendar"){
    const days=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
    panel.innerHTML=`<div class="panel-heading"><div><h2>November 2026</h2><p>Sample schedule view · Select a job to explore your week.</p></div></div><div class="calendar-grid">${days.map(d=>`<div class="calendar-day"><strong>${d}</strong></div>`).join("")}${Array.from({length:30},(_,i)=>{const n=i+1;const matching=jobs.filter(j=>Number(j.date.slice(-2))===n);return `<div class="calendar-day"><strong>${n<=30?n:""}</strong>${matching.slice(0,2).map(j=>`<span class="calendar-event">${escapeHTML(j.title)}</span>`).join("")}</div>`;}).join("")}</div>`;
  }else if(view==="invoices"){
    const rows=jobs.slice(0,5).map((j,i)=>`<tr><td><strong>INV-2026-${String(42-i).padStart(3,"0")}</strong></td><td>${escapeHTML(j.customer)}</td><td>${dateLabel(j.date)}</td><td><span class="status ${i<2?"status-pending":"status-completed"}">${i<2?"Awaiting payment":"Paid"}</span></td><td class="amount-cell">${money(j.amount)}</td><td><button class="row-menu" data-invoice="${j.id}">Print ↗</button></td></tr>`).join("");
    panel.innerHTML=`<div class="panel-heading"><div><h2>Recent invoices</h2><p>Demo invoices generated from sample jobs.</p></div><button class="outline-button" id="exportInvoices">Export CSV ↓</button></div><div class="table-wrap"><table><thead><tr><th>INVOICE</th><th>CUSTOMER</th><th>DATE</th><th>STATUS</th><th>AMOUNT</th><th>ACTION</th></tr></thead><tbody>${rows}</tbody></table></div>`;
    $("#exportInvoices").addEventListener("click",exportCSV);
  }else if(view==="reports"){
    panel.innerHTML=`<div class="report-grid"><div class="report-box"><small>Jobs this month</small><strong>56</strong><span class="trend positive">↗ 12.5% vs last month</span></div><div class="report-box"><small>Revenue this month</small><strong>$8,460</strong><span class="trend positive">↗ 18.4% vs last month</span></div><div class="report-box"><small>Average job value</small><strong>$151</strong><span class="trend positive">↗ 4.2% vs last month</span></div></div><p class="subheading" style="margin-top:22px">These are illustrative demo figures, not live financial data.</p>`;
  }else{
    panel.innerHTML=`<div class="settings-row"><div><strong>Workspace name</strong><small>Shown to your team and customers.</small></div><strong>Acme Services</strong></div><div class="settings-row"><div><strong>Currency</strong><small>Used for sample estimates and invoices.</small></div><strong>USD ($)</strong></div><div class="settings-row"><div><strong>Data storage</strong><small>Demo data is stored in this browser only.</small></div><strong>Local storage</strong></div><div class="settings-row"><div><strong>Notifications</strong><small>In-app reminders and updates.</small></div><strong>Demo mode</strong></div>`;
  }
}
function openModal(){ $("#jobModal").classList.remove("hidden");document.body.style.overflow="hidden"; }
function closeModal(){ $("#jobModal").classList.add("hidden");document.body.style.overflow=""; }
function showToast(message){const toast=$("#toast");toast.textContent=message;toast.classList.add("show");clearTimeout(showToast.timer);showToast.timer=setTimeout(()=>toast.classList.remove("show"),2600);}
function exportCSV(){
  const rows=[["Job ID","Job","Customer","Date","Status","Amount"],...jobs.map(j=>[j.id,j.title,j.customer,j.date,j.status,j.amount])];
  const csv=rows.map(row=>row.map(v=>'"'+String(v).replaceAll('"','""')+'"').join(",")).join("\n");
  const link=document.createElement("a");link.href=URL.createObjectURL(new Blob([csv],{type:"text/csv"}));link.download="kaamflow-invoices-demo.csv";link.click();URL.revokeObjectURL(link.href);showToast("Your CSV export is ready.");
}
document.addEventListener("click",event=>{
  const nav=event.target.closest("[data-view]");
  if(nav){event.preventDefault();setView(nav.dataset.view);return;}
  const action=event.target.closest("[data-job-action]");
  if(action){const job=jobs.find(j=>j.id===action.dataset.jobAction);if(!job)return;const next=job.status==="Completed"?"Upcoming":"Completed";job.status=next;saveJobs();renderOverview();if(currentView==="jobs")renderJobs();showToast(`${job.id} marked ${next.toLowerCase()}.`);return;}
  const quoteAction=event.target.closest("[data-quote-action]");
  if(quoteAction){const quote=quotes.find(q=>q.id===quoteAction.dataset.quoteAction);if(quote){quote.status="Approved";saveQuotes();renderSecondary("quotes");showToast(`${quote.id} marked approved.`);}return;}
  const invoice=event.target.closest("[data-invoice]");
  if(invoice){const job=jobs.find(j=>j.id===invoice.dataset.invoice);if(job){const w=window.open("","_blank","width=600,height=700");if(w){w.document.write(`<title>Invoice ${job.id}</title><body style="font:16px Arial;padding:40px;color:#182230"><h1>KaamFlow</h1><h2>Invoice for ${escapeHTML(job.customer)}</h2><p>Reference: ${job.id}</p><p>Service: ${escapeHTML(job.title)}</p><p>Date: ${dateLabel(job.date)}</p><h2>Total: ${money(job.amount)}</h2><p>Thank you for your business.</p><script>window.print()<\/script></body>`);w.document.close();}}}
});
$("#newJobBtn").addEventListener("click",openModal);$("#secondaryNewBtn").addEventListener("click",openModal);
$("#closeModal").addEventListener("click",closeModal);$("#cancelModal").addEventListener("click",closeModal);
$("#jobModal").addEventListener("click",e=>{if(e.target.id==="jobModal")closeModal();});
$("#jobForm").addEventListener("submit",event=>{
  event.preventDefault();const data=new FormData(event.currentTarget);
  const title=data.get("title").trim(),customer=data.get("customer").trim();
  const job={id:"KF-"+(1043+jobs.length-initialJobs.length),title,service:data.get("service"),customer,date:data.get("date"),time:"Time TBD",location:data.get("location").trim()||"Location not set",status:"Upcoming",amount:Number(data.get("amount")),icon:"✦",tone:"purple"};
  jobs.unshift(job);saveJobs();renderOverview();if(currentView==="jobs")renderJobs();event.currentTarget.reset();closeModal();showToast("New job created successfully.");
});
$("#mobileMenu").addEventListener("click",()=>$("#sidebar").classList.toggle("open"));
$("#notificationBtn").addEventListener("click",()=>showToast("You're all caught up. No new notifications."));
$("#guideBtn").addEventListener("click",()=>showToast("Tip: Start by creating a job, then track it from the Jobs page."));
$("#todayLabel").textContent=new Date().toLocaleDateString("en-US",{weekday:"long",day:"numeric",month:"long"});
renderOverview();