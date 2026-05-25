---
title: "Certificado API Bradesco (Boleto Híbrido)"
module: "Financeiro"
difficulty: "Avançada"
reading_time: 15
updated: 2026-05-25
summary: "Passo a passo completo para configurar a integração com a API do Bradesco: cadastro no portal Developers, inscrição nos produtos, criação de aplicativos, geração de credenciais e configuração no SysEmp."
permalink: /artigos/bradesco-api-boleto/index.html
layout: artigo.njk
prerequisites:
  - "Certificado digital da empresa (.pfx) com senha"
  - "Acesso ao portal Bradesco Developers (o cliente deve ter conta criada)"
  - "Gerência do Bradesco do cliente deve habilitar: Cobrança Bancária, Pix, CBON (para e-commerce se aplicável)"
  - "OpenSSL disponível no servidor (pasta C:\\sysemp\\SSL_EXTRATO)"
  - "Acesso à Carteira de Cobrança no SysEmp para inserir as credenciais"
steps:
  - heading: "Cadastro no Bradesco Developers"
    content: |
      O cliente deve acessar o portal do Bradesco Developers e realizar seu cadastro:

      **https://developers.bradesco.com.br/**

      Após o cadastro, o cliente enviará os dados de acesso para que a equipe Nexus prossiga com as configurações.
    image: /assets/img/artigos/bradesco-api-boleto/01-passo.png

  - heading: "Acessar o Portal e ir em Produtos"
    content: |
      Com acesso ao portal, vá até **Produtos**. O procedimento precisa ser realizado em **3 produtos**:

      - **Cobrança com QR Code**
      - **Cobrança**
      - **Pix — geração de QR Code**
    image: /assets/img/artigos/bradesco-api-boleto/02-passo.png

  - heading: "Filtrar e abrir cada Produto"
    content: |
      Use o filtro para localizar cada um dos 3 produtos listados e clique para abri-los individualmente.

      Você repetirá as próximas etapas de inscrição para cada produto.
    image: /assets/img/artigos/bradesco-api-boleto/03-passo.png

  - heading: "Inscrever-se em cada Produto (Ambiente de Produção)"
    content: |
      Dentro de cada produto, clique em **"Inscrever-se"** e preencha as informações de inscrição selecionando o **Ambiente de Produção**.

      Em seguida, clique em **"Enviar Solicitação"**. A solicitação ficará pendente de autorização.
    image: /assets/img/artigos/bradesco-api-boleto/05-passo.png
    callout:
      type: warning
      text: "⏳ O Bradesco geralmente demora entre 1 e 2 dias úteis para aprovar a solicitação. Após aprovado, o status será atualizado no portal."

  - heading: "Criar os Aplicativos necessários"
    content: |
      Após a aprovação das inscrições, registre **dois aplicativos** para a equipe **Default Team**:

      - **1º Aplicativo:** Boleto Híbrido
      - **2º Aplicativo:** Pix Recebidos

      Crie ambos antes de prosseguir para o registro das aplicações nos produtos.
    image: /assets/img/artigos/bradesco-api-boleto/08-passo.png

  - heading: "Registrar Aplicações nos Produtos"
    content: |
      Em **Produtos**, clique em **"Registrar Aplicação"** e associe cada recurso ao aplicativo correto, sempre em **Produção**:

      **Produto: Cobrança com QR Code** → Aplicativo: *Boleto Híbrido*
      - Cobrança com QRCode — Alteração de boleto com QRCode
      - Cobrança com QRCode — Registro de boleto com QRCode

      **Produto: Pix — geração de QR Code** → Aplicativo: *Pix Recebidos*
      - PIX Gerenciamento de Recebidos

      **Produto: Cobrança** → Aplicativo: *Boleto Híbrido*
      - Cobrança — Consulta de boleto específico e emissão de 2ª via
      - Cobrança — Consulta lista de boletos pendentes de liquidação
      - Cobrança — Solicitação de baixa de boleto
      - Cobrança — Listar boletos liquidados
    image: /assets/img/artigos/bradesco-api-boleto/10-passo.png

  - heading: "Solicitar Credencial — Converter Certificado .pfx em .pem"
    content: |
      Para solicitar a credencial no portal, é necessário converter o certificado da empresa de **.pfx para .pem**.

      **Passo 1:** Copie o arquivo **.pfx** da empresa para a pasta:
      ```
      C:\sysemp\SSL_EXTRATO
      ```

      **Passo 2:** No Windows Explorer, navegue até essa pasta e clique na barra de endereços, digite **CMD** e pressione Enter para abrir o prompt de comando na pasta.

      **Passo 3:** Execute o comando abaixo (substituindo o nome do arquivo e a senha):
      ```
      openssl.exe pkcs12 -in NomeDoArquivo.pfx -nokeys -out cert_publico.pem -passin pass:SenhaDoCertificado
      ```

      O arquivo **cert_publico.pem** será gerado na mesma pasta.

      **Passo 4:** De volta ao portal Bradesco Developers, solicite a **Credencial** nos produtos abaixo, selecionando o `cert_publico.pem` gerado:

      - **Cobrança com QR Code** → Credencial *Boleto*
        - Cobrança com QRCode — Registro de boleto com QRCode
        - Cobrança com QRCode — Alteração de boleto com QRCode
      - **Cobrança** → Credencial *Boleto*
        - Consulta de boleto específico e emissão de 2ª via
        - Consulta lista de boletos pendentes de liquidação
        - Solicitação de baixa de boleto
        - Listar boletos liquidados
      - **Pix — geração de QR Code** → Credencial *Pix Recebidos*
        - PIX Gerenciamento de Recebidos
    image: /assets/img/artigos/bradesco-api-boleto/15-passo.png
    callout:
      type: info
      text: "💡 Serão geradas 2 credenciais: uma para Boleto e uma para Pix. Cada uma terá seu próprio Client ID e Client Secret."

  - heading: "Configurar as Credenciais no SysEmp"
    content: |
      Após a aprovação das credenciais no portal Bradesco, você terá **2 Client ID** e **2 Client Secret** — um par para Boleto e outro para Pix.

      Acesse a **Carteira de Cobrança no SysEmp** e insira esses valores nos campos correspondentes.
    image: /assets/img/artigos/bradesco-api-boleto/18-passo.png
    callout:
      type: success
      text: "✅ Configuração concluída! O Boleto Híbrido e o Pix estão integrados ao SysEmp via API Bradesco."
---

## Habilitações necessárias pelo gerente Bradesco do cliente

Antes de iniciar o processo, o gerente do cliente no Bradesco precisa habilitar os seguintes serviços na conta:

- Cobrança Bancária (Boleto)
- Pix
- CBON (obrigatório se o cliente emitir boletos para e-commerce)

Sem essas habilitações, erros ocorrerão durante a emissão de boletos.

## Erros comuns

**`IDENTIFICADOR DO PRODUTO NAO CADASTRADO`**

```
statusHttp: 400 — IDENTIFICADOR DO PRODUTO NAO CADASTRADO
```

Ocorre quando o gerente Bradesco não habilitou os produtos na conta. Solicite ao cliente que entre em contato com seu gerente para liberar Cobrança Bancária e Pix.

**`REGISTRO DE TITULOS ECOMMERCE NAO CONTRATADO`**

```
statusHttp: 400 — REGISTRO DE TITULOS ECOMMERCE NAO CONTRATADO
```

Necessário quando o cliente usa e-commerce. Solicite ao gerente a liberação do scope **CBON**.

## Resumo do fluxo

1. Cliente se cadastra em **developers.bradesco.com.br** e passa os dados de acesso
2. No portal: inscrição nos 3 produtos em Produção (aguardar 1-2 dias úteis para aprovação)
3. Criar 2 aplicativos: **Boleto Híbrido** e **Pix Recebidos** para a equipe Default Team
4. Registrar as aplicações de cada produto no aplicativo correspondente
5. Converter certificado `.pfx` → `.pem` via OpenSSL em `C:\sysemp\SSL_EXTRATO`
6. Solicitar credenciais nos produtos usando o `cert_publico.pem`
7. Inserir os 2 pares de Client ID / Client Secret na Carteira de Cobrança no SysEmp
