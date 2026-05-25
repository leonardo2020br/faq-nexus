---
title: "Definir Boleto de Cobrança Padrão para Empresa"
module: "Financeiro"
difficulty: "Iniciante"
reading_time: 3
updated: 2026-05-22
summary: "Como configurar o boleto de cobrança padrão de uma empresa no Nexus ERP usando o parâmetro 3.011."
permalink: /artigos/boleto-padrao-empresa/index.html
layout: artigo.njk
prerequisites:
  - "Acesso ao menu Configurações > Empresas"
  - "Carteiras de cobrança já cadastradas em Financeiro > Bancos"
  - "Permissão para alterar parâmetros da empresa"
steps:
  - heading: "Acesse Configurações > Empresas"
    content: |
      No menu principal do Nexus ERP, vá em **Configurações > Empresas**. A tela lista todas as empresas cadastradas no sistema.
    image: /assets/img/artigos/boleto-padrao-empresa/image1.png
  - heading: "Selecione a empresa e abra as Configurações"
    content: |
      Clique sobre a empresa desejada e, em seguida, acesse a opção **Configurações** da empresa.
    image: /assets/img/artigos/boleto-padrao-empresa/image2.png
  - heading: "Acesse a Aba 3 (Financeiro) e localize o Parâmetro 3.011"
    content: |
      Vá até a **Aba 3 — Financeiro** dentro das configurações da empresa. Localize o **Parâmetro 3.011** e selecione o boleto desejado como padrão.
    image: /assets/img/artigos/boleto-padrao-empresa/image3.png
    callout:
      type: info
      text: "💡 O Parâmetro 3.011 controla qual carteira de cobrança será sugerida automaticamente nas emissões de boleto desta empresa."
  - heading: "Confirme que o boleto padrão foi aplicado"
    content: |
      Após salvar, o boleto definido como padrão passará a aparecer automaticamente no campo correspondente em todos os fluxos de cobrança da empresa.
    image: /assets/img/artigos/boleto-padrao-empresa/image4.png
    callout:
      type: success
      text: "✅ <strong>Pronto!</strong> A empresa agora utiliza o boleto definido como padrão em todas as cobranças."
---

## Problemas comuns

**Não aparece nenhuma opção no Parâmetro 3.011.** Significa que não há carteiras de cobrança cadastradas em **Financeiro > Bancos > Carteiras de Cobrança**. Cadastre uma carteira antes de retornar a essa tela.

**Configurei mas o boleto não aparece automaticamente na emissão.** Verifique se a empresa selecionada na hora de emitir o boleto é a mesma onde o parâmetro foi configurado (em multi-empresa, cada CNPJ tem seus próprios parâmetros).

**Quero definir boletos diferentes por filial.** O Parâmetro 3.011 é por empresa/CNPJ. Para variações por filial, use a configuração específica de cada filial no mesmo caminho.
