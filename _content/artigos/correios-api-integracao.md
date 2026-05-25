---
title: "Migração Correios: SIGEP Web → API (Sigep Via API)"
module: "Configurações"
difficulty: "Intermediária"
reading_time: 8
updated: 2026-05-25
summary: "Passo a passo para migrar a integração dos Correios do modo SIGEP Web para o novo modo Sigep Via API, incluindo configuração no sistema, geração do token no portal dos Correios e atualização do cadastro de transportadora."
permalink: /artigos/correios-api-integracao/index.html
layout: artigo.njk
prerequisites:
  - "Acesso ao módulo Configurações com perfil Administrador"
  - "Conta ativa no Portal Correios (cws.correios.com.br)"
  - "Cartão de postagem dos Correios em mãos"
steps:
  - heading: "Configurar o modo Sigep Via API no sistema"
    content: |
      Acesse **Configurações → Empresas → Configurações → Aba "17-Integrações"**.

      Na seção **Correios**, altere os seguintes campos:

      - **Modo:** `Sigep Via API`
      - **Ambiente:** `Produção`
      - **Não Reservar Faixas de Etiqueta:** marque esta opção (recomendado pelos Correios)

      Salve as configurações.
    image: /assets/img/artigos/correios-api-integracao/01-passo.png

  - heading: "Gerar o Token de API no Portal dos Correios"
    content: |
      Acesse o portal dos Correios em **https://cws.correios.com.br/ajuda** e gere o seu **Token de API**.

      Guarde o token gerado — ele será usado como **senha** no cadastro da transportadora (próximo passo).
    callout:
      type: warning
      text: "O token tem validade. Caso a integração pare de funcionar, acesse o portal novamente e regenere o token."

  - heading: "Atualizar o cadastro da transportadora CORREIOS"
    content: |
      Acesse **Cadastros → Parceiros de Negócios**, localize o cadastro **CORREIOS** e clique em **Alterar**.

      Vá para a aba **Transportadora** e preencha:

      - **Utilizar o Rastreio dos CORREIOS:** marque esta opção
      - **Usuário:** seu usuário/CPF do portal dos Correios
      - **Senha:** cole o **Token de API** gerado no passo anterior
      - **Cartão de Postagem:** informe o número do cartão de postagem

      Salve o cadastro.
    image: /assets/img/artigos/correios-api-integracao/02-passo.png
---

## Limpeza de Faixas de Etiqueta (importante)

Após migrar para o modo **Sigep Via API**, é necessário excluir as faixas de etiqueta livres que ficaram armazenadas pelo SIGEP Web. Execute a consulta abaixo no banco de dados para identificar os registros:

```sql
SELECT *
FROM etiquetas_correios
WHERE id_nota_saida IS NULL
  AND id_cliente IS NULL
  AND data_emissao IS NULL
  AND id_transp = <id da transportadora Correios>
```

Substitua `<id da transportadora Correios>` pelo ID do cadastro dos Correios no sistema. Após identificar os registros, exclua-os para evitar conflitos com as novas faixas geradas via API.

> **Recomendação:** Realize essa limpeza antes de emitir as primeiras etiquetas no novo modo.
