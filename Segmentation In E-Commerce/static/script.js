// script.js

document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.getElementById("file");
    const fileNameDisplay = document.getElementById("file-name");
    const uploadForm = document.getElementById("upload-form");
    const submitBtn = document.getElementById("submit-btn");
    const loader = document.getElementById("loader");

    fileInput.addEventListener("change", function() {
        const fileName = this.files[0].name;
        fileNameDisplay.textContent = "Selected file: " + fileName;
        fileNameDisplay.style.color = "green";
    });

    uploadForm.addEventListener("submit", function() {
        loader.style.display = "inline-block";
        submitBtn.disabled = true;
    });
});
