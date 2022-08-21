const addBtn1 = document.querySelector(".place-add");
const places = document.querySelector(".places");
addBtn1.addEventListener("click", () => {
  let place = document.createElement("input");
  place.setAttribute("class", "log-input");
  place.setAttribute("type", "text");
  place.setAttribute("placeholder", "장소를 추가해주세요");
  place.setAttribute("name", "place[]");
  places.appendChild(place);
});

const addBtn2 = document.querySelector(".img-add");
const images = document.querySelector(".images");
addBtn2.addEventListener("click", () => {
  let image = document.createElement("input");
  image.setAttribute("type", "file");
  image.setAttribute("name", "logImgs[]");
  images.appendChild(image);
});
