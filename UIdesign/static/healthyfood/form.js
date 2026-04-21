const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileInput");
const imagePreview = document.getElementById("image-preview");
const clearButton = document.getElementById("clear-btn");
const submitButton = document.getElementById("submit-btn");
const outputclear = document.getElementById("output");

function handleDragOver(event) {
  event.preventDefault();
  dropArea.classList.add("active");
}

function handleDrop(event) {
  event.preventDefault();
  dropArea.classList.remove("active");
  const file = event.dataTransfer.files[0];
  if (file) {
    handleFiles(file);
  }
}

function handleFiles(file) {
  const reader = new FileReader();
  reader.onload = function (e) {
    imagePreview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
    clearButton.style.display = "inline-block";
    submitButton.style.display = "inline-block";
  };
  reader.readAsDataURL(file);
}

function clearImage() {
  imagePreview.innerHTML = "";
  outputclear.innerHTML = "";
  fileInput.value = "";
  clearButton.style.display = "none";
  submitButton.style.display = "none";
}

fileInput.addEventListener("change", function () {
  handleFiles(this.files[0]);
});

// submitButton.addEventListener("click", function () {
//   // Add functionality to handle the submission
//   alert("Submitted!");
// });
