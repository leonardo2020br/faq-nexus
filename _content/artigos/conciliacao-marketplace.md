---
title: "Conciliação Marketplace"
module: "E-commerce"
difficulty: "Intermediária"
reading_time: 8
updated: 2026-05-25
summary: "Como importar a planilha de pagamentos do marketplace, conciliar os valores recebidos e finalizar a conciliação na conta corrente do Nexus ERP."
permalink: /artigos/conciliacao-marketplace/index.html
layout: artigo.njk
prerequisites:
  - "Planilha de conciliação exportada diretamente do marketplace (Magalu, Shopee, Amazon, B2W etc.)"
  - "Conta transitória de débito cadastrada (onde os pedidos são lançados antes da conciliação)"
  - "Conta/banco de crédito cadastrado (onde o marketplace efetivamente deposita o valor)"
  - "Permissão de acesso ao módulo Financeiro > Conta Corrente > Conciliação de Marketplace"
steps:
  - heading: "Acesse a Conciliação de Marketplace"
    content: |
      No menu principal do Nexus ERP, clique na aba **Financeiro**.

      Em seguida, dentro do bloco **Conta Corrente**, localize e clique em **Conciliação de MarketPlace**.
    image: /assets/img/artigos/conciliacao-marketplace/01-acesso-menu.png

  - heading: "Clique em Importar Planilha"
    content: |
      Na tela de Conciliação Marketplace, clique no botão **Importar Planilha** na barra de ferramentas superior.

      Essa ação abre a janela de importação onde você irá configurar todos os parâmetros da conciliação.
    image: /assets/img/artigos/conciliacao-marketplace/02-importar-planilha.png

  - heading: "Selecione o Marketplace"
    content: |
      No campo **MarketPlace (Modelo Arquivo)**, selecione a plataforma correspondente à planilha que você vai importar. As opções disponíveis incluem:

      - SHOPEE (SLR)
      - MAGALU (MLS) / MAGALU PADRÃO MAGALU (SLS)
      - B2W (DIV)
      - AMAZON (ALS)
      - VIA VAREJO / CARTÃO CRÉDITO (DLS)
      - VIPAY (DLS)
      - MADEIRA MADEIRA (SLS)
      - MERCADO LIVRE (DLS)
      - HETRADE PADRÃO MAGALU (SLS)

      **Atenção:** o modelo deve corresponder exatamente ao formato da planilha baixada no marketplace.
    image: /assets/img/artigos/conciliacao-marketplace/03-selecionar-marketplace.png
    callout:
      type: warning
      text: "⚠️ Selecionar o marketplace errado causará falha na importação ou valores incorretos. Confirme o formato da planilha antes de prosseguir."

  - heading: "Preencha os campos da conciliação"
    content: |
      Com o marketplace selecionado, preencha os demais campos:

      - **Descrição:** nome que identifica esta conciliação (ex.: `MAGALU MES-08`). Use um nome claro para facilitar a busca depois.
      - **Ajuste Débito:** informe a **conta transitória** — é a conta onde os valores dos pedidos são lançados antes de serem conciliados (ex.: `CAIXA INTERNO`).
      - **Ajuste Crédito:** informe o **banco ou conta de destino** — onde o marketplace de fato depositou o dinheiro (ex.: `BANCO SANTANDER`).
      - **Data do Crédito:** data em que o depósito foi realizado pelo marketplace na conta bancária.
    image: /assets/img/artigos/conciliacao-marketplace/04-preencher-campos.png
    callout:
      type: info
      text: "💡 O Ajuste Débito é a conta transitória de saída; o Ajuste Crédito é o banco que recebeu o valor real. Verifique com seu financeiro quais contas estão configuradas para cada marketplace."

  - heading: "Selecione e abra a planilha"
    content: |
      Clique no botão de seleção de arquivo. Navegue até a pasta onde está salva a planilha de conciliação exportada do marketplace e dê um clique duplo (ou selecione e clique em **Abrir**) para carregar o arquivo.

      O sistema aceita arquivos no formato **.XLS** (planilha Excel).
    image: /assets/img/artigos/conciliacao-marketplace/05-selecionar-arquivo.png

  - heading: "Verifique os pedidos carregados e clique em Gravar e Concluir"
    content: |
      Após a importação, o sistema lista todos os pedidos encontrados na planilha — com referência, data do pedido, valor, SKU, quantidade e parcelas.

      Revise os itens carregados. Quando estiver tudo correto, clique em **Gravar e Concluir** para registrar a conciliação no sistema.
    image: /assets/img/artigos/conciliacao-marketplace/06-pedidos-carregados.png
    callout:
      type: success
      text: "✅ A importação foi concluída. Os pedidos já estão vinculados à conciliação criada."

  - heading: "Regularize e Conclua"
    content: |
      De volta à tela de Conciliação Marketplace, informe o **período** da conciliação realizada e clique em **Regularizar**.

      Em seguida, na lista de conciliações, selecione a que você acabou de importar e clique em **Concluir**.

      Após essa etapa, a conciliação está encerrada — os valores são movidos da conta transitória para o banco de destino.
    image: /assets/img/artigos/conciliacao-marketplace/07-regularizar-concluir.png
    callout:
      type: success
      text: "🎉 Conciliação finalizada! Os valores do marketplace foram conciliados e a movimentação financeira está registrada corretamente."
---

## Resumo do fluxo

1. Financeiro > Conta Corrente > **Conciliação de MarketPlace**
2. **Importar Planilha** → selecionar marketplace → preencher Descrição, Conta Débito, Conta Crédito e Data do Crédito
3. Selecionar o arquivo `.XLS` exportado do marketplace → **Abrir**
4. Verificar pedidos carregados → **Gravar e Concluir**
5. Informar período → **Regularizar**
6. Selecionar a conciliação → **Concluir**

## Marketplaces suportados

| Marketplace | Modelo na tela |
|---|---|
| Shopee | SHOPEE (SLR) |
| Magazine Luiza | MAGALU (MLS) / MAGALU PADRÃO MAGALU (SLS) |
| B2W (Americanas, Submarino) | B2W (DIV) |
| Amazon | AMAZON (ALS) |
| Via Varejo / Cartão | VIA VAREJO - CARTÃO CRÉDITO (DLS) |
| Vipay | VIPAY (DLS) |
| Madeira Madeira | MADEIRA MADEIRA (SLS) |
| Mercado Livre | MERCADO LIVRE (DLS) |
| HeTrade / Magalu | HETRADE PADRÃO MAGALU (SLS) |

## Problemas comuns

**A planilha importa mas os valores ficam zerados.** O separador de decimais da planilha pode ser diferente do configurado. Na tela de importação, ajuste o campo **Separador de Decimais** conforme o formato do arquivo (ponto ou vírgula).

**Erro ao abrir o arquivo.** Verifique se a planilha está no formato `.XLS`. Arquivos `.XLSX` podem precisar ser salvos novamente no formato antigo pelo Excel.

**O marketplace correto não aparece na lista.** Entre em contato com o suporte do Nexus para que o modelo da plataforma seja cadastrado.

**A conciliação foi importada com dados errados.** Antes de Concluir, é possível excluir a conciliação e refazer o processo. Após o Concluir, acione o suporte para estorno.
