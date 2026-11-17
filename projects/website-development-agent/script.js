const WHATSAPP = "https://wa.me/923443868091";
const messages = {
  general: "Assalam o Alaikum! I would like to place an order.",
  sajji: "Assalam o Alaikum! I would like to order: Sajji (سجی) with 1-litre bottle — PKR 1,500.",
  fish: "Assalam o Alaikum! I would like to order: Fish Fries — PKR 1,000.",
  rice: "Assalam o Alaikum! I would like to order: Simple Rice Plate — PKR 500."
};
function orderLink(message) {
  return WHATSAPP + "?text=" + encodeURIComponent(message);
}
document.querySelectorAll("[data-general-order]").forEach(link => link.href = orderLink(messages.general));
document.querySelectorAll("[data-sajji-order]").forEach(link => link.href = orderLink(messages.sajji));
document.querySelectorAll("[data-fish-order]").forEach(link => link.href = orderLink(messages.fish));
document.querySelectorAll("[data-rice-order]").forEach(link => link.href = orderLink(messages.rice));
document.getElementById("year").textContent = new Date().getFullYear();