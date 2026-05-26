---
question: "O que fazer com as faixas de etiqueta antigas após migrar para a API dos Correios?"
category: suporte
search_keywords: "correios faixas etiqueta sigep api limpeza banco dados"
order: 111
---

Após a migração, as faixas de etiqueta armazenadas pelo SIGEP Web podem gerar conflito. Execute a consulta SQL abaixo no banco de dados para identificá-las e exclua os registros encontrados antes de emitir as primeiras etiquetas via API:

```sql
SELECT * FROM etiquetas_correios
WHERE id_nota_saida IS NULL
  AND id_cliente IS NULL
  AND data_emissao IS NULL
  AND id_transp = <id da transportadora Correios>
```
