document.documentElement.dataset.theme = localStorage.getItem("theme") || "light";
document.addEventListener("click", (event) => {
  if (event.target.matches("[data-theme-toggle]")) {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    localStorage.setItem("theme", next);
  }
});
