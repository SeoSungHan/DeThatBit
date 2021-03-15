const comments = document.querySelector(".comment");

function handleClick(e) {
  const e_type = e.target.name;
  const pk = e.target.value;
  const tmp = ".comment-edit-form-" + pk;
  const commentNum = ".comment_box-" + pk;
  const form = document.querySelector(tmp);
  const commentBox = document.querySelector(commentNum);
  if (e_type === "try-edit") {
    form.classList.remove("hidden");
    commentBox.classList.add("hidden");
    const textarea = form.querySelector("#id_text");
    const nowText = commentBox.querySelectorAll("p")[1].innerHTML;
    textarea.value = nowText;
  } else if (e_type === "edit-back") {
    form.classList.add("hidden");
    commentBox.classList.remove("hidden");
  }
}

function main() {
  comments.addEventListener("click", handleClick);
}

main();
