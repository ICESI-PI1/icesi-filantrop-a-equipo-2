document.getElementById("fileInput").addEventListener("change", function(event) {
    let uploadedFileName = event.target.files[0].name;
    document.getElementById("fileName").textContent = uploadedFileName;
});

