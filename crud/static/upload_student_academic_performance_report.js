function upload_data(file) {
    const formData = new FormData();
    formData.append('excelFile', file);

    fetch('/upload_data/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Datos agregados con éxito!");
        } else {
            alert("Hubo un error al agregar los datos.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
