function deletarArquivo(nomeArquivo) {
    document.getElementById(nomeArquivo.getAttribute("value")).remove();

    //requisição

}

function downloadFile(fileName) {
    fileName = fileName.getAttribute("value");

    console.log("Download do arquivo: " + fileName);
    
    //fazer requisição para baixar o arquivo via post
    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Adicionando cabeçalho Content-Type
        },
        body: JSON.stringify({ filename: fileName }),
    })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(new Blob([blob]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', fileName);
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        })
        .catch(error => {
            console.error('Error:', error);
            openModalWithMessage("Erro ao baixar arquivo: "+ error);
        });
    
}

function openModalWithMessage(x) {
    //seta a mensagem do modal
    document.getElementById("modalMessage").innerHTML = x;
    $("#myModal").modal("show");
}

function closeModalWithMessage() {
    $("#myModal").modal("hide");
}


function openModal(x) {
    $("#" + x).modal("show");
}

function closeModal(x) {
    $("#" + x).modal("hide");
}