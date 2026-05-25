---
title: "Conciliação da Conta Corrente com Arquivo OFX"
module: "Financeiro"
difficulty: "Intermediária"
reading_time: 7
updated: 2026-05-25
summary: "Como importar um arquivo OFX do banco, conciliar automaticamente os lançamentos já existentes na conta corrente, incluir novos lançamentos sugeridos e cancelar conciliações incorretas."
permalink: /artigos/conciliacao-ofx/index.html
layout: artigo.njk
prerequisites:
  - "Arquivo OFX exportado do internet banking do banco"
  - "Conta corrente cadastrada no Nexus com apelido definido"
  - "Lançamentos do período já registrados na conta corrente (para conciliação com existentes)"
  - "Versão do Nexus 19.6.3.0 ou superior"
steps:
  - heading: "Selecione a conta e abra a Conciliação OFX"
    content: |
      Na tela de **Conta Corrente**, selecione o **Apelido** da conta bancária que deseja conciliar e clique em **Conciliação OFX**.
    image: /assets/img/artigos/conciliacao-ofx/01-passo.png

  - heading: "Selecione o arquivo OFX"
    content: |
      Na janela que se abre, selecione o **arquivo OFX** exportado do internet banking do seu banco.

      O sistema carregará automaticamente todos os lançamentos contidos no extrato.
    image: /assets/img/artigos/conciliacao-ofx/02-passo.png

  - heading: "Identifique os lançamentos já conciliados"
    content: |
      Após carregar o arquivo, os lançamentos **já conciliados** aparecem marcados com um ✔ e os campos da conta corrente ficam desabilitados — nenhuma ação é necessária para eles.
    image: /assets/img/artigos/conciliacao-ofx/03-passo.png

  - heading: "Incluir novos lançamentos não conciliados"
    content: |
      Para lançamentos do extrato que **ainda não existem** na conta corrente, o sistema habilita os campos para preenchimento e oferece **sugestões automáticas** com base em lançamentos anteriores do mesmo banco.

      Preencha os dados restantes e clique em **INCLUIR** para registrar o lançamento na conta corrente.
    image: /assets/img/artigos/conciliacao-ofx/04-passo.png
    callout:
      type: info
      text: "💡 As sugestões automáticas agilizam o lançamento de transações recorrentes como tarifas, DOCs e TEDs."

  - heading: "Associar lançamentos já existentes"
    content: |
      Se o lançamento do extrato **já existe** na conta corrente, selecione o(s) lançamento(s) correspondente(s) na grade inferior até que o valor do extrato e da conta corrente se igualem, e clique em **Associar**.

      O sistema permite selecionar **um ou mais lançamentos** para compor o valor total do extrato.
    image: /assets/img/artigos/conciliacao-ofx/05-passo.png

  - heading: "Cancelar uma conciliação incorreta"
    content: |
      Caso uma conciliação tenha sido feita de forma errada, selecione o lançamento e clique em **Cancelar Conciliação**.

      O cancelamento **não exclui** nenhum lançamento da conta corrente — mesmo que o lançamento tenha sido incluído pela própria tela de conciliação.
    image: /assets/img/artigos/conciliacao-ofx/06-passo.png
    callout:
      type: warning
      text: "⚠️ Cancelar a conciliação apenas desfaz o vínculo entre o extrato e o lançamento — o registro na conta corrente permanece intacto."

  - heading: "Filtrar visualização e trocar período"
    content: |
      Na grade inferior, é possível alternar entre exibir os lançamentos **não conciliados** ou os **conciliados**. Também é possível **trocar o período** caso necessite consultar datas diferentes.

      Use esses filtros para controlar e revisar toda a conciliação do período.
    image: /assets/img/artigos/conciliacao-ofx/07-passo.png
    callout:
      type: success
      text: "✅ Conciliação concluída! Todos os lançamentos do extrato OFX estão vinculados à conta corrente do Nexus."
---

## Como obter o arquivo OFX no banco

O arquivo OFX é exportado diretamente pelo internet banking de cada banco. Normalmente fica em:

- **Bradesco:** Extrato → Exportar → formato OFX
- **Itaú:** Extrato → Baixar extrato → OFX
- **Santander:** Extrato → Exportar extrato → OFX
- **Banco do Brasil:** Extrato → Salvar como OFX

O caminho exato pode variar conforme a versão do internet banking. Se não encontrar, consulte o suporte do banco.

## Resumo do fluxo

1. Conta Corrente → selecionar **Apelido** → **Conciliação OFX**
2. Selecionar o arquivo `.ofx` exportado do banco
3. Para lançamentos já existentes: selecionar na grade inferior → **Associar**
4. Para lançamentos novos: preencher campos (com sugestão automática) → **INCLUIR**
5. Para desfazer um vínculo errado: **Cancelar Conciliação**

> **Versão mínima:** 19.6.3.0
