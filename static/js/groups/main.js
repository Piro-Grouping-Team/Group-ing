const modal = document.querySelector(".modal-container");
const newBtn = document.querySelector(".new-btn");

newBtn.addEventListener("click", () => {
  modal.classList.add("modal-show");
});

window.addEventListener("click", (e) => {
  if (e.target === modal) {
    modal.classList.remove("modal-show");
  } else false;
});


