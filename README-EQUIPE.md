# Portal de Conhecimento — Nexus ERP

Base de conhecimento web para os clientes do Nexus ERP. Construído com Eleventy (gerador de site estático) + Decap CMS (painel visual de edição) + GitHub + Cloudflare Pages.

**Resumo:** sua equipe edita o conteúdo num painel visual estilo Word/Notion (`/admin`). O site se atualiza sozinho. Nada de mexer em código.

---

## 🗺️ O que existe hoje no portal

- **5 páginas principais:** Início, Módulos, FAQ, Notícias, Vídeos
- **10 módulos do ERP** com busca integrada na sidebar (ver estrutura detalhada abaixo)
- **11 artigos publicados com imagens reais:**
  - Cadastro de Rota
  - Certificados API Itaú (Boleto Híbrido)
  - Certificado API Bradesco (Boleto Híbrido)
  - Conciliação da Conta Corrente com Arquivo OFX
  - Definir boleto padrão da empresa
  - Carta e Aviso de Cobrança
  - Migração Correios SIGEP→API (Outros)
  - Migração Correios: SIGEP Web → Sigep Via API (Integrações)
  - Parametrização e Emissão de GNRE
  - Nexus ERP e a Reforma Tributária
  - Conciliação Marketplace
- **16 FAQs** em 7 categorias
- **6 notícias/releases** com tags
- **6 vídeos** prontos para receber URL do YouTube

---

## 📦 Estrutura dos módulos e submenus

| Módulo | Submenus | Artigos vinculados |
|---|---|---|
| **Cadastros** | Clientes, Produtos, Equipamentos, Serviços | Cadastro de Rota (Clientes) |
| **Compras** | *(a definir)* | — |
| **Configurações** | Usuários, Configuração do Sistema, Empresas, Horários, Canais de Venda, Tipos de Pedido, Terminais, Andamentos, Integrações, Outros | Correios — Migração SIGEP→API (Outros); Migração Correios: SIGEP Web → Sigep Via API (Integrações) |
| **Dashboard** | Dashboard Nexus | — |
| **E-commerce & Marketplaces** | Operações | Conciliação Marketplace (Operações) |
| **Estoque** | Inventário, Ajuste, Transferências, Históricos, Aferições | — |
| **Financeiro** | Bancos, Cartão de Crédito, Contas a Pagar, Contas a Receber, Cartas de Cobrança | API Itaú + API Bradesco + Boleto Padrão + Conciliação OFX (Bancos); Carta de Cobrança (Cartas de Cobrança) |
| **Fiscal** | TES, TES Automática, NCM, CFOP, Alíquotas de ICMS, GNRE, Tributação de Serviços, Mensagem Tributária, SPEDs, Reforma Tributária, Outros | GNRE (GNRE); Reforma Tributária (Reforma Tributária) |
| **Relatórios & BI** | *(a definir)* | — |
| **Vendas** | Vendas, Separação, Expedição, Metas, Comissões, Outros | — |

---

## 📁 Estrutura de pastas

```
FAQ NEXUS/
├── _content/              ← CONTEÚDO EDITÁVEL PELO DECAP CMS
│   ├── faqs/              Perguntas frequentes (1 .md por pergunta)
│   ├── noticias/          Notícias/releases (1 .md por notícia)
│   ├── artigos/           Tutoriais passo a passo (1 .md por artigo)
│   └── videos/            Catálogo de vídeos (1 .md por vídeo)
│
├── _data/                 ← Dados globais
│   ├── contato.json       Telefone, WhatsApp, e-mail, endereço
│   └── site.json          Nome, logo, URL principal
│
├── _includes/             ← Templates compartilhados
│   ├── base.njk           Header + footer (usado por todas as páginas)
│   ├── artigo.njk         Layout dos tutoriais passo a passo
│   └── noticia.njk        Layout das notícias
│
├── admin/                 ← PAINEL DO DECAP CMS
│   ├── index.html         Entrada do painel (acesse em /admin/)
│   └── config.yml         Configuração das coleções editáveis
│
├── assets/                ← CSS, JS, imagens
│   ├── css/style.css
│   ├── js/main.js
│   └── img/artigos/       Imagens dos tutoriais (1 pasta por artigo)
│       ├── bradesco-api-boleto/     (20 imagens)
│       ├── conciliacao-marketplace/ (7 imagens)
│       ├── conciliacao-ofx/         (7 imagens)
│       ├── gnre/
│       └── ...                      (demais artigos)
│
├── modulos/               ← Páginas estáticas dos módulos do ERP
│   ├── financeiro.html, estoque.html, vendas.html, ...
│
├── _site/                 ← GERADO pelo Eleventy (não editar)
│
├── index.html             ← Home (estático)
├── modulos.html           ← Listagem de módulos (estático)
├── faq.njk                ← Template que monta /faq/ a partir dos .md
├── noticias.njk           ← Template que monta /noticias/
├── videos.njk             ← Template que monta /videos/
│
├── .eleventy.js           ← Configuração do gerador de site
├── package.json           ← Lista de dependências
└── .github/workflows/     ← CI/CD para build automático
```

---

## 🔍 Busca dentro dos módulos

Cada página de módulo tem um campo **"Buscar neste módulo..."** no topo da sidebar. Ele filtra os artigos em tempo real conforme o usuário digita, ocultando automaticamente as seções sem resultado. Ao limpar o campo, tudo volta ao normal.

Esse comportamento é controlado por:
- **CSS:** bloco `.sidebar-search` em `assets/css/style.css`
- **JS:** bloco `BUSCA NA SIDEBAR DO MÓDULO` em `assets/js/main.js`
- **HTML:** tag `<input data-sidebar-search>` no topo do `<aside class="doc-sidebar">` de cada módulo

---

## 🖼️ Como adicionar imagens a um artigo

As imagens ficam em `assets/img/artigos/[slug-do-artigo]/` e são referenciadas no `.md` com o campo `image:` de cada passo.

**Extraindo imagens de um PDF ou DOCX (via script Python):**

```python
# Para DOCX — extrai todas as imagens embutidas
from docx import Document
doc = Document("arquivo.docx")
for i, rel in enumerate(doc.part.rels.values()):
    if "image" in rel.target_ref:
        with open(f"{i+1:02d}-passo.png", "wb") as f:
            f.write(rel.target_part.blob)

# Para PDF — renderiza cada página como imagem (requer pymupdf)
import fitz
doc = fitz.open("arquivo.pdf")
for i, page in enumerate(doc):
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    pix.save(f"{i+1:02d}-passo.png")
```

Salve as imagens na pasta do artigo e referencie no `.md`:
```yaml
steps:
  - heading: "Título do passo"
    content: "Descrição..."
    image: /assets/img/artigos/slug-do-artigo/01-passo.png
```

---

## ✏️ Como a equipe edita o conteúdo

### Acesso ao painel

1. Acessar **https://ajuda.nexuserp.com.br/admin/** (após publicação)
2. Clicar em **"Login with GitHub"**
3. Autorizar o aplicativo na conta GitHub (apenas uma vez)
4. O painel mostra todas as coleções: FAQ, Notícias, Artigos, Vídeos, Configurações

### Quem pode editar

Apenas pessoas adicionadas como **colaboradoras** do repositório no GitHub. Para adicionar alguém:

1. Acesse o repositório no GitHub
2. Clique em **Settings → Collaborators**
3. Add people com o usuário GitHub da pessoa
4. Ela aceita o convite por e-mail e já pode logar no `/admin`

### Como criar/editar conteúdo

**Criar uma nova FAQ:**

1. Painel `/admin` → clicar em **❓ FAQ — Perguntas Frequentes**
2. Botão **"New Pergunta"** no topo
3. Preencher: pergunta, categoria, palavras-chave (busca), resposta
4. Clicar em **"Publish"** (vai abrir um Pull Request no GitHub para revisão)
5. Em ~1 minuto, a FAQ aparece online em `/faq/`

**Criar um novo artigo passo a passo:**

1. Painel `/admin` → **📖 Artigos & Tutoriais** → **New Artigo**
2. Preencher: título, módulo do ERP, dificuldade, tempo de leitura
3. Adicionar pré-requisitos como lista
4. Para cada passo do tutorial:
   - Título do passo
   - Descrição (com formatação rica: negrito, listas, links)
   - Print da tela (upload direto pelo painel)
   - Callout opcional (dica/atenção/erro)
5. Publicar

**Criar uma notícia:**

1. Painel `/admin` → **📰 Notícias & Atualizações** → **New Notícia**
2. Preencher título, data, categoria (release/tutorial/aviso/evento), resumo
3. Escrever o conteúdo completo na área de texto rico
4. Publicar

**Adicionar um vídeo:**

1. Painel `/admin` → **🎬 Vídeos & Tutoriais** → **New Vídeo**
2. Colar URL do YouTube
3. Categoria, duração, descrição
4. Publicar (a thumbnail vem automaticamente do YouTube)

**Editar contatos da empresa:**

1. Painel `/admin` → **⚙️ Configurações gerais** → **Contatos da empresa**
2. Atualizar telefone/WhatsApp/e-mail/endereço
3. Publicar — todas as páginas se atualizam

---

## 🎨 Personalizar a identidade visual

Editar `assets/css/style.css`, bloco `:root` no topo:

```css
:root {
  --color-primary: #0B3D91;     /* Azul principal */
  --color-accent:  #00B8A9;     /* Verde-água accent */
  /* ... */
}
```

Mudou as cores → commit no GitHub → site se atualiza em 1-2 minutos.

### Logo

O logo é puxado direto de `https://nexuserp.com.br/img/logo-nexus.png` (sempre sincronizado com o site oficial). Para usar versão local, ver instruções no antigo README.

---

## 🛠️ Para desenvolvedores: rodar localmente

Pré-requisitos: Node.js 20+ instalado.

```bash
# Instalar dependências (primeira vez)
npm install

# Servidor local com hot reload
npm run dev
# Abre em http://localhost:8080

# Build de produção (gera _site/)
npm run build
```

---

## 🚀 Publicação

Veja o documento separado **GUIA-PUBLICACAO.md** com passo a passo de:

1. Criar repositório no GitHub
2. Subir o código
3. Conectar ao Cloudflare Pages
4. Configurar OAuth do Decap CMS
5. Apontar o domínio `ajuda.nexuserp.com.br`

---

## 📚 Referências técnicas

- **Eleventy:** https://www.11ty.dev/docs/
- **Decap CMS:** https://decapcms.org/docs/
- **Cloudflare Pages:** https://developers.cloudflare.com/pages/
- **Nunjucks (sintaxe dos templates):** https://mozilla.github.io/nunjucks/templating.html

---

## ❓ Perguntas frequentes (para a equipe técnica)

**Onde fica o conteúdo de uma FAQ depois que publico?**
Em `_content/faqs/[slug].md` no repositório. O Decap CMS commita esse arquivo, o Cloudflare Pages reconstrói o site.

**Posso editar um arquivo .md direto pelo VS Code?**
Sim. Tudo o que o Decap CMS faz é editar arquivos `.md` e `.json`. Você pode pular o painel e editar direto se preferir.

**Como adiciono uma categoria nova ao FAQ?**
Edite `admin/config.yml`, encontre o campo `category` da coleção FAQ e adicione uma opção no array `options`. Também adicione um botão no template `faq.njk`.

**Quero mudar o layout/HTML de um artigo passo a passo.**
Edite `_includes/artigo.njk`. Esse arquivo controla como cada `.md` da pasta `_content/artigos/` é renderizado.

**O site não está reconstruindo após publicar.**
Verifique no Cloudflare Pages → seu projeto → Deployments. Veja se o último deploy deu erro. Logs disponíveis na interface.

**Posso ter ambiente de teste e produção separados?**
Sim. Configure 2 projetos no Cloudflare Pages: um apontando para a branch `main` (produção) e outro para `develop` (homologação). O Decap CMS aponta para a branch onde commita.

---

## 📅 Histórico de atualizações

### 25/05/2026
- Busca integrada na sidebar de todos os 10 módulos (filtra artigos em tempo real por módulo)
- Novo artigo: **Conciliação Marketplace** (E-commerce → Operações) com 7 imagens extraídas do PDF
- Novo artigo: **Certificado API Bradesco — Boleto Híbrido** (Financeiro → Bancos) com 20 imagens extraídas do docx
- Novo artigo: **Conciliação da Conta Corrente com Arquivo OFX** (Financeiro → Bancos) com 7 imagens extraídas do docx
- Novo artigo: **Migração Correios: SIGEP Web → Sigep Via API** (Configurações → Integrações) com 2 imagens + query SQL de limpeza de faixas
- Novo submenu **Integrações** adicionado ao módulo Configurações
- Módulos em ordem alfabética na home e na listagem `/modulos/`
- Ícone dos módulos com fundo azul claro (`#e0ecff`)
- Módulo Dashboard adicionado (10º módulo)

### Sessões anteriores
- Estrutura inicial do portal: Home, Módulos, FAQ, Notícias, Vídeos
- 9 módulos configurados com submenus: Cadastros, Compras, Configurações, E-commerce, Estoque, Financeiro, Fiscal, Relatórios & BI, Vendas
- Artigos iniciais: API Itaú, Boleto padrão, Carta de Cobrança, Cadastro de Rota, GNRE, Reforma Tributária, Correios SIGEP→API
- Painel Decap CMS configurado em `/admin`
