---
title: "Nexus ERP e a Reforma Tributária"
module: "Fiscal"
difficulty: "Intermediária"
reading_time: 6
updated: 2026-05-22
summary: "Como ativar o envio dos dados da Reforma Tributária (CBS e IBS) no Nexus ERP — versões a partir de 15/12/2025 já vêm preparadas, basta ligar o parâmetro 6.009."
permalink: /artigos/reforma-tributaria/index.html
layout: artigo.njk
prerequisites:
  - "Nexus ERP atualizado para versão de 15/12/2025 ou posterior"
  - "Permissão para alterar configurações da empresa"
  - "Permissões de usuário 10.005 a 10.008 (se for necessário alterar tabelas)"
steps:
  - heading: "Confirme que sua versão do Nexus já contempla a Reforma"
    content: |
      As versões do **Nexus ERP a partir de 15/12/2025** já contemplam as novas regras de impostos da Reforma Tributária.
      
      Já estão configuradas no sistema:
      
      - Alíquotas de **CBS** e **IBS** (conforme última atualização do governo no Portal da Conformidade)
      - **Tipos de Alíquota**
      - **Classificações Tributárias**
      - **Operações Tributárias**
      - **Regras Fiscais**
      - **Relação de Anexos com NCMs**
    callout:
      type: info
      text: "💡 Se a sua versão for anterior a 15/12/2025, fale com o suporte do Nexus para atualizar antes de prosseguir."
  - heading: "Ative o Parâmetro 6.009 em cada empresa"
    content: |
      Para iniciar o envio do XML no novo padrão, ative o parâmetro em cada **Empresa Ativa**:
      
      **Configuração da Empresa > Aba: Nota Fiscal Eletrônica > marcar o Parâmetro 6.009 — "Ativar Envio dos Dados da Reforma Tributária"**
    image: /assets/img/artigos/reforma-tributaria/parametro-6009.png
    callout:
      type: warning
      text: "⚠️ <strong>Ative empresa por empresa.</strong> Em ambientes multi-empresa, cada CNPJ precisa ter o parâmetro 6.009 ligado individualmente."
  - heading: "Confira as operações onerosas (configuradas automaticamente)"
    content: |
      Com o parâmetro 6.009 ativo, as **operações onerosas** ficam automaticamente configuradas:
      
      - **Compra**
      - **Devolução**
      
      Nada precisa ser feito manualmente para essas operações.
  - heading: "Configure manualmente as operações Não Onerosas"
    content: |
      Outras operações precisam ser conferidas — **Bonificação, Remessa, Transferência** — pois o respectivo cadastro do **CFOP** no Nexus precisa ter o vínculo correto no campo de **Tipo de Operação**, que deve constar como **"Não Onerosa"**.
    image: /assets/img/artigos/reforma-tributaria/cfop-nao-onerosa.png
    callout:
      type: warning
      text: "⚠️ <strong>Conferência obrigatória:</strong> revise cada CFOP usado nessas operações. Vínculo errado gera XML com tributos incorretos."
  - heading: "Visualize os impostos calculados na aba IBS/CBS"
    content: |
      Após a ativação, para visualizar os resultados dos novos impostos, acesse a aba **"Impostos IBS/CBS"** da respectiva Nota Fiscal emitida.
    image: /assets/img/artigos/reforma-tributaria/aba-impostos-ibs-cbs.png
  - heading: "Acesse as Telas Novas da Reforma Tributária (se necessário)"
    content: |
      Para visualizar ou alterar as tabelas da Reforma Tributária, o usuário precisa das permissões **10.005 a 10.008**.
    image: /assets/img/artigos/reforma-tributaria/tabelas-reforma-1.png
    callout:
      type: info
      text: "💡 As tabelas já vêm pré-configuradas conforme o Portal da Conformidade. Só altere se houver instrução específica do seu contador."
  - heading: "Documentos oficiais de apoio"
    content: |
      Para consulta complementar, mantenha à mão os portais oficiais do governo:
      
      - **Classificação Tributária:** [dfe-portal.svrs.rs.gov.br/CFF/ClassificacaoTributaria](https://dfe-portal.svrs.rs.gov.br/CFF/ClassificacaoTributaria)
      - **Calculadora de Alíquotas (Piloto CBS):** [piloto-cbs.tributos.gov.br/servico/calculadora-consumo/calculadora/aliquotas](https://piloto-cbs.tributos.gov.br/servico/calculadora-consumo/calculadora/aliquotas)
    image: /assets/img/artigos/reforma-tributaria/tabelas-reforma-2.png
---

## Resumo da configuração

| Item | Onde fica | O que fazer |
|---|---|---|
| Versão Nexus | — | Confirmar ≥ 15/12/2025 |
| Parâmetro 6.009 | Configuração da Empresa > Aba NF-e | Ativar |
| Operações onerosas | CFOP de Compra/Devolução | Nada (automático) |
| Operações não onerosas | CFOP de Bonificação/Remessa/Transferência | Vincular como "Não Onerosa" |
| Permissões | Usuário 10.005 a 10.008 | Conceder a quem for editar tabelas |
| Conferência | Aba "Impostos IBS/CBS" na NF-e | Validar valores calculados |

## Problemas comuns

**Emiti NF-e sem CBS/IBS depois da ativação.** Verifique se o parâmetro 6.009 foi marcado **e salvo** na empresa correta — em multi-empresa, é comum salvar em uma e esquecer outra.

**Operação de bonificação saiu com tributos cheios.** O CFOP da bonificação não foi marcado como "Não Onerosa". Volte no cadastro do CFOP e ajuste o campo de tipo de operação.

**Não consigo abrir as tabelas da Reforma.** Falta permissão de usuário. Solicite ao administrador as permissões 10.005 a 10.008.

<div class="callout danger">
  <div>
    <strong>🚨 Recomendação:</strong> antes de ativar em produção, faça testes em ambiente de homologação emitindo notas de cada tipo de operação (venda, compra, devolução, bonificação, transferência) e conferindo os tributos calculados com o seu contador.
  </div>
</div>
