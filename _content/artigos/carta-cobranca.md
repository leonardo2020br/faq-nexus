---
title: "Carta e Aviso de Cobrança — Manual e Automática"
module: "Financeiro"
difficulty: "Intermediária"
reading_time: 7
updated: 2026-05-22
summary: "Como configurar e emitir cartas/avisos de cobrança no Nexus ERP — modo manual (envio sob demanda) e automático (via robô durante a sincronização)."
permalink: /artigos/carta-cobranca/index.html
layout: artigo.njk
prerequisites:
  - "Permissão para acessar Configurações > Modelos de Carta de Cobrança"
  - "Configuração de e-mail padrão (SMTP) já realizada no Nexus"
  - "Para envio automático: arquivo robo_manifesto presente na pasta Sysemp"
steps:
  - heading: "Acesse a configuração do layout"
    content: |
      Navegue até:
      
      **Configurações > Configurações > Modelos de Carta de Cobrança > Incluir**
      
      Será aberta a tela de cadastro de um novo modelo (layout) de carta ou aviso de cobrança.
    image: /assets/img/artigos/carta-cobranca/01-layout-modelo.png
  - heading: "Preencha os campos do modelo"
    content: |
      Preencha os 7 campos da tela:
      
      1. **Descrição** — nome identificador do modelo (ex.: "Carta de Cobrança 30 dias").
      2. **Novo Status** — status que será atribuído ao título após o envio.
      3. **Tipo** — escolha **AVISO** (para títulos a vencer) ou **CARTA** (para títulos já vencidos).
         - Se **AVISO**: aparecerá o campo para definir o intervalo de dias futuros (de/até) que o sistema deve selecionar para envio.
         - Se **CARTA**: preencha a quantidade de dias vencidos para que o sistema selecione os títulos em atraso.
      4. **Enviar Cobrança Automático** — deixar como **NÃO** (configuração manual; veremos o automático mais adiante).
      5. **Assunto padrão** do e-mail.
      6. **Cabeçalho padrão** do corpo do e-mail.
      7. **Rodapé padrão** do corpo do e-mail.
      
      Clique em **Gravar**.
    callout:
      type: info
      text: "💡 Use variáveis dinâmicas no cabeçalho/rodapé (nome do cliente, valor, vencimento) se o seu modelo aceitar — isso personaliza cada envio sem trabalho manual."
  - heading: "Configure o e-mail de envio"
    content: |
      Para que o Nexus consiga enviar as cartas/avisos, é necessário ter o e-mail de envio configurado:
      
      **Configurações > Configurações > Configuração do Sistema > Aba "1 Configuração do Sistema" > Campo "Configuração de E-mail Padrão para Envio de Carta de Cobrança"**
      
      Preencha as credenciais SMTP da conta que vai enviar (servidor, porta, usuário, senha, criptografia).
    image: /assets/img/artigos/carta-cobranca/02-configurar-email.png
    callout:
      type: warning
      text: "⚠️ Em muitos provedores (Gmail, Microsoft 365) é necessário gerar uma <em>senha de aplicativo</em> em vez de usar a senha pessoal — confira a documentação do seu e-mail."
  - heading: "Emita a carta de cobrança (manual)"
    content: |
      Para o envio manual, vá em:
      
      **Financeiro > Contas a Receber > Menu "Funções" > Emissão de Carta de Cobrança**
      
      - Selecione o **layout configurado** anteriormente
      - Tipo de carta: **HTML**
      - Clique em **Pesquisar**
      
      O sistema trará os títulos na tela de acordo com o layout selecionado (vencidos para "CARTA", a vencer para "AVISO").
    image: /assets/img/artigos/carta-cobranca/03-emissao-envio.png
  - heading: "Envie por e-mail"
    content: |
      Com os títulos listados na tela, acesse o **Menu "Enviar por E-mail"**. O Nexus dispara o e-mail para cada cliente filtrado, usando o layout, assunto, cabeçalho e rodapé configurados no modelo.
    callout:
      type: success
      text: "✅ Os títulos selecionados recebem o <em>Novo Status</em> definido no passo 2, evidenciando que a cobrança foi enviada."
  - heading: "Configure o envio automático (opcional)"
    content: |
      Para que o Nexus envie cartas/avisos automaticamente, durante a sincronização do sistema:
      
      No cadastro do modelo (passos 1 e 2), no campo **4 - "Enviar Cobrança Automático"**, marque **SIM** em vez de NÃO.
    image: /assets/img/artigos/carta-cobranca/04-automatica.png
  - heading: "Habilite o robô de envio automático"
    content: |
      O envio automático é feito por um robô que roda junto com a sincronização. Para ativá-lo, dois requisitos:
      
      1. **Arquivo `robo_manifesto`** — confirme que está presente na pasta `Sysemp` do servidor.
      2. **Linha no config da máquina remetente**, incluir:
      
      ```
      ROBO_MANIFESTO=SIM
      ```
      
      Reinicie o serviço de sincronização após a alteração para que o robô passe a executar.
    callout:
      type: success
      text: "🎉 <strong>Pronto!</strong> A partir daqui, o robô do Nexus selecionará os títulos enquadrados no modelo e disparará as cartas/avisos automaticamente — sem intervenção manual."
---

## Quando usar Aviso vs Carta

| Tipo | Para quando | Exemplo de uso |
|---|---|---|
| **AVISO** | Títulos **a vencer** (futuro) | "Sua fatura vence em 3 dias" |
| **CARTA** | Títulos **vencidos** (passado) | "Sua fatura está em atraso há 15 dias" |

Você pode criar **múltiplos modelos** para diferentes momentos da régua de cobrança (aviso 5 dias antes, carta 5 dias após o vencimento, carta 15 dias, carta 30 dias, etc.).

## Problemas comuns

**O e-mail não está sendo enviado.** Verifique a configuração SMTP (passo 3). Teste enviar um e-mail de outro lugar com as mesmas credenciais para confirmar que estão corretas.

**Provedor pede "senha de aplicativo".** Gmail e Microsoft 365 exigem uma senha específica gerada nas configurações de segurança da conta — a senha do usuário normal não funciona.

**Robô automático não está enviando.** Confira:
1. O arquivo `robo_manifesto` existe na pasta `Sysemp`
2. A linha `ROBO_MANIFESTO=SIM` está no config da máquina remetente
3. O serviço de sincronização foi reiniciado após a alteração
4. O modelo de carta está com "Enviar Cobrança Automático" = SIM

**Quero suspender o envio para alguns clientes.** Normalmente o cadastro do cliente tem a opção "Não receber cobrança automática" ou similar — verifique na aba financeira do cliente.

**Os títulos não aparecem no Pesquisar.** Confirme que o filtro de dias do modelo está coerente com a situação dos títulos (se a carta é "15 dias vencidos", só vai pegar títulos com 15+ dias de atraso).
