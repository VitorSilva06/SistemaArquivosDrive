export const servicesConfig = {
  inss: {
    id: "inss",
    name: "Aposentadoria por incapacidade permanente (aposentadoria por invalidez) / auxílio por incapacidade temporária (auxílio doença)",
    notice:
      "Observação: Os documentos que serão anexados deverão ser legíveis, se acaso algum dos documentos enviados não estiverem dessa forma, o próprio sistema através de inteligência artificial não fará a leitura do documento e poderá ocorrer o não aceite pelo sistema, por favor, pedimos que retire nova foto do documento de forma legível e tente anexar novamente. Lembre-se que essa documentação tem que realmente estar apta para leitura, pois é ela que irá fazer parte do seu processo administrativo ou judicial.",
    extraFields: [
      {
        id: "inss-senha",
        label: "Digite aqui a sua senha do site ou aplicativo MEU INSS",
        type: "password",
        placeholder: "Senha do Meu INSS",
      },
      {
        id: "inss-processo",
        label: "Número do processo (caso já tenha essa informação)",
        type: "text",
        placeholder: "Número do processo",
      },
      {
        id: "inss-cat",
        label: "CAT - Se tiver sofrido um acidente",
        type: "text",
        placeholder: "Número do CAT",
      },
    ],
    fields: [
      { id: "inss-identidade", label: "Identidade (RG)" },
      { id: "inss-cpf", label: "CPF" },
      {
        id: "inss-comp",
        label:
          "Comprovante de Residência em nome do cliente e com data que não seja superior a 6 meses, ou seja, não pode ser antigo",
      },
      { id: "inss-ctps", label: "Todas as Carteiras de Trabalho", multiple: true },
      { id: "inss-fgts", label: "Extrato do FGTS" },
      {
        id: "inss-laudos",
        label: "Laudos médicos, exames, receituários",
        multiple: true,
      },
      {
        id: "inss-ppp",
        label: "PPP (Perfil Profissiográfico Previdenciário) - Insalubridade ou periculosidade",
      },
      {
        id: "inss-carnes",
        label: "Carnês do INSS (caso já tenha essa informação)",
        multiple: true,
      },
      { id: "inss-outros", label: "Outros documentos", multiple: true },
    ],
  },
  bpc: {
    id: "bpc",
    name: "Atendimento BPC/LOAS",
    notice:
      "Observação: Os documentos que serão anexados deverão ser legíveis, se acaso algum dos documentos enviados não estiverem dessa forma, o próprio sistema através de inteligência artificial não fará a leitura do documento e poderá ocorrer o não aceite pelo sistema, por favor, pedimos que retire nova foto do documento de forma legível e tente anexar novamente. Lembre-se que essa documentação tem que realmente estar apta para leitura, pois é ela que irá fazer parte do seu processo administrativo ou judicial.",
    extraFields: [
      {
        id: "bpc-senha",
        label: "Senha do site Meu INSS (essa senha o requerente consegue buscar em qualquer agência do INSS)",
        type: "password",
        placeholder: "Senha do Meu INSS",
      },
    ],
    fields: [
      {
        id: "bpc-moradores",
        label:
          "RG, CPF e carteiras de trabalho de *todos* os moradores da residência",
        multiple: true,
      },
      {
        id: "bpc-cadunico",
        label: "Comprovante de inscrição no Cadastro do CAD ÚNICO",
      },
      {
        id: "bpc-gastos",
        label:
          "Notas de compras com alimentação, gastos gerais, despesas médicas, gastos com o tratamento da deficiência, comprovantes dos gastos mensais que a família tem no mês, luz, água, telefone",
        multiple: true,
      },
      {
        id: "bpc-ajuda",
        label:
          "Comprovantes de ajuda que o requerente recebe, a título de exemplo, declarações de igrejas que dão cesta básica, declarações de ajuda do próprio setor público",
        multiple: true,
      },
      {
        id: "bpc-pensao",
        label:
          "Comprovante de pensão alimentícia caso haja o recebimento",
      },
      {
        id: "bpc-fotos",
        label: "Fotos da residência, dos móveis",
        multiple: true,
      },
      {
        id: "bpc-laudos",
        label:
          "Em casos da deficiência laudos médicos, é indispensável que o laudo conste a CID da doença",
        multiple: true,
      },
      { id: "bpc-outros", label: "Outros documentos", multiple: true },
    ],
  },
  trabalhista: {
    id: "trabalhista",
    name: "Trabalhista",
    notice:
      "Observação: Os documentos que serão anexados deverão ser legíveis, se acaso algum dos documentos enviados não estiverem dessa forma, o próprio sistema através de inteligência artificial não fará a leitura do documento e poderá ocorrer o não aceite pelo sistema, por favor, pedimos que retire nova foto do documento de forma legível e tente anexar novamente. Lembre-se que essa documentação tem que realmente estar apta para leitura, pois é ela que irá fazer parte do seu processo administrativo ou judicial.",
    fields: [
      { id: "trab-identidade", label: "Identidade (RG)" },
      { id: "trab-cpf", label: "CPF" },
      { id: "trab-comp", label: "Comprovante de Residência" },
      { id: "trab-contracheques", label: "Contracheques", multiple: true },
      { id: "trab-fgts", label: "Extrato Analítico do FGTS" },
      {
        id: "trab-extratos",
        label: "Extratos mostrando os salários",
        multiple: true,
      },
      {
        id: "trab-fotos",
        label: "Fotografias do trabalho",
        multiple: true,
      },
      {
        id: "trab-whatsapp",
        label: "Mensagens de Whatsapp",
        multiple: true,
      },
      { id: "trab-trct", label: "Termo de recisão (TRCT)" },
      { id: "trab-ferias", label: "Recibo de férias" },
      { id: "trab-outros", label: "Outros documentos", multiple: true },
    ],
  },
  pensao_conjuge: {
    id: "pensao_conjuge",
    name: "Pensão por morte para esposa(o), filhos menores de 21 anos ou filho com deficiência",
    notice:
      "Observação: Os documentos que serão anexados deverão ser legíveis, se acaso algum dos documentos enviados não estiverem dessa forma, o próprio sistema através de inteligência artificial não fará a leitura do documento e poderá ocorrer o não aceite pelo sistema, por favor, pedimos que retire nova foto do documento de forma legível e tente anexar novamente. Lembre-se que essa documentação tem que realmente estar apta para leitura, pois é ela que irá fazer parte do seu processo administrativo ou judicial.",
    extraFields: [
      {
        id: "conj-senha",
        label:
          "Senha do 'Meu INSS' da pessoa que está requerendo/pedindo a pensão por morte",
        type: "password",
        placeholder: "Senha do Meu INSS",
      },
    ],
    fields: [
      { id: "conj-casamento", label: "Certidão de casamento" },
      {
        id: "conj-cnis",
        label: "CNIS do(a) falecido(a) ou carteira de trabalho",
      },
      {
        id: "conj-rgreq",
        label:
          "RG (da pessoa que está requerendo/pedindo a pensão por morte)",
      },
      {
        id: "conj-cpfreq",
        label:
          "CPF (da pessoa que está requerendo/pedindo a pensão por morte)",
      },
      {
        id: "conj-comp-falecido",
        label:
          "Comprovante de residência do(a) falecido(a) - *Os comprovantes de residência não pode ser superiores a dois anos da data do óbito*",
      },
      {
        id: "conj-comp-sobrevivente",
        label:
          "Comprovante de residência do(a) cônjuge sobrevivente",
      },
      { id: "conj-obito", label: "Certidão de óbito" },
      {
        id: "conj-laudos",
        label:
          "Laudos médicos que comprovem condição (Caso o cônjuge sobrevivente possua alguma incapacidade permanente ou deficiência)",
        multiple: true,
      },
      {
        id: "conj-acidente",
        label:
          "Caso o falecimento tenha ocorrido por acidente de qualquer natureza (Documentos que comprovem circunstância - ex: Boletim de ocorrência, laudos médicos demostrando a questão de que tenha tido acidente))",
        multiple: true,
      },
      { id: "conj-cpf-filho", label: "CPF do filho(a)" },
      {
        id: "conj-laudos-filho",
        label: "Laudos médicos do filho(a)",
        multiple: true,
      },
      { id: "conj-outros", label: "Outros documentos", multiple: true },
    ],
  },
  pensao_companheiro: {
    id: "pensao_companheiro",
    name: "Pensão por morte para companheira(o)",
    notice:
      "Observação: Os documentos que serão anexados deverão ser legíveis, se acaso algum dos documentos enviados não estiverem dessa forma, o próprio sistema através de inteligência artificial não fará a leitura do documento e poderá ocorrer o não aceite pelo sistema, por favor, pedimos que retire nova foto do documento de forma legível e tente anexar novamente. Lembre-se que essa documentação tem que realmente estar apta para leitura, pois é ela que irá fazer parte do seu processo administrativo ou judicial.",
    fields: [
      {
        id: "comp-rgreq",
        label: "RG da pessoa que deseja solicitar o benefício",
      },
      {
        id: "comp-cpfreq",
        label: "CPF da pessoa que deseja solicitar o benefício",
      },
      { id: "comp-rgfal", label: "RG do falecido(a)" },
      { id: "comp-cpffal", label: "CPF do falecido(a)" },
      { id: "comp-obito", label: "Certidão de óbito" },
      { id: "comp-comp", label: "Comprovante de residência" },
      {
        id: "comp-uniao",
        label:
          "Documentos que comprovem a união estável: (certidão de nascimento de filho em comum); prova de mesmo domicílio (comprovante de residência do(a) falecido(a) e do(a) requerente); conta bancária conjunta; declaração de Imposto de Renda em que um conste como dependente do outro; apólice de seguro em que um seja instituidor e o outro seja beneficiário; ficha de tratamento em instituição médica em que o companheiro conste como responsável pelo segurado, ou vice-versa; cadastro no CadÚnico; entre outros documentos que possam servir para essa comprovação",
        multiple: true,
      },
      { id: "comp-outros", label: "Outros documentos", multiple: true },
    ],
  },
  aposentadoria: {
    id: "aposentadoria",
    name: "Aposentadoria",
    notice:
      "Observação: Os documentos que serão anexados deverão ser legíveis, se acaso algum dos documentos enviados não estiverem dessa forma, o próprio sistema através de inteligência artificial não fará a leitura do documento e poderá ocorrer o não aceite pelo sistema, por favor, pedimos que retire nova foto do documento de forma legível e tente anexar novamente. Lembre-se que essa documentação tem que realmente estar apta para leitura, pois é ela que irá fazer parte do seu processo administrativo ou judicial.",
    extraFields: [
      {
        id: "apos-senha",
        label: "Digite aqui a sua senha do site ou aplicativo MEU INSS",
        type: "password",
        placeholder: "Senha do Meu INSS",
      },
    ],
    fields: [
      { id: "apos-rg-cpf", label: "RG e CPF OU CNH legíveis" },
      {
        id: "apos-comp",
        label: "Comprovante de residência (recente – até 120 dias)",
      },
      {
        id: "apos-ctps",
        label:
          "CTPS – todas as carteiras, mesmo as antigas com páginas de identificação, contratos e anotações",
        multiple: true,
      },
      { id: "apos-cnis", label: "Extrato CNIS completo" },
      {
        id: "apos-ppp",
        label:
          "PPP – Perfil Profissiográfico Previdenciário (para atividades insalubres/com periculosidade)",
      },
      {
        id: "apos-ltcat",
        label:
          "LTCAT, PPRA, PCMSO ou Laudo Técnico relacionado (para atividades insalubres/com periculosidade)",
        multiple: true,
      },
      {
        id: "apos-ctc",
        label:
          "Certidão de tempo de contribuição (CTC) e declaração com valores das remunerações (em caso de servidor público)",
      },
      {
        id: "apos-reservista",
        label: "Certificado de Reservista (em caso de ter servido o exército)",
      },
      {
        id: "apos-fgts",
        label:
          "Extrato analítico do FGTS (documento fornecido pela caixa econômica federal)",
      },
      {
        id: "apos-sentencas",
        label:
          "Sentenças trabalhistas que reconheçam vínculo empregatício (em caso de já ter tido algum processo trabalhista, anexar a sentença)",
        multiple: true,
      },
      {
        id: "apos-vinculos",
        label:
          "Comprovantes de vínculos que não estão reconhecidos no CNIS (carnês do INSS, recibos, notas fiscais e contratos de prestação de serviços)",
        multiple: true,
      },
      {
        id: "apos-exterior",
        label: "Comprovantes de tempo no exterior (se houver)",
        multiple: true,
      },
      { id: "apos-outros", label: "Outros documentos", multiple: true },
    ],
  },
  aposentadoria_rural: {
    id: "aposentadoria_rural",
    name: "Aposentadoria Rural",
    notice:
      "Observação: Os documentos que serão anexados deverão ser legíveis, se acaso algum dos documentos enviados não estiverem dessa forma, o próprio sistema através de inteligência artificial não fará a leitura do documento e poderá ocorrer o não aceite pelo sistema, por favor, pedimos que retire nova foto do documento de forma legível e tente anexar novamente. Lembre-se que essa documentação tem que realmente estar apta para leitura, pois é ela que irá fazer parte do seu processo administrativo ou judicial.",
    extraFields: [
      {
        id: "rural-senha",
        label: "Digite aqui sua senha do site ou aplicativo meu INSS",
        type: "password",
        placeholder: "Senha do Meu INSS",
      },
    ],
    fields: [
      { id: "rural-rg-cpf", label: "RG e CPF ou CNH" },
      {
        id: "rural-certidao",
        label: "Certidão de nascimento ou casamento (preferencialmente atualizada)",
      },
      {
        id: "rural-comp",
        label: "Comprovante de residência atual (até 120 dias)",
      },
      {
        id: "rural-ctps",
        label:
          "CTPS – todas as carteiras de trabalho (mesmo sem ter tido registro, as CTPS devem ser enviadas na íntegra, ou seja, em todas as páginas que tiver algo anotado é para ter o envio)",
        multiple: true,
      },
      { id: "rural-notas-produtor", label: "Bloco de notas do produtor rural", multiple: true },
      {
        id: "rural-declaracao-sindicato",
        label:
          "Declaração de exercício rural pelo sindicato (com firma reconhecida)",
      },
      { id: "rural-itr", label: "ITR (Imposto Territorial Rural)" },
      {
        id: "rural-ccir",
        label: "CCIR – Certificado de Cadastro de Imóvel Rural",
      },
      {
        id: "rural-notas-venda",
        label: "Notas fiscais de venda de produção rural",
        multiple: true,
      },
      {
        id: "rural-notas-compra",
        label: "Notas fiscais de compra de insumos (sementes, ração, adubo)",
        multiple: true,
      },
      {
        id: "rural-contratos",
        label: "Contratos de arrendamento, meação ou parceria rural",
        multiple: true,
      },
      { id: "rural-incra", label: "Cadastro no INCRA" },
      {
        id: "rural-credito",
        label:
          "Comprovantes de crédito rural, financiamentos ou custeio",
        multiple: true,
      },
      {
        id: "rural-notas-terceiros",
        label:
          "Notas de produtor de terceiros que mencionem o local de produção do cliente",
        multiple: true,
      },
      {
        id: "rural-documentacao-publica",
        label:
          "Documentação pública com profissão 'lavrador(a)', 'agricultor', 'pescador' etc",
        multiple: true,
      },
      {
        id: "rural-ccir-itr-familia",
        label:
          "CCIR ou ITR em nome dos pais, irmãos ou cônjuge",
        multiple: true,
      },
      {
        id: "rural-dap-caf",
        label: "DAP/CAF em nome de qualquer membro da família",
        multiple: true,
      },
      {
        id: "rural-contratos-familia",
        label:
          "Contratos de arrendamento/meação em nome de familiar",
        multiple: true,
      },
      {
        id: "rural-notas-familia",
        label: "Notas de produtor em nome do pai/mãe/marido",
        multiple: true,
      },
      {
        id: "rural-certidoes-profissao",
        label: "Certidões que indiquem profissão rural do familiar",
        multiple: true,
      },
      {
        id: "rural-certidao-nascimento-filhos",
        label:
          "Certidão de nascimento dos filhos com profissão rural do pai/mãe",
        multiple: true,
      },
      {
        id: "rural-certidao-casamento",
        label: "Certidão de casamento com profissão 'lavrador(a)'",
      },
      {
        id: "rural-alistamento",
        label: "Certidão de alistamento militar com profissão rural",
      },
      {
        id: "rural-obito-familia",
        label: "Certidão de óbito de familiares indicando atividade rural",
        multiple: true,
      },
      {
        id: "rural-historico-escolar",
        label: "Histórico escolar dos filhos constando endereço rural",
        multiple: true,
      },
      {
        id: "rural-ficha-medica",
        label: "Ficha de atendimento médico/hospitalar com endereço rural",
        multiple: true,
      },
      {
        id: "rural-recibos",
        label: "Recibos de pagamento por tarefa ou diária",
        multiple: true,
      },
      {
        id: "rural-contratos-trabalho",
        label: "Contratos de trabalho rurais (mesmo não registrados)",
        multiple: true,
      },
      { id: "rural-outros", label: "Outros documentos", multiple: true },
    ],
  },
  documentos_rurais: {
    id: "documentos_rurais",
    name: "Documentos rurais (para os clientes que trabalharam no meio rural) - Para revisão de aposentadoria ou pensão por morte",
    notice:
      "Observação: Os documentos que serão anexados deverão ser legíveis, se acaso algum dos documentos enviados não estiverem dessa forma, o próprio sistema através de inteligência artificial não fará a leitura do documento e poderá ocorrer o não aceite pelo sistema, por favor, pedimos que retire nova foto do documento de forma legível e tente anexar novamente. Lembre-se que essa documentação tem que realmente estar apta para leitura, pois é ela que irá fazer parte do seu processo administrativo ou judicial.",
    extraFields: [
      {
        id: "rurais-senha",
        label: "Digite aqui sua senha do site ou aplicativo meu inss",
        type: "password",
        placeholder: "Senha do Meu INSS",
      },
    ],
    fields: [
      { id: "rurais-rg-cpf", label: "RG e CPF ou CNH" },
      {
        id: "rurais-comp",
        label: "Comprovante de residência atualizado (até no máximo 120 dias)",
      },
      {
        id: "rurais-carta",
        label: "Carta de concessão da aposentadoria (se possuir)",
      },
      { id: "rurais-ctps", label: "CTPS – todas as carteiras", multiple: true },
      {
        id: "rurais-cnis",
        label: "Extrato CNIS atualizado (se possuir)",
      },
      {
        id: "rurais-fgts",
        label:
          "FGTS (extrato analítico) (esse documento é emitido pela própria caixa econômica federal)",
      },
      {
        id: "rurais-holerites",
        label:
          "Holerites/contracheques antigos em que os recibos estejam com valores maiores do que no CNIS",
        multiple: true,
      },
      {
        id: "rurais-sentenca",
        label:
          "Sentença trabalhista (se houve processo na justiça do trabalho)",
        multiple: true,
      },
      {
        id: "rurais-notas-recibos",
        label:
          "Notas fiscais/recibos de prestação de serviço (em que não houve recolhimento junto ao INSS)",
        multiple: true,
      },
      {
        id: "rurais-ppp",
        label:
          "PPP – Perfil Profissiográfico Previdenciário, LTCAT, PPRA / PCMSO, Holerites com adicional de insalubridade/periculosidade, Laudos antigos da empresa (em caso do Autor ter trabalhado com fatores de risco: insalubridade ou periculosidade)",
        multiple: true,
      },
      {
        id: "rurais-ctc",
        label: "Certidão de Tempo de Contribuição (CTC) (para servidores públicos)",
      },
      {
        id: "rurais-cat",
        label:
          "CAT (se houver acidente de trabalho ou se trata de doença adquirida no trabalho)",
      },
      { id: "rurais-outros", label: "Outros documentos", multiple: true },
    ],
  },
};

export const serviceOptions = Object.entries(servicesConfig).map(
  ([value, config]) => ({
    value,
    label: config.name,
  })
);
