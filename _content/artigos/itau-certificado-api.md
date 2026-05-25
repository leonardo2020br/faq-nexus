---
title: "Geração de Certificados API Itaú (Boleto Híbrido)"
module: "Financeiro"
difficulty: "Avançada"
reading_time: 12
updated: 2026-05-22
summary: "Passo a passo para gerar os arquivos de certificado (.csr, .key e .crt) e o Client Secret necessários para integrar o Boleto Híbrido do Itaú ao Nexus ERP, usando GitBash e Postman."
permalink: /artigos/itau-certificado-api/index.html
layout: artigo.njk
prerequisites:
  - "GitBash instalado (https://git-scm.com/downloads)"
  - "Postman instalado (https://www.postman.com/downloads/)"
  - "E-mail do Itaú com o ClientID e o Token Temporário anexo (válido por 7 dias)"
  - "Razão Social, Cidade e Estado da empresa cliente em mãos"
  - "Acesso ao Nexus ERP com permissão em Financeiro > Bancos"
steps:
  - heading: "Receba o e-mail do Banco Itaú"
    content: |
      O cliente receberá um e-mail do Itaú com a liberação da API contendo:
      
      - **ClientID** — identificador único da integração
      - **Token Temporário** — arquivo anexo, válido por **7 dias** para gerar os certificados
      
      Guarde esses dois valores em local seguro — eles serão usados nos próximos passos.
    callout:
      type: warning
      text: "⚠️ <strong>Atenção ao prazo:</strong> O Token Temporário expira em 7 dias. Se passar esse prazo, será necessário solicitar uma nova liberação ao Itaú."
  - heading: "Defina uma pasta para os arquivos do certificado"
    content: |
      No Windows, crie uma pasta dedicada (por exemplo, `C:\Certificados Itaú\NomeDoCliente\`). Nessa pasta serão gerados e armazenados os arquivos `.csr`, `.key` e `.crt`.
      
      Com o **botão direito do mouse** sobre a pasta, selecione a opção **"Open Git Bash here"** para abrir o terminal já apontando para o diretório correto.
    image: /assets/img/artigos/itau-certificado-api/image1.png
  - heading: "Gere os arquivos .csr e .key via GitBash"
    content: |
      No GitBash já aberto na pasta, cole o comando abaixo, **substituindo os campos em destaque** pelos dados reais do cliente:
      
      ```
      openssl req -new -subj "//CN={CLIENT_ID}\OU={RAZAO_SOCIAL}\L={CIDADE}\ST={UF}\C=BR" -out API_BOLETO.csr -nodes -sha512 -newkey rsa:2048 -keyout API_BOLETO.key
      ```
      
      Substitua:
      
      - `{CLIENT_ID}` — o ClientID recebido no e-mail do Itaú
      - `{RAZAO_SOCIAL}` — Razão Social completa do cliente
      - `{CIDADE}` — cidade da empresa (sem acentos)
      - `{UF}` — sigla do estado (ex.: SP, RJ, MG)
      
      Pressione **Enter** para executar.
    image: /assets/img/artigos/itau-certificado-api/image2.png
    callout:
      type: info
      text: "💡 <strong>Dica:</strong> Mantenha as barras invertidas duplas (\\\\) entre cada campo do comando — elas são obrigatórias na sintaxe do openssl no Windows."
  - heading: "Confira os arquivos gerados"
    content: |
      Após a execução, a pasta definida no passo 2 conterá dois arquivos novos:
      
      - `API_BOLETO.csr` — solicitação de assinatura do certificado
      - `API_BOLETO.key` — chave privada (mantenha em segurança absoluta)
    image: /assets/img/artigos/itau-certificado-api/image4.png
    callout:
      type: danger
      text: "🚨 <strong>Crítico:</strong> A chave .key é confidencial. Nunca compartilhe por e-mail, WhatsApp ou serviços públicos. Em caso de exposição, é necessário solicitar nova liberação ao Itaú."
  - heading: "Abra o Postman e crie uma nova requisição"
    content: |
      Abra o Postman e crie uma nova requisição do tipo **POST**.
    image: /assets/img/artigos/itau-certificado-api/image5.png
  - heading: "Informe a URL da requisição"
    content: |
      No campo de URL, informe:
      
      ```
      https://sts.itau.com.br/seguranca/v1/certificado/solicitacao
      ```
    image: /assets/img/artigos/itau-certificado-api/image6.png
  - heading: "Configure os Headers da requisição"
    content: |
      Na aba **"Headers"**, adicione duas variáveis:
      
      | Key | Value |
      |---|---|
      | `Content-Type` | `text/plain` |
      | `Authorization` | `Bearer {TOKEN_TEMPORÁRIO}` |
      
      Substitua `{TOKEN_TEMPORÁRIO}` pelo token recebido no e-mail do Itaú. **Atenção:** a palavra `Bearer` deve vir antes do token, separada por um espaço.
    image: /assets/img/artigos/itau-certificado-api/image7.png
  - heading: "Cole o conteúdo do .csr no Body e envie"
    content: |
      Acesse a aba **"Body"**, selecione a opção **"raw"** e cole o conteúdo completo do arquivo `API_BOLETO.csr` gerado no passo 3 (abra o arquivo com Bloco de Notas para copiar).
      
      Clique em **"Send"** para enviar a requisição.
    image: /assets/img/artigos/itau-certificado-api/image8.png
  - heading: "Salve o Client Secret e crie o arquivo .crt"
    content: |
      Estando tudo correto, o Postman retornará no painel inferior uma resposta contendo:
      
      - **Client Secret** — guarde esse valor (será usado no Nexus ERP)
      - **Conteúdo do .crt** — texto que precisa ser salvo como certificado
      
      Abra o **Bloco de Notas**, cole o conteúdo do `.crt` retornado e salve o arquivo na mesma pasta dos demais, com o nome `API_BOLETO.crt` (atenção à extensão `.crt`, não `.txt`).
    image: /assets/img/artigos/itau-certificado-api/image9.png
    callout:
      type: success
      text: "✅ <strong>Pronto:</strong> agora você tem os três arquivos finais (.csr, .key, .crt) e o Client Secret. Faltam apenas os ajustes dentro do Nexus."
  - heading: "Configure no Nexus ERP"
    content: |
      Dentro do Nexus, acesse:
      
      **Financeiro > Bancos > Selecionar o Banco (Itaú) > Botão "Carteiras de Cobrança" > Incluir/Alterar**
      
      Configure a carteira de cobrança normalmente. No quadro de **"API"**, preencha:
      
      - **ClientID** — o mesmo recebido no e-mail do Itaú (passo 1)
      - **Client Secret** — o valor retornado no Postman (passo 9)
      - **Certificado (.crt)** — anexe o arquivo `API_BOLETO.crt`
      - **Chave Privada (.key)** — anexe o arquivo `API_BOLETO.key`
      
      Salve a configuração.
    image: /assets/img/artigos/itau-certificado-api/image10.png
    callout:
      type: success
      text: "🎉 <strong>Integração concluída!</strong> A carteira do Itaú está pronta para emitir boletos híbridos via API."
---

## Problemas comuns

**O comando openssl retorna erro de sintaxe.** Geralmente é falta de uma das barras invertidas duplas (`\\`) ou aspas mal copiadas. Cole o comando em um editor de texto simples (Bloco de Notas), substitua os campos e só depois copie para o GitBash.

**Postman retorna 401 Unauthorized.** O Token Temporário pode ter expirado (validade de 7 dias). Solicite uma nova liberação ao Itaú. Confira também se `Bearer` está antes do token, separado por espaço.

**Postman retorna 400 Bad Request.** Normalmente o conteúdo do `.csr` no body está incompleto — abra o arquivo no Bloco de Notas e copie do `-----BEGIN CERTIFICATE REQUEST-----` até o `-----END CERTIFICATE REQUEST-----` inclusive.

**Erro ao salvar o .crt — fica salvando como .txt.** No Bloco de Notas, ao salvar, troque o "Tipo" para **"Todos os arquivos"** e digite o nome completo com a extensão (`API_BOLETO.crt`).

**Nexus não aceita o certificado.** Confira se anexou os arquivos corretos (`.crt` e `.key` — não o `.csr`) e se o Client Secret foi copiado sem espaços extras no início ou fim.

## Próximos passos

Com os certificados configurados, você pode:

- [Emitir boletos via API](#) — geração automática pelo módulo financeiro
- [Configurar remessa CNAB](#) — caso ainda use o fluxo tradicional como fallback
- [Conciliação bancária do Itaú](/artigos/conciliacao-bancaria/) — para fechar o ciclo
