const saElementList = document.querySelectorAll(".ti");
const saDefaultMargin = 300;
let saTriggerMargin = 0;
let saTriggerHeight = 0;

const saFunc = function () {
  for (const element of saElementList) {
    if (!element.classList.contains("show")) {
      if (element.dataset.saMargin) {
        saTriggerMargin = parseInt(element.dataset.saMargin);
      } else {
        saTriggerMargin = saDefaultMargin;
      }

      if (element.dataset.saTrigger) {
        saTriggerHeight =
          document
            .querySelector(element.dataset.saTrigger)
            .getBoundingClientRect().top + saTriggerMargin;
      } else {
        saTriggerHeight = element.getBoundingClientRect().top + saTriggerMargin;
      }

      if (window.innerHeight > saTriggerHeight) {
        let delay = element.dataset.saDelay ? element.dataset.saDelay : 0;
        setTimeout(function () {
          element.classList.add("show");
        }, delay);
      }
    }
  }
};

window.addEventListener("load", saFunc);
window.addEventListener("scroll", saFunc);
