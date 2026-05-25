---
title: "Cadastro de Rota"
module: "Cadastros"
difficulty: "Iniciante"
reading_time: 4
updated: 2026-05-22
summary: "Como cadastrar uma rota de entrega no Nexus ERP — definição por faixa de CEP e aplicação automática nos clientes."
permalink: /artigos/cadastro-rota/index.html
layout: artigo.njk
prerequisites:
  - "Acesso ao módulo ROTA"
  - "Lista das faixas de CEP que compõem cada rota a ser cadastrada"
  - "Permissão para alterar cadastros de clientes (necessária no passo final)"
steps:
  - heading: "Acesse o módulo ROTA"
    content: |
      Abra o módulo **ROTA** no Nexus ERP. Essa é a tela central de gestão das rotas de entrega da sua operação.
    image: /assets/img/artigos/cadastro-rota/01-acessar-modulo.jpg
  - heading: "Inclua uma nova rota"
    content: |
      Clique no botão para **incluir uma rota**. Será aberto o formulário para cadastrar uma rota nova, com nome e parâmetros de faixa de CEP.
    image: /assets/img/artigos/cadastro-rota/02-incluir-rota.png
  - heading: "Consulte o CEP"
    content: |
      Use a função de **Consultar CEP** para localizar e validar as faixas de CEP que farão parte dessa rota.
    image: /assets/img/artigos/cadastro-rota/03-consultar-cep.png
  - heading: "Determine UF, Cidade e Bairro"
    content: |
      Informe a **UF**, a **Cidade** e o **Bairro** que compõem o trecho desejado da rota. Esses filtros ajudam a delimitar com precisão as áreas de atendimento.
    image: /assets/img/artigos/cadastro-rota/04-definir-uf-cidade.png
  - heading: "Pesquise e exporte os CEPs"
    content: |
      Clique em **Pesquisar** para listar os CEPs que se enquadram nos filtros e em **Exportar** para vincular essa faixa de CEP à rota.
    image: /assets/img/artigos/cadastro-rota/05-pesquisar-exportar.png
    callout:
      type: info
      text: "💡 Você pode repetir os passos 3 a 5 várias vezes para somar diferentes faixas de CEP numa mesma rota."
  - heading: "Grave a rota"
    content: |
      Após adicionar todas as faixas de CEP desejadas, clique em **Gravar** para salvar a rota no sistema.
    image: /assets/img/artigos/cadastro-rota/06-gravar.jpg
  - heading: "Atualize a rota nos clientes"
    content: |
      Volte ao módulo **ROTA** e utilize a opção **[Atualizar Rota nos Clientes]**. O Nexus aplica automaticamente a rota cadastrada a todos os clientes cujo CEP se enquadra nas faixas parametrizadas.
    image: /assets/img/artigos/cadastro-rota/07-atualizar-rota-clientes.png
    callout:
      type: success
      text: "✅ <strong>Pronto!</strong> A partir desse momento, todos os clientes com CEP dentro das faixas configuradas passam a usar essa rota automaticamente."
---

## Como o Nexus aplica a rota

O sistema adota a rota determinada para **todas as faixas de CEP parametrizadas**. Ou seja: quando você executa "Atualizar Rota nos Clientes", o Nexus varre a base de clientes, confere o CEP de cada um e atribui a rota correspondente — sem necessidade de ajuste manual cliente a cliente.

## Problemas comuns

**A rota não foi atribuída a alguns clientes.** O CEP desses clientes provavelmente não está dentro das faixas cadastradas. Volte ao cadastro da rota e amplie as faixas, ou inclua uma nova rota cobrindo aquela região.

**Cliente apareceu em duas rotas após atualização.** O CEP do cliente está em sobreposição de faixas entre duas rotas diferentes. Ajuste as faixas de uma das rotas para eliminar a sobreposição.

**Cadastrei a rota, mas os clientes antigos continuam sem rota.** A vinculação não é automática para clientes já existentes. Sempre rode a opção **"Atualizar Rota nos Clientes"** após cadastrar ou alterar uma rota.

**Quero rota diferente para entrega de mercadoria vs cobrança.** O Nexus permite vincular tipos de rota distintos no cadastro do cliente. Verifique no módulo Cadastros > Clientes > aba Logística.
