const modal = document.querySelector(".modal");
const newBtn = document.querySelectorAll(".new-btn");
let flag = 1;

newBtn.forEach((btn) => { btn.addEventListener("click", (event) => {
  if (flag == 0) {
    modal.style.display = "none";
    btn.innerHTML = `<i class="fa-solid fa-circle-plus fa-lg"></i>`;
    flag = 1;
  } else {
    modal.style.display = "flex";
    btn.innerHTML = `<i class="fa-solid fa-circle-xmark fa-lg"></i>`;
    flag = 0;
  }
})
});

// newBtn.addEventListener("click", (event) => {
//   if (flag == 0) {
//     modal.style.display = "none";
//     newBtn.innerHTML = `<i class="fa-solid fa-circle-plus fa-lg"></i>`;
//     flag = 1;
//   } else {
//     modal.style.display = "flex";
//     newBtn.innerHTML = `<i class="fa-solid fa-circle-xmark fa-lg"></i>`;
//     flag = 0;
//   }
// });