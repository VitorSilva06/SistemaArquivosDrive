const form = document.getElementById("mainForm");
const serviceSelect = document.getElementById("serviceSelect");
const docBoxes = document.querySelectorAll(".doc-box");
const fileInputs = document.querySelectorAll('input[type="file"]');
const feedbackBox = document.getElementById("feedback");
const API_URL = "http://localhost:8000/api/submit";

const toggleDocBoxes = () => {
  docBoxes.forEach((box) => box.classList.add("hidden"));
  const target = serviceSelect.value;
  if (!target) return;
  const section = document.getElementById(target);
  if (section) {
    section.classList.remove("hidden");
  }
};

serviceSelect.addEventListener("change", toggleDocBoxes);

const updateFileList = (input) => {
  const targetId = input.dataset.target;
  const listEl = document.getElementById(targetId);
  if (!listEl) return;
  listEl.innerHTML = "";
  Array.from(input.files).forEach((file) => {
    const item = document.createElement("div");
    item.className = "file-item";
    const fileName = document.createElement("span");
    fileName.className = "file-name";
    fileName.textContent = file.name;
    item.appendChild(fileName);
    listEl.appendChild(item);
  });
};

fileInputs.forEach((input) => {
  input.addEventListener("change", () => updateFileList(input));
});

const showFeedback = (message, isError = false) => {
  feedbackBox.textContent = message;
  feedbackBox.classList.remove("hidden", "error", "success");
  feedbackBox.classList.add(isError ? "error" : "success");
  feedbackBox.scrollIntoView({ behavior: "smooth" });
};

const buildFieldStatus = () => {
  const status = {};
  fileInputs.forEach((input) => {
    const fieldKey = input.dataset.field || input.id;
    const label = input
      .closest(".form-group")
      ?.querySelector("label")
      ?.childNodes[0]?.textContent?.trim();
    status[fieldKey] = {
      label: label || fieldKey,
      uploadedCount: input.files.length,
    };
  });
  return status;
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!serviceSelect.value) {
    showFeedback("Selecione um serviço para continuar.", true);
    return;
  }

  const submitButton = form.querySelector('button[type="submit"]');
  submitButton.disabled = true;
  submitButton.textContent = "Enviando...";

  const formData = new FormData();
  formData.append("nome", document.getElementById("nome").value.trim());
  formData.append("telefone", document.getElementById("telefone").value.trim());
  formData.append("servico", serviceSelect.value);

  const fieldStatus = buildFieldStatus();
  formData.append("field_status", JSON.stringify(fieldStatus));

  let filesCount = 0;
  fileInputs.forEach((input) => {
    Array.from(input.files).forEach((file) => {
      formData.append("documentos", file, file.name);
      filesCount += 1;
    });
  });

  if (filesCount === 0) {
    showFeedback("Adicione ao menos um documento para continuar.", true);
    submitButton.disabled = false;
    submitButton.textContent = "Enviar documentos";
    return;
  }

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      body: formData,
    });

    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Erro inesperado ao enviar os dados.");
    }

    showFeedback(
      `Arquivos enviados! Pasta criada: ${payload.pasta}. ${
        payload.arquivos_rejeitados.length
          ? "Alguns arquivos foram rejeitados, revise o relatório."
          : "Todos os arquivos foram aceitos."
      }`,
      false
    );
    form.reset();
    docBoxes.forEach((box) => box.classList.add("hidden"));
    document.querySelectorAll(".file-list").forEach((list) => (list.innerHTML = ""));
  } catch (err) {
    showFeedback(err.message, true);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Enviar documentos";
  }
});

