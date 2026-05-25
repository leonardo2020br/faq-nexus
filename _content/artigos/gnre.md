---
title: "Parametrização e Emissão de GNRE"
module: "Fiscal"
difficulty: "Avançada"
reading_time: 10
updated: 2026-05-22
summary: "Como parametrizar a integração com o webservice da GNRE e emitir guias — individualmente após a NF-e ou em massa pelo módulo de Vendas."
permalink: /artigos/gnre/index.html
layout: artigo.njk
prerequisites:
  - "CNPJ, Razão Social e E-mail de cobrança da empresa em mãos"
  - "Acesso ao portal GNRE (https://www.gnre.pe.gov.br:444)"
  - "Permissão no Nexus para Fiscal > Alíquotas ICMS"
  - "Acesso ao servidor para colar a pasta FILES GNRE em C:\\SYSEMP"
  - "Fornecedor GNRE, grupo de despesas IMPOSTOS e despesa GNRE/DIFAL já cadastrados"
steps:
  - heading: "Acesse o portal da GNRE — módulo Automação"
    content: |
      Dentro do portal GNRE ([gnre.pe.gov.br](https://www.gnre.pe.gov.br:444/gnre/portal/GNRE_Principal.jsp)), localize o módulo **Automação** e clique em **"SAIBA MAIS"**.
    image: /assets/img/artigos/gnre/01-portal-automacao.png
  - heading: "Solicite o uso do Webservice"
    content: |
      Na página seguinte, clique em **"SOLICITAR USO DO WEBSERVICE"**.
    image: /assets/img/artigos/gnre/02-solicitar-webservice.png
  - heading: "Preencha os dados e valide o e-mail"
    content: |
      Informe **CNPJ, Razão Social e E-mail** e clique em **"SOLICITAR"**.
      
      Confira a caixa de entrada do e-mail informado e clique no link de validação enviado pela GNRE para concluir a habilitação.
    image: /assets/img/artigos/gnre/03-formulario-solicitacao.png
    callout:
      type: warning
      text: "⚠️ Sem a validação por e-mail, o webservice fica inativo. Confirme essa etapa antes de prosseguir no Nexus."
  - heading: "No Nexus, entre em Fiscal > Alíquotas ICMS"
    content: |
      Acesse o módulo **Fiscal** e abra **Alíquotas ICMS**.
    image: /assets/img/artigos/gnre/04-modulo-fiscal.png
  - heading: "Configure cada UF com os códigos da receita"
    content: |
      Selecione **uma UF por vez** e clique em **"Alterar"**. Preencha:
      
      - **ICMS Partilha:** `100102`
      - **FCP:** `100129`
      - **ICMS ST:** `100099`
      
      Na seção **Contas a Pagar**, informe:
      
      - **Fornecedor:** GNRE
      - **Grupo de despesas:** IMPOSTOS
      - **Despesa:** GNRE (ou DIFAL, conforme o caso)
      
      Repita para cada UF que sua empresa opera.
    image: /assets/img/artigos/gnre/05-aliquotas-icms.png
    callout:
      type: info
      text: "💡 Os códigos 100102/100129/100099 são padrão da receita estadual. Caso seu estado use códigos diferentes, valide com o contador."
  - heading: "Repita o processo para as alíquotas internas"
    content: |
      Ainda em **Alíquotas ICMS**:
      
      1. Desmarque a UF de origem **SP** e deixe **TODOS**
      2. Marque o checkbox **"Listar Apenas Alíquotas Internas"**
      3. Clique em **Pesquisar**
      4. Preencha os **mesmos campos** novamente (códigos da receita + contas a pagar)
    image: /assets/img/artigos/gnre/07-aliquotas-internas.png
  - heading: "Copie a pasta FILES GNRE para C:\\SYSEMP"
    content: |
      No servidor do Nexus, cole a pasta **FILES GNRE** dentro de `C:\SYSEMP`.
      
      Essa pasta contém os arquivos do webservice da GNRE. **Solicite ao suporte do Nexus** para obtê-la.
    image: /assets/img/artigos/gnre/08-pasta-files-gnre.png
    callout:
      type: danger
      text: "🚨 Sem a pasta FILES GNRE no caminho correto, a transmissão falha silenciosamente. Confirme com o suporte antes de testar emissões."
  - heading: "Emissão Individual — após cada NF-e"
    content: |
      Na **tela de transmissão de NFe (165)**, logo após a NF-e ser autorizada, clique no botão **GNRE**.
    image: /assets/img/artigos/gnre/09-emissao-individual-nfe.png
  - heading: "Transmita, imprima e lance no Contas a Pagar"
    content: |
      O sistema abre a tela de transmissão de GNRE. Clique em:
      
      - **Transmitir** — envia a guia para a SEFAZ
      - **Imprimir** — gera o PDF da guia para o cliente
      - **Contas a Pagar** — opcional; gera o registro financeiro automaticamente
    image: /assets/img/artigos/gnre/10-transmissao-gnre.png
    callout:
      type: success
      text: "✅ Pronto! A guia foi gerada, impressa e (se marcado) registrada nas contas a pagar como GNRE/DIFAL."
  - heading: "Emissão em Massa — pelo módulo Vendas"
    content: |
      Para gerar várias guias de uma vez, acesse o módulo **Vendas** e clique em **GERAR GNRE**.
    image: /assets/img/artigos/gnre/11-modulo-vendas.png
  - heading: "Filtre as guias pendentes"
    content: |
      Use os filtros disponíveis (período, UF, cliente, etc.) para localizar todas as guias pendentes que devem ser emitidas.
    image: /assets/img/artigos/gnre/12-gerar-gnre-filtros.png
  - heading: "Transmita em lote: Posicionada ou Todas"
    content: |
      Ao clicar em **Transmitir**, o sistema oferece duas opções:
      
      - **POSICIONADA** — apenas a guia atualmente selecionada
      - **TODAS** — todas as guias que estão na tela após o filtro
      
      Após a transmissão, **imprima** as guias e, se desejar, **gere os registros no Contas a Pagar**.
    image: /assets/img/artigos/gnre/13-transmitir-massa.png
    callout:
      type: success
      text: "🎉 Emissão em massa concluída. Todas as guias do filtro foram transmitidas e podem ser impressas/lançadas em uma única operação."
---

## Códigos de receita usados na configuração

| Item | Código |
|---|---|
| ICMS Partilha | 100102 |
| FCP | 100129 |
| ICMS ST | 100099 |

Esses códigos são os mais comuns. Se o estado da sua empresa usa códigos diferentes, valide com seu contador antes de aplicar.

## Resumo do fluxo

**Parametrização (faz uma vez):**

1. Habilitar webservice no portal da GNRE (CNPJ + e-mail validado)
2. No Nexus, em Fiscal > Alíquotas ICMS, preencher códigos de receita + contas a pagar para cada UF
3. Repetir para alíquotas internas (listar apenas internas, todos UFs)
4. Copiar pasta FILES GNRE para `C:\SYSEMP`

**Emissão (rotina):**

- **Individual** (NF-e a NF-e): tela 165 > botão GNRE > Transmitir > Imprimir > Contas a Pagar
- **Em massa** (lote): Vendas > Gerar GNRE > filtrar > Transmitir (Posicionada/Todas) > Imprimir > Contas a Pagar

## Problemas comuns

**Webservice retorna erro de autenticação.** O e-mail de validação não foi clicado, ou o CNPJ habilitado no portal não é o mesmo que está emitindo. Refaça a solicitação no portal GNRE.

**Mensagem "FILES GNRE não encontrado".** A pasta não está em `C:\SYSEMP` ou está com nome diferente. Confirme com o suporte do Nexus e copie exatamente como recebido.

**Guia emitida sem valor de FCP.** O código FCP (100129) não foi preenchido na alíquota interna daquele estado. Volte em Alíquotas ICMS, marque "Listar Apenas Alíquotas Internas" e revise.

**Contas a Pagar não foi gerada após a transmissão.** O botão "Contas a Pagar" precisa ser clicado manualmente após a transmissão — não é automático. Se o fornecedor GNRE ou a despesa não estiverem cadastrados, ele falha silenciosamente.

**Erro ao emitir em massa: "Sem permissão para fornecedor".** Usuário sem alçada para criar lançamentos no Contas a Pagar. Solicite ao administrador a permissão correspondente.
