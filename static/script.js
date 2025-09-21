// Search filter
document.addEventListener("DOMContentLoaded", () => {
  const searchBar = document.getElementById("searchBar");
  if (searchBar) {
    searchBar.addEventListener("keyup", () => {
      let term = searchBar.value.toLowerCase();
      document.querySelectorAll(".book-card").forEach(card => {
        card.style.display = card.innerText.toLowerCase().includes(term) ? "" : "none";
      });
    });
  }
});

// Show book details in modal
function showDetails(title, author, category, description, file_link) {
  let content = `
    <p><strong>Title:</strong> ${title}</p>
    <p><strong>Author:</strong> ${author}</p>
    <p><strong>Category:</strong> ${category}</p>
    <p><strong>Description:</strong> ${description}</p>
    <a href="${file_link}" target="_blank">📖 Open Book</a>
  `;
  document.getElementById("modalContent").innerHTML = content;
  new bootstrap.Modal(document.getElementById("bookModal")).show();
}
