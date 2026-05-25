---
title: "Geração de Contas a Receber na Devolução de Compra"
module: "Financeiro"
difficulty: "Intermediária"
reading_time: 10
updated: "2026-05-25"
summary: "Como configurar e utilizar a geração de contas a receber a partir de notas de devolução de compra, em vez do crédito padrão ao fornecedor."
prerequisites:
  - item: "Permissão de usuário habilitada para gerar Contas a Receber por devolução"
  - item: "Acesso ao módulo Configurações → Empresas"
  - item: "CFOP da devolução configurado para gerar financeiro"
steps:
  - heading: "Habilitar a permissão de geração de Contas a Receber por devolução"
    content: |
      Por padrão, a opção está **desmarcada** — o sistema continua gerando crédito ao fornecedor quando o CFOP da devolução gera financeiro.

      Para liberar a geração de Contas a Receber, acesse as **permissões de usuário** e habilite a opção correspondente a este recurso.

      > **Atenção:** A geração de parcelas utiliza campos padrões definidos na configuração da empresa. Esses padrões são essenciais para controles como: bloqueio de emissão de boleto e bloqueio de envio de carta de cobrança nesses títulos.
    image: /assets/img/artigos/contas-receber-devolucao/01-passo.png

  - heading: "Configurar os parâmetros padrão na Empresa"
    content: |
      Acesse **Configurações → Empresas → Configurações** e localize o campo **3.031 - Tipo de Cobrança**.

      Neste campo, defina o **Tipo de Cobrança padrão** que será usado ao criar o Contas a Receber por meio da devolução.

      Pontos importantes:
      - Foi criado o tipo de cobrança **ID 26 - MERCADORIA/DESCONTO**, listado exclusivamente nesses documentos. Use-o quando a liquidação não deve gerar financeiro (ex.: fornecedor devolveu em mercadorias).
      - Controles automáticos aplicados nesses títulos: **sem junções**, **sem envio para desconto bancário**.
    image: /assets/img/artigos/contas-receber-devolucao/02-passo.png
    callout:
      type: info
      text: "O Tipo de Cobrança definido aqui determina quais operações estarão disponíveis nos títulos gerados por devolução."

  - heading: "Escolher entre Crédito ao Fornecedor ou Contas a Receber na nota"
    content: |
      Na tela de nota fiscal **(0098)**, quando o documento for do tipo **DC (Devolução de Compra)** com um CFOP que gera financeiro, a aba de **Pagamento** exibirá um combo com duas opções:

      - **Gerar Crédito** — mantém o comportamento original (crédito ao fornecedor)
      - **Gerar Contas a Receber** — cria um título no Contas a Receber

      Selecione a opção desejada antes de gravar a nota.
    image: /assets/img/artigos/contas-receber-devolucao/03-passo.jpeg

  - heading: "Identificação e bloqueio da nota que gerou Contas a Receber"
    content: |
      Ao optar por gerar Contas a Receber, a nota fiscal fica **identificada internamente** (campo `nota_saida.gerou_contas_receber`) para impedir alterações que afetariam o financeiro.

      - **Alterações comuns ficam bloqueadas** após a gravação
      - Via **CTRL+P** é possível liberar alterações, mas **sem impacto no financeiro já gerado**

      Isso garante a rastreabilidade entre a nota de devolução e os títulos criados no Contas a Receber.
    image: /assets/img/artigos/contas-receber-devolucao/04-passo.png

  - heading: "Como a parcela é gerada no Contas a Receber"
    content: |
      O sistema insere **uma única parcela** com o valor total da nota, seguindo estas regras:

      - **Número do documento:** número da nota fiscal do fornecedor (nota de origem da devolução)
      - **Origem:** CP
      - **Demais campos:** utilizados os padrões definidos na configuração da empresa

      Para devoluções **incluídas manualmente** (sem vínculo a uma entrada no sistema), ao optar por gerar Contas a Receber, o campo **número da nota de referência torna-se obrigatório**. O sistema exibirá a mensagem:

      > *"É NECESSÁRIO DEFINIR NÚMERO DA NOTA PARA PROSSEGUIR COM O MÉTODO DE CONTAS A RECEBER"*
    image: /assets/img/artigos/contas-receber-devolucao/07-passo.png

  - heading: "Atenção à permissão de exclusão do financeiro da nota original"
    content: |
      Existe outra permissão que impacta diretamente este recurso:

      **Vendas → 3.453 — Na devolução TOTAL, excluir Financeiro da nota Original**

      Quando essa permissão está ativa, ao gravar uma devolução o sistema pergunta: *"CONFIRMA REALIZAR A EXCLUSÃO DO LANÇAMENTO ORIGINAL?"*

      Porém, se o usuário optou por **gerar Contas a Receber**, a pergunta de exclusão **não será exibida** — o financeiro da nota original é mantido. A exclusão só ocorre quando o usuário opta por **Gerar Crédito**.
    image: /assets/img/artigos/contas-receber-devolucao/09-passo.png
    callout:
      type: warning
      text: "Com ambas as permissões ativas, a exclusão do financeiro da nota original só acontece ao escolher Gerar Crédito — nunca ao gerar Contas a Receber."

  - heading: "Baixa de parcelas com MERCADORIA/DESCONTO"
    content: |
      Para liquidar títulos de devolução sem movimentação financeira (ex.: fornecedor devolveu em mercadorias), utilize o tipo de cobrança **ID 26 - MERCADORIA/DESCONTO** na baixa.

      O sistema suporta dois cenários:

      - **Baixa por Valor e Parcela** aplicando MERCADORIA/DESCONTO — quita o título sem gerar financeiro
      - **Baixa por Valor e Parcela** com **recebimento parcial**, combinando MERCADORIA/DESCONTO com outro tipo de recebimento
    image: /assets/img/artigos/contas-receber-devolucao/10-passo.png

  - heading: "Restrições nos títulos gerados por devolução (tela 0079)"
    content: |
      Contas a Receber gerados por devolução de compra (origem **CP**) possuem restrições automáticas na tela **0079 — Contas a Receber**:

      - **Renegociação de Parcelas por Cliente** — não lista
      - **Renegociação de Parcelas em Massa** — não lista
      - **Enviar boletos para desconto** — não lista
      - **Emissão de Cartas de Cobrança** — não lista
      - **Emissão de boletos de cobrança** — não lista
      - **Pagamento múltiplo** — não listado

      Esses controles são aplicados automaticamente para garantir a integridade dos títulos originados por devolução.
    image: /assets/img/artigos/contas-receber-devolucao/12-passo.png
---
