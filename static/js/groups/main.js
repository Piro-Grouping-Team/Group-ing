const modal = document.querySelector(".modal");
const newBtn = document.querySelector(".new-btn");
let flag = 1;

newBtn.addEventListener("click", (event) => {
  if (flag == 0) {
    modal.style.display = "none";
    newBtn.innerHTML = `<i class="fa-solid fa-circle-plus"></i>`;
    flag = 1;
  } else {
    modal.style.display = "flex";
    newBtn.innerHTML = `<i class="fa-solid fa-circle-xmark"></i>`;
    flag = 0;
  }
});
