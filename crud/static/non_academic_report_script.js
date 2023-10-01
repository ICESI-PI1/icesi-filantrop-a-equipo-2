const fileInput = document.getElementById('fileInput');
const fileNameSpan = document.getElementById('fileName');

fileInput.addEventListener('change', function() {
    const selectedFile = fileInput.files[0];
    if (selectedFile) {
        fileNameSpan.textContent = selectedFile.name;
    } else {
        fileNameSpan.textContent = 'Ningún archivo seleccionado';
    }
});