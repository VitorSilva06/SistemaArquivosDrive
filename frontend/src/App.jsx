import { useMemo, useRef, useState } from "react";
import "./App.css";
import { serviceOptions, servicesConfig } from "./data/services";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api";
const API_URL = `${API_BASE}`;

const defaultForm = {
  nome: "",
  telefone: "",
  servico: "",
};

function App() {
  const [formValues, setFormValues] = useState(defaultForm);
  const [filesMap, setFilesMap] = useState({});
  const [extraValues, setExtraValues] = useState({});
  const [feedback, setFeedback] = useState({ type: "", message: "" });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [rejectedFiles, setRejectedFiles] = useState([]);
  const formRef = useRef(null);

  const selectedService = useMemo(
    () => servicesConfig[formValues.servico],
    [formValues.servico]
  );

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormValues((prev) => ({ ...prev, [name]: value }));
  };

  const handleServiceChange = (event) => {
    const { value } = event.target;
    setFormValues((prev) => ({ ...prev, servico: value }));
    setFilesMap({});
    setExtraValues({});
    setFeedback({ type: "", message: "" });
    setRejectedFiles([]);
  };

  const handleFileChange = (fieldId, fileList) => {
    // Substitui a lista de arquivos do campo
    setFilesMap((prev) => ({
      ...prev,
      [fieldId]: Array.from(fileList),
    }));
  };

  const handleAppendFiles = (fieldId, fileList) => {
    // Acrescenta arquivos ao campo sem substituir os existentes
    const toAppend = Array.from(fileList);

    setFilesMap((prev) => {
      const existing = prev[fieldId] ?? [];
      // Evita duplicatas por nome + lastModified
      const existingKeys = new Set(
        existing.map((f) => `${f.name}__${f.lastModified}`)
      );
      const merged = [
        ...existing,
        ...toAppend.filter((f) => !existingKeys.has(`${f.name}__${f.lastModified}`)),
      ];
      return { ...prev, [fieldId]: merged };
    });
  };

  const replaceSingleFile = (fieldId, index, oldFileName, newFile) => {
    // Substitui o arquivo na posição 'index' e limpa a rejeição apenas desse item
    setFilesMap((prev) => {
      const list = [...(prev[fieldId] ?? [])];
      list[index] = newFile;
      return { ...prev, [fieldId]: list };
    });

    // Remove a marcação de rejeição apenas do item específico
    setRejectedFiles((prev) =>
      prev.filter((rf) => !(rf.field_id === fieldId && rf.filename === oldFileName))
    );
  };

  const handleExtraFieldChange = (fieldId, value) => {
    setExtraValues((prev) => ({ ...prev, [fieldId]: value }));
  };

  const buildFieldStatus = () => {
    if (!selectedService) return {};
    const status = {};
    selectedService.fields.forEach((field) => {
      status[field.id] = {
        label: field.label,
        uploadedCount: filesMap[field.id]?.length ?? 0,
      };
    });
    selectedService.extraFields?.forEach((field) => {
      status[field.id] = {
        label: field.label,
        uploadedCount: 0,
        value: extraValues[field.id] ?? "",
      };
    });
    return status;
  };

  const resetForm = () => {
    setFormValues(defaultForm);
    setFilesMap({});
    setExtraValues({});
    setRejectedFiles([]);
    formRef.current?.reset();
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedService) {
      setFeedback({
        type: "error",
        message: "Selecione um serviço para continuar.",
      });
      return;
    }

    const fieldStatus = buildFieldStatus();

    // Cria mapeamento de arquivo -> campo de origem
    const fileFieldMap = {};
    selectedService.fields.forEach((field) => {
      if (filesMap[field.id]) {
        filesMap[field.id].forEach((file) => {
          fileFieldMap[file.name] = {
            fieldId: field.id,
            fieldLabel: field.label,
          };
        });
      }
    });

    const filesToSend = selectedService.fields.flatMap((field) =>
      filesMap[field.id] ? filesMap[field.id] : []
    );

    if (filesToSend.length === 0) {
      setFeedback({
        type: "error",
        message: "Adicione ao menos um documento antes de enviar.",
      });
      return;
    }

    const formData = new FormData();
    formData.append("nome", formValues.nome.trim());
    formData.append("telefone", formValues.telefone.trim());
    formData.append("servico", formValues.servico);
    formData.append("field_status", JSON.stringify(fieldStatus));
    formData.append("file_field_map", JSON.stringify(fileFieldMap));
    formData.append("extra_values", JSON.stringify(extraValues));
    filesToSend.forEach((file) => {
      formData.append("documentos", file, file.name);
    });

    setIsSubmitting(true);
    setFeedback({ type: "", message: "" });

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        body: formData,
        mode: "cors",
        headers: {
          "Accept": "*/*"
        }
      });
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Erro ao enviar os documentos.");
      }

      // Armazena arquivos rejeitados
      if (payload.arquivos_rejeitados?.length > 0) {
        setRejectedFiles(payload.arquivos_rejeitados);
        setFeedback({
          type: "warning",
          message: `Arquivos enviados parcialmente! ${payload.arquivos_rejeitados.length} arquivo(s) foram rejeitados - veja abaixo em vermelho.`,
        });
      } else {
        setRejectedFiles([]);
        setFeedback({
          type: "success",
          message: `Arquivos enviados com sucesso! Todos os arquivos foram aceitos.`,
        });
        resetForm();
      }
    } catch (error) {
      setFeedback({
        type: "error",
        message: error.message || "Falha inesperada.",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="page">
      <header>
        <img src="/logo.png" alt="logo do escritório" />
      </header>
      <main className="container">
        <h2>Cadastro do cliente:</h2>
        <h3 style={{ fontSize: "0.9rem", fontWeight: "normal", color: "#666" }}>
          Informe os seus dados
        </h3>

        <form ref={formRef} onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="nome">Nome completo</label>
              <input
                id="nome"
                name="nome"
                type="text"
                placeholder="Seu nome"
                value={formValues.nome}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="telefone">Telefone</label>
              <input
                id="telefone"
                name="telefone"
                type="text"
                placeholder="(DDD) 00000-0000"
                value={formValues.telefone}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group full-width">
              <label htmlFor="serviceSelect">Por favor, selecione o tipo de serviço</label>
              <select
                id="serviceSelect"
                value={formValues.servico}
                onChange={handleServiceChange}
                required
              >
                <option value="">Selecione...</option>
                {serviceOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {selectedService && (
            <section
              key={selectedService.id}
              className="doc-box full-width"
              aria-live="polite"
            >
              <h3>Por favor, anexe aqui os documentos necessários para: {selectedService.name}</h3>
              <p className="notice">{selectedService.notice}</p>

              {selectedService.extraFields?.map((field) => (
                <div className="form-group" key={field.id}>
                  <label htmlFor={field.id}>{field.label}</label>
                  <input
                    id={field.id}
                    type={field.type ?? "text"}
                    placeholder={field.placeholder}
                    value={extraValues[field.id] ?? ""}
                    onChange={(event) =>
                      handleExtraFieldChange(field.id, event.target.value)
                    }
                  />
                </div>
              ))}

              {selectedService.fields.map((field) => {
                const hasRejectedFiles = rejectedFiles.some(
                  (rf) => rf.field_id === field.id
                );

                // ID para input hidden de anexos adicionais
                const hiddenInputId = `${field.id}-hidden-append`;

                return (
                  <div
                    className={`form-group ${hasRejectedFiles ? "has-rejected" : ""}`}
                    key={field.id}
                  >
                    <label htmlFor={field.id}>{field.label}</label>

                    <div className="file-controls">
                      {/* Input principal: visível apenas enquanto não há arquivos selecionados */}
                      {(filesMap[field.id]?.length ?? 0) === 0 && (
                        <input
                          id={field.id}
                          type="file"
                          multiple
                          onChange={(event) =>
                            handleFileChange(field.id, event.target.files)
                          }
                        />
                      )}

                      {/* Input hidden que recebe anexos adicionais */}
                      <input
                        id={hiddenInputId}
                        type="file"
                        multiple
                        style={{ display: "none" }}
                        onChange={(event) => {
                          handleAppendFiles(field.id, event.target.files);
                          event.target.value = "";
                        }}
                      />

                      {/* Botão + do campo: aparece quando já houver ao menos um arquivo */}
                      {(filesMap[field.id]?.length ?? 0) > 0 && (
                        <button
                          type="button"
                          className="btn-add-more-small"
                          aria-label={`Adicionar outro arquivo em ${field.label}`}
                          title="Adicionar outro arquivo"
                          onClick={() => document.getElementById(hiddenInputId)?.click()}
                        >
                          +
                        </button>
                      )}
                    </div>

                    <div className="file-list">
                      {(filesMap[field.id] ?? []).length === 0 ? (
                        <span className="file-item empty">Nenhum arquivo adicionado.</span>
                      ) : (
                        filesMap[field.id].map((file, index) => {
                          const rejectedFile = rejectedFiles.find(
                            (rf) => rf.filename === file.name && rf.field_id === field.id
                          );

                          const itemReplaceInputId = `${field.id}-replace-${index}`;

                          return (
                            <div key={`${field.id}-${file.name}-${file.lastModified}`}>
                              <div
                                className={`file-item ${rejectedFile ? "rejected" : "accepted"}`}
                                title={rejectedFile ? `Rejeitado: ${rejectedFile.reason}` : ""}
                              >
                                <span className="file-name">{file.name}</span>
                                {rejectedFile && (
                                  <span className="rejection-info">
                                    {rejectedFile.reason}
                                  </span>
                                )}
                                <span className="file-size">
                                  {(file.size / 1024).toFixed(0)} KB
                                </span>
                              </div>

                              {/* input hidden para substituir especificamente este item */}
                              <input
                                id={itemReplaceInputId}
                                type="file"
                                style={{ display: "none" }}
                                onChange={(e) => {
                                  const f = e.target.files?.[0];
                                  if (f) {
                                    replaceSingleFile(field.id, index, file.name, f);
                                  }
                                  e.target.value = "";
                                }}
                              />

                              {/* Botão por item para troca específica */}
                              <div className="file-item-actions">
                                <button
                                  type="button"
                                  className="btn-add-more-small"
                                  aria-label={`Trocar este arquivo em ${field.label}`}
                                  title="Trocar este arquivo"
                                  onClick={() => document.getElementById(itemReplaceInputId)?.click()}
                                >
                                  +
                                </button>
                              </div>
                            </div>
                          );
                        })
                      )}
                    </div>
                  </div>
                );
              })}
            </section>
          )}

          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Enviando..." : "Enviar documentos"}
          </button>

          {feedback.message && (
            <div className={`feedback ${feedback.type}`}>
              {feedback.message}
            </div>
          )}
        </form>
      </main>
    </div>
  );
}

export default App;
