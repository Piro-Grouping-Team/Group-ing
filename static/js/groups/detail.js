const copyBtn = document.querySelector(".group-code");

const copyClipboard = () => {
  const copyText = document.querySelector(".group-code").textContent;
  const textarea = document.createElement("textarea");
  textarea.textContent = copyText;
  document.body.append(textarea);

  textarea.select();
  document.execCommand("copy");
  textarea.remove();
};

copyBtn.addEventListener("click", copyClipboard);
