
console.log("Script carregado");
console.log("Limpando session storage");
sessionStorage.clear();

function initializeTooltips() {
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.forEach(function (tooltipTriggerEl) {
    new bootstrap.Tooltip(tooltipTriggerEl);
  });
}

// Chame esta função após adicionar ou remover elementos que precisam de tooltips
initializeTooltips();

function handleDrop(event) {
  unhighlight();
  const files = event.dataTransfer.files;
  handleFiles(files).then(() => {
    // Reinicializa os tooltips após o processamento dos arquivos
    initializeTooltips();
  });
}

listarArquivos();


// Definir o intervalo de atualização para 5 segundos (5000 milissegundos)
setInterval(listarArquivos, 5000);

//atualizar lista de arquivos
async function listarArquivos() {

  console.log("Listando arquivos");

  var tagFile = document.getElementById("files");
  tagFile.innerHTML = "";

  fetch('/list-files')
    .then(response => response.text())
    .then(data => {

      var files = JSON.parse(data);

      for (const file of files) {

        tagFile.innerHTML +=
 
          `
          <span data-bs-toggle="tooltip" data-bs-placement="top" data-bs-title="Clique para baixar" id="` +
          file +
          `" style="margin: 5px;" class="badge d-flex p-2 align-items-center bg-success rounded-pill">
                
                <a  style="color: aliceblue; text-decoration: none;" value="` +
          file +
          `" href="#" onclick="downloadFile(this)">
                  <span   class=" downloadBox"` + file + ` "class="px-1"> ` +
          file +
          ` </span> </a>
                <a style="color: aliceblue;" value="` +
          file +
          `" href="#" onclick="deletarArquivo(this)">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                class="bi bi-x-circle" viewBox="0 0 16 16">
                <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16" />
                <path
                d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708" />
                </svg>
                </a>
                </span>`;
      }
      // Após adicionar todos os elementos, inicializa os tooltips
      var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
      tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
      });

      addMouseoverToDownloadBoxes();
      addMouseOutToDownloadBoxes();
    })
    .catch(error => {
      console.error('Error:', error);
      document.getElementById('output').innerText = 'Error: ' + error;
    });
}

async function handleFile(file) {
  var reader = new FileReader();
  console.log("Arquivo carregado: " + file.name);

  return new Promise((resolve, reject) => {
    reader.onload = async function (e) {
      console.log("Arquivo carregado com sucesso");
    };

    listarArquivos();
  });
}



document.addEventListener("DOMContentLoaded", function () {
  const dropArea = document.getElementById("drop-area");

  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(event) {
    event.preventDefault();
    event.stopPropagation();
  }

  dropArea.addEventListener("dragenter", highlight, false);
  dropArea.addEventListener("dragover", highlight, false);
  dropArea.addEventListener("dragleave", unhighlight, false);
  dropArea.addEventListener("drop", handleDrop, false);

  function highlight() {
    dropArea.classList.add("dragover");
  }

  function unhighlight() {
    dropArea.classList.remove("dragover");
  }

  function handleDrop(event) {
    unhighlight();
    const files = event.dataTransfer.files;
    handleFiles(files);
  }

  async function handleFiles(files) {
    //Pega arquivos do session storage
    var keys = Object.keys(sessionStorage);

    for (const file of files) {
      // Cria um FormData para enviar o arquivo
      const formData = new FormData();
      formData.append('file', file);

      // Envia o arquivo via Fetch para o servidor
      fetch('/upload', {
        method: 'POST',
        body: formData
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Erro ao enviar arquivo');
          }
          return response.text();
        })
        .then(data => {
          console.log('Resposta do servidor:', data);
          
          openModalWithMessage('Arquivo enviado com sucesso!');
        })
        .catch(error => {
          console.error('Erro:', error);
          openModalWithMessage('Erro ao enviar arquivo');
        });

      await handleFile(file);

      // Após atualizar o DOM, reinicialize os tooltips
      initializeTooltips();
    }
  }

  // Também tornamos possível clicar na área para selecionar um arquivo
  dropArea.addEventListener("click", function () {
    document.getElementById("file-input").click();
  });

  // Lidar com a seleção de arquivo através do botão de entrada de arquivo
  document
    .getElementById("file-input")
    .addEventListener("change", function (event) {
      const files = event.target.files;
      handleFiles(files);
    });
});

function addMouseoverToDownloadBoxes() {
  const fileBoxes = document.getElementsByClassName("downloadBox");
  for (const fileBox of fileBoxes) {
    fileBox.addEventListener("mouseover", function () {
      this.style.fontSize = "16px";
    });
  }
}

function addMouseOutToDownloadBoxes() {
  const fileBoxes = document.getElementsByClassName("downloadBox");
  for (const fileBox of fileBoxes) {
    fileBox.addEventListener("mouseout", function () {
      this.style.fontSize = "10px";
    });
  }
}