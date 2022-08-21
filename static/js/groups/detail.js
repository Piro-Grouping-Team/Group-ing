const copyBtn = document.querySelector(".group-code");

const copyClipboard = () => {
  const copyText = document.querySelector(".group-code-content").textContent;
  const textarea = document.createElement("textarea");
  const modal = document.querySelector(".group-code-modal");

  textarea.textContent = copyText;
  document.body.append(textarea);

  textarea.select();
  document.execCommand("copy");
  textarea.remove();

  modal.style.display = "flex";
};

copyBtn.addEventListener("click", copyClipboard);
