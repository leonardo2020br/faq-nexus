---
title: "Migração Correios: SIGEP Web → API (PPN)"
module: "Configurações"
difficulty: "Avançada"
reading_time: 8
updated: 2026-05-22
summary: "Como migrar a integração com os Correios do antigo SIGEP Web para a nova API — geração de token, configuração da empresa, cadastro da transportadora e limpeza das faixas livres armazenadas."
permalink: /artigos/correios-sigep-ppn/index.html
layout: artigo.njk
prerequisites:
  - "Contrato dos Correios ativo e cadastro de Cartão de Postagem"
  - "Acesso ao Portal dos Correios para geração do Token (https://cws.correios.com.br/ajuda)"
  - "Permissão no Nexus para Configurações > Empresas e Cadastros > Parceiro de Negócios"
  - "Acesso ao banco SysEmp para executar o SELECT de limpeza das faixas livres antigas"
steps:
  - heading: "Ajuste a Configuração da Empresa para Sigep Via API"
    content: |
      Acesse no Nexus:
      
      **Configurações > Empresas > Configurações > Aba "17- Integrações" > Grupo de Configurações "Correios"**
      
      Defina:
      
      - **Modo:** Sigep Via API
      - **Modo de Transmissão PLP:** Sigep Via API
      - **Ambiente:** Produção
    image: /assets/img/artigos/correios-sigep-ppn/01-config-empresa-integracoes.png
  - heading: "Decida: reservar ou não reservar faixa de etiquetas"
    content: |
      Com a migração para API, surgiu o parâmetro **"Não Reservar Faixa de Etiqueta"**. Entenda a diferença:
      
      - **Antes (SIGEP Web):** era possível solicitar N faixas de Etiquetas e deixar armazenadas no SysEmp.
      - **Agora (API):** os Correios determinam a quantidade de etiquetas/mês com base na média de uso dos meses anteriores.
      
      A nova **modalidade por demanda** é ativada marcando **"Não Reservar Faixas de Etiqueta"** — a cada faturamento de NF, o sistema solicita uma faixa nova aos Correios, sem armazenar nada no ERP.
    callout:
      type: success
      text: "✅ <strong>Recomendação dos Correios:</strong> marcar <em>Não Reservar Faixa de Etiqueta</em>. Solicita sob demanda, alinhado à nova lógica da API."
  - heading: "Gere o Token no Portal dos Correios"
    content: |
      Após ajustar a Configuração da Empresa, acesse o **Portal dos Correios** para gerar o Token de uso da API:
      
      👉 [https://cws.correios.com.br/ajuda](https://cws.correios.com.br/ajuda)
      
      Siga o passo a passo do portal para gerar e copiar o **Token** — ele será usado no próximo passo como senha.
    callout:
      type: warning
      text: "⚠️ Guarde o Token em local seguro. Ele substitui a senha tradicional no fluxo da API."
  - heading: "Configure o Cadastro da Transportadora CORREIOS"
    content: |
      Volte ao Nexus e acesse:
      
      **SysEmp > Cadastros > Parceiro de Negócios > Localizar o cadastro da Transportadora: CORREIOS > Alterar > Aba: Transportadora**
      
      Configure:
      
      - ✅ **Marcar** o parâmetro **"Utilizar o Rastreio dos CORREIOS"**
      - **Usuário:** login utilizado no Portal dos Correios
      - **Senha:** o **Token da API** gerado no passo anterior (não é a senha tradicional)
      - **Cartão de Postagem:** número do contrato/cartão de postagem ativo
    image: /assets/img/artigos/correios-sigep-ppn/02-cadastro-transportadora.png
    callout:
      type: info
      text: "💡 O campo Senha agora recebe o Token. A senha pessoal usada no portal não é aceita pela API."
  - heading: "Limpe as Faixas Livres antigas (SIGEP Web)"
    content: |
      Na migração, é necessário **excluir do SysEmp todas as Faixas Livres** armazenadas pelo SIGEP Web — caso contrário, o sistema pode tentar usar etiquetas inválidas.
      
      Use o SELECT abaixo no banco para localizar as faixas livres da transportadora Correios:
      
      ```sql
      select * from etiquetas_correios 
       where id_nota_saida is null 
         and id_cliente is null 
         and data_emissao is null 
         and id_transp = {ID_DA_TRANSPORTADORA_CORREIOS};
      ```
      
      Substitua `{ID_DA_TRANSPORTADORA_CORREIOS}` pelo ID da transportadora Correios cadastrada na sua base. Após confirmar os registros, execute a exclusão das faixas livres listadas.
    callout:
      type: danger
      text: "🚨 <strong>Atenção:</strong> só exclua registros que tenham <code>id_nota_saida</code>, <code>id_cliente</code> e <code>data_emissao</code> nulos — esses são faixas <em>não utilizadas</em>. Etiquetas já emitidas/usadas não devem ser apagadas."
  - heading: "Gere etiquetas e PLP normalmente"
    content: |
      O processo de **geração de etiquetas e PLP permanece igual** — todas as telas foram tratadas para que a impressão funcione corretamente com a nova API.
      
      Para a geração de Etiqueta/PLP é **obrigatório** informar o **Tipo de Serviço** a ser utilizado, por exemplo:
      
      - **PAC**
      - **SEDEX**
    callout:
      type: success
      text: "🎉 <strong>Migração concluída.</strong> A partir daqui, todo o fluxo de postagem dos Correios passa pela nova API com solicitação de etiquetas sob demanda."
---

## Antes vs. Depois — o que muda na prática

| Aspecto | SIGEP Web (antigo) | API (atual) |
|---|---|---|
| Reserva de faixas | Possível reservar e armazenar várias | Solicitação por demanda recomendada |
| Limite de etiquetas | Definido pelo usuário | Determinado pelos Correios com base no histórico mensal |
| Autenticação | Usuário + senha tradicional | Usuário + Token gerado no portal |
| Geração de etiqueta/PLP | Igual | **Igual** (telas adaptadas) |
| Tipo de serviço (PAC/SEDEX) | Configurável | **Obrigatório** informar antes |

## Problemas comuns

**Etiqueta retorna erro de autenticação.** A senha cadastrada é a tradicional do portal — substitua pelo Token gerado em [cws.correios.com.br/ajuda](https://cws.correios.com.br/ajuda).

**Falha ao gerar PLP — "Faixa indisponível".** Significa que ainda existem faixas livres antigas (do SIGEP Web) no banco. Execute o SELECT do passo 5 e exclua os registros listados.

**Mensagem "Tipo de Serviço não informado".** Com a API, o tipo (PAC, SEDEX, etc.) virou obrigatório. Volte na tela de emissão e selecione o tipo antes de gerar.

**Cartão de postagem inválido.** Confirme no Portal dos Correios qual é o cartão ativo do contrato — pode ter sido renumerado. Atualize no cadastro da transportadora no Nexus.

**Quero continuar reservando faixas (não usar por demanda).** É possível desmarcar "Não Reservar Faixa de Etiqueta", mas a quantidade liberada pelos Correios continuará sendo definida pelo histórico mensal. A recomendação oficial continua sendo solicitar sob demanda.
