# Portal de Conhecimento — Nexus ERP

Base de conhecimento web para os clientes do Nexus ERP. Construído com **Eleventy** (gerador de site estático) + **Decap CMS** (painel visual de edição) + **GitHub** + **Cloudflare Pages**.

**Resumo para a equipe:** editem o conteúdo pelo painel visual em `/admin`. O site se atualiza sozinho em ~1-2 minutos. Nada de mexer em código.

**Stack:**
- **GitHub** — armazena o código (gratuito)
- **Cloudflare Pages** — hospedagem e build automático (gratuito, ilimitado)
- **Decap CMS** — painel visual de edição (gratuito, open source)
- **GitHub OAuth** — login seguro para o painel `/admin`

---

## 🗺️ O que existe hoje no portal

- **5 páginas principais:** Início, Módulos, FAQ, Notícias, Vídeos
- **10 módulos do ERP** com busca integrada na sidebar
- **12 artigos publicados com imagens reais:**
  - Cadastro de Rota
  - Certificados API Itaú (Boleto Híbrido)
  - Certificado API Bradesco (Boleto Híbrido)
  - Conciliação da Conta Corrente com Arquivo OFX
  - Definir boleto padrão da empresa
  - Carta e Aviso de Cobrança
  - Migração Correios: SIGEP Web → Sigep Via API (Integrações)
  - Parametrização e Emissão de GNRE
  - Nexus ERP e a Reforma Tributária
  - Conciliação Marketplace
  - Geração de Contas a Receber na Devolução de Compra
- **16 FAQs** em 7 categorias
- **6 notícias/releases** com tags e imagens automáticas
- **6 vídeos** prontos para receber URL do YouTube

---

## 📦 Estrutura dos módulos e submenus

| Módulo | Submenus | Artigos vinculados |
|---|---|---|
| **Cadastros** | Clientes, Produtos, Equipamentos, Serviços | Cadastro de Rota (Clientes) |
| **Compras** | *(a definir)* | — |
| **Configurações** | Usuários, Configuração do Sistema, Empresas, Horários, Canais de Venda, Tipos de Pedido, Terminais, Andamentos, Integrações, Outros | Migração Correios: SIGEP Web → Sigep Via API (Integrações) |
| **Dashboard** | Dashboard Nexus | — |
| **E-commerce & Marketplaces** | Operações | Conciliação Marketplace (Operações) |
| **Estoque** | Inventário, Ajuste, Transferências, Históricos, Aferições | — |
| **Financeiro** | Bancos, Cartão de Crédito, Contas a Pagar, Contas a Receber, Cartas de Cobrança | API Itaú + API Bradesco + Boleto Padrão + Conciliação OFX (Bancos); Carta de Cobrança (Cartas de Cobrança); Geração de Contas a Receber na Devolução (Contas a Receber) |
| **Fiscal** | TES, TES Automática, NCM, CFOP, Alíquotas de ICMS, GNRE, Tributação de Serviços, Mensagem Tributária, SPEDs, Reforma Tributária, Outros | GNRE (GNRE); Reforma Tributária (Reforma Tributária) |
| **Relatórios & BI** | *(a definir)* | — |
| **Vendas** | Vendas, Separação, Expedição, Metas, Comissões, Outros | — |

---

## 📁 Estrutura de pastas

```
FAQ NEXUS/
├── _content/              ← CONTEÚDO EDITÁVEL PELO DECAP CMS
│   ├── faqs/              Perguntas frequentes (1 .md por pergunta)
│   ├── noticias/          Notícias importadas do Contabeis (geradas automaticamente)
│   ├── artigos/           Tutoriais passo a passo (1 .md por artigo)
│   └── videos/            Catálogo de vídeos (1 .md por vídeo)
│
├── _data/                 ← Dados globais
│   ├── contato.json       WhatsApp, e-mail, endereço
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
│
├── modulos/               ← Páginas estáticas dos módulos do ERP
│
├── _site/                 ← GERADO pelo Eleventy (não editar)
│
├── index.html             ← Home (estático)
├── modulos.html           ← Listagem de módulos (estático)
├── faq.njk                ← Template que monta /faq/
├── noticias.njk           ← Template que monta /noticias/
├── videos.njk             ← Template que monta /videos/
│
├── scripts/
│   └── import-noticias.py ← Script de importação automática do RSS do Contabeis
│
├── .eleventy.js           ← Configuração do gerador de site
├── package.json           ← Lista de dependências
└── .github/workflows/
    ├── build.yml              CI/CD — valida build a cada push
    └── import-noticias.yml    Importa notícias do Contabeis todo dia às 07h
```

---

## 📰 Importação automática de notícias

O portal importa notícias do **Contabeis.com.br** automaticamente todo dia às **07h00 (Brasília)** via GitHub Actions.

### Como funciona

1. O workflow `.github/workflows/import-noticias.yml` busca o RSS `https://www.contabeis.com.br/rss/noticias/`
2. O script `scripts/import-noticias.py` parseia os itens, extrai título, resumo, data, categoria e **imagem**
   - Extração de imagem com fallback triplo: elemento `media:content` (namespace Yahoo MRSS) → `<img src>` no HTML da `<description>` → qualquer atributo `url=` no XML
   - Suporte a URLs com query string (ex: `image.jpg?w=600`) via regex
3. Cria arquivos `.md` novos em `_content/noticias/` (artigos já existentes são ignorados)
4. Commita e faz push — o Cloudflare Pages reconstrói automaticamente

### Rodar manualmente

**GitHub → Actions → Importar Noticias Contabeis → Run workflow**

Parâmetros disponíveis:
- **Maximo de artigos:** quantos importar por execução (padrão: 20)
- **Ignorar artigos mais antigos que N dias** (padrão: 60)
- **Apagar e reimportar TODOS:** `true` para deletar os existentes e recriar com imagens

### Script local

```bash
# Importar as 20 notícias mais recentes dos últimos 60 dias
python scripts/import-noticias.py

# Reimportar tudo do zero (útil para corrigir imagens)
python scripts/import-noticias.py --reset

# Opções completas
python scripts/import-noticias.py --max 30 --days 90 --reset
```

### Formato do arquivo gerado

```yaml
---
layout: noticia.njk
title: "Título da notícia"
date: 2026-05-25
tag: aviso          # aviso / tutorial / evento / release
summary: "Resumo..."
thumb: "https://www.contabeis.com.br/assets/img/news/imagem.jpg"
source_url: "https://www.contabeis.com.br/noticias/..."
permalink: /noticias/slug-da-noticia/index.html
---
```

---

## 🚀 Guia de publicação (primeira vez)

Este setup leva entre **30 e 60 minutos** e depois é manutenção zero. Custo total: **R$ 0/mês**.

### Etapa 1 — Criar o repositório no GitHub

1. Acesse [github.com/new](https://github.com/new)
2. **Repository name:** `central-de-ajuda-nexus`
3. Visibilidade: **Public** (necessário no plano gratuito do Cloudflare para deploy automático)
4. **NÃO marque** README, .gitignore ou licença — vamos subir do nosso lado
5. Clique em **Create repository**

### Etapa 2 — Atualizar `admin/config.yml`

Abra `admin/config.yml` e troque a linha:

```yaml
repo: leonardo2020br/faq-nexus
```

Pelo nome real do seu repositório (`seu-usuario/central-de-ajuda-nexus`).

### Etapa 3 — Subir o código no GitHub

Abra o terminal/PowerShell na pasta do projeto e execute:

```bash
git init
git add .
git commit -m "primeira versao do portal"
git branch -M main
git remote add origin https://github.com/leonardo2020br/faq-nexus.git
git push -u origin main
```

### Etapa 4 — Conectar ao Cloudflare Pages

1. Acesse [dash.cloudflare.com](https://dash.cloudflare.com) → **Workers & Pages**
2. **Create application** → aba **Pages** → **Connect to Git**
3. Conecte sua conta GitHub e selecione o repositório
4. **Build settings:**
   - Framework preset: **Eleventy**
   - Build command: `npm run build`
   - Build output directory: `_site`
5. Em **Environment variables:** `NODE_VERSION` = `20`
6. **Save and Deploy**

Aguarde 1-2 minutos. O Cloudflare gera uma URL provisória tipo `ajuda-nexus.pages.dev`.

### Etapa 5 — Apontar o domínio `ajuda.nexuserp.com.br`

No painel do Cloudflare Pages → aba **Custom domains** → **Set up a custom domain** → `ajuda.nexuserp.com.br`.

No painel DNS de `nexuserp.com.br`, crie o registro:

| Tipo | Nome | Valor |
|---|---|---|
| **CNAME** | `ajuda` | `ajuda-nexus.pages.dev` |

Em 5-30 minutos o domínio passa a responder. O Cloudflare gera certificado SSL automaticamente.

### Etapa 6 — Configurar o OAuth do Decap CMS

O painel `/admin` precisa de um proxy OAuth para login com GitHub. Opção recomendada:

**Cloudflare Worker (gratuito):**

1. Acesse [github.com/settings/developers](https://github.com/settings/developers) → **OAuth Apps** → **New OAuth App**
   - Homepage URL: `https://ajuda.nexuserp.com.br`
   - Authorization callback URL: `https://decap-oauth.SEU_SUBDOMINIO.workers.dev/callback`
   - Anote o **Client ID** e **Client Secret**

2. No Cloudflare → **Workers & Pages** → **Create Worker** → Nome: `decap-oauth`
   - Use o código de [github.com/sterlp/decap-cms-oauth-cloudflare-worker](https://github.com/sterlp/decap-cms-oauth-cloudflare-worker)
   - Adicione como variáveis secretas: `OAUTH_CLIENT_ID` e `OAUTH_CLIENT_SECRET`
   - Deploy

3. Em `admin/config.yml`, ajuste:

```yaml
backend:
  name: github
  repo: leonardo2020br/faq-nexus
  branch: main
  base_url: https://decap-oauth.SEU_SUBDOMINIO.workers.dev
```

4. Commit e push → em ~2 minutos o `/admin` está funcionando com login GitHub.

> **Alternativa simples:** enquanto não configurar OAuth, editores podem editar arquivos `.md` diretamente pelo editor web do GitHub (botão "Edit this file"). Configure OAuth quando o ritmo de publicação justificar.

### Etapa 7 — Convidar a equipe editora

1. No repositório GitHub → **Settings → Collaborators → Add people**
2. Digite o usuário GitHub de cada pessoa que vai editar
3. Ela aceita o convite por e-mail e já pode logar no `/admin`

### Fluxo do dia a dia (depois de tudo configurado)

```
Editor abre /admin → escreve artigo → clica em Publish
       ↓
Decap CMS faz commit no GitHub
       ↓
Cloudflare Pages detecta o commit e roda o build
       ↓
Site atualiza em ~1-2 minutos
```

### Custo total

| Serviço | Custo |
|---|---|
| GitHub (repositório público) | R$ 0 |
| Cloudflare Pages (até 500 builds/mês) | R$ 0 |
| Cloudflare Worker (OAuth, 100k req/dia) | R$ 0 |
| Decap CMS | R$ 0 (open source) |
| Domínio `nexuserp.com.br` | Você já tem |
| **Total mensal** | **R$ 0** |

---

## ✏️ Como a equipe edita o conteúdo

### Acesso ao painel

1. Acessar **https://ajuda.nexuserp.com.br/admin/**
2. Clicar em **"Login with GitHub"**
3. Autorizar o aplicativo (apenas uma vez)
4. O painel mostra todas as coleções: FAQ, Notícias, Artigos, Vídeos, Configurações

### Criar/editar conteúdo

**Nova FAQ:**
1. Painel `/admin` → **❓ FAQ — Perguntas Frequentes** → **New Pergunta**
2. Preencher: pergunta, categoria, palavras-chave, resposta
3. **Publish** → aparece online em `/faq/` em ~1 minuto

**Novo artigo passo a passo:**
1. Painel `/admin` → **📖 Artigos & Tutoriais** → **New Artigo**
2. Título, módulo do ERP, dificuldade, tempo de leitura
3. Para cada passo: título, descrição, print da tela, callout opcional
4. Publicar

**Nova notícia:**
1. Painel `/admin` → **📰 Notícias & Atualizações** → **New Notícia**
2. Título, data, categoria (release/tutorial/aviso/evento), resumo, conteúdo
3. Publicar

**Novo vídeo:**
1. Painel `/admin` → **🎬 Vídeos & Tutoriais** → **New Vídeo**
2. URL do YouTube, categoria, duração, descrição
3. Publicar (thumbnail vem automaticamente do YouTube)

**Contatos da empresa:**
1. Painel `/admin` → **⚙️ Configurações gerais** → **Contatos da empresa**
2. Atualizar WhatsApp/e-mail/endereço → Publicar

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

## 🎨 Personalizar a identidade visual

Edite `assets/css/style.css`, bloco `:root` no topo:

```css
:root {
  --color-primary: #0B3D91;     /* Azul principal */
  --color-accent:  #00B8A9;     /* Verde-água accent */
}
```

Commit no GitHub → site atualiza em 1-2 minutos.

O logo é puxado de `https://nexuserp.com.br/img/logo-nexus.png` (sempre sincronizado com o site oficial).

---

## 🛠️ Para desenvolvedores: rodar localmente

Pré-requisitos: Node.js 20+.

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

## 🧩 Funcionalidades técnicas

### Dropdown de módulos no nav

O botão **Módulos** no menu superior abre um painel com os 10 módulos ao passar o cursor (desktop) ou tocar (mobile). Controlado por: bloco `NAV DROPDOWN` em `style.css` e `DROPDOWN MÓDULOS` em `main.js`.

### Formulário de chamado de suporte

O botão **"Abrir Chamado"** (na home e no rodapé) abre um modal com formulário completo: nome, empresa, e-mail, WhatsApp, módulo, tipo de ocorrência, descrição, upload de prints/vídeos (até 25 MB) e campo de link.

O envio vai para **suporte@nexuserp.com.br** via Formspree. **Configuração necessária:**
1. Crie conta grátis em [formspree.io](https://formspree.io)
2. Crie um form apontando para `suporte@nexuserp.com.br`
3. Copie o ID gerado (ex.: `xpwdkgrn`)
4. Em `assets/js/main.js`, substitua `SEU_FORM_ID` pelo ID

### Busca na sidebar dos módulos

Cada módulo tem um campo **"Buscar neste módulo..."** que filtra artigos em tempo real. Controlado por bloco `BUSCA NA SIDEBAR DO MÓDULO` em `main.js` + tag `<input data-sidebar-search>` nos templates de módulo.

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
Edite `admin/config.yml`, encontre o campo `category` da coleção FAQ e adicione no array `options`. Adicione também o botão de filtro correspondente em `faq.njk`.

**Quero mudar o layout/HTML de um artigo passo a passo.**
Edite `_includes/artigo.njk`. Esse arquivo controla como cada `.md` de `_content/artigos/` é renderizado.

**O site não está reconstruindo após publicar.**
Verifique no Cloudflare Pages → seu projeto → **Deployments**. Veja se o último deploy deu erro — os logs são exibidos na interface.

**`/admin` mostra tela em branco.**
O `config.yml` está com `repo` errado ou o OAuth não está respondendo. Abra o console do navegador (F12) para ver o erro exato.

**Editor não consegue logar no `/admin`.**
Confirme que ele é colaborador do repositório no GitHub e que aceitou o convite por e-mail.

**Quero voltar uma versão antiga do site.**
Cada deploy fica registrado no Cloudflare Pages com botão **"Rollback"**. Em 5 segundos você volta para uma versão anterior.

**Posso ter ambiente de teste e produção separados?**
Sim. Configure 2 projetos no Cloudflare Pages: um apontando para a branch `main` (produção) e outro para `develop` (homologação).

---

## 📅 Histórico de atualizações

### 26/05/2026
- **Fix imagens nos cards de notícias** — script `import-noticias.py` estava truncado (função `main()` inexistente); reescrito por completo. Extração de imagem corrigida com regex `IMG_RE` que suporta URLs com query string (ex: `image.jpg?w=600`); fallback triplo: elemento XML com `url=` → `<img src>` no HTML da description → qualquer atributo `url=` sem checar extensão
- **Importação automática de notícias** do Contabeis.com.br via RSS — workflow GitHub Actions roda todo dia às 07h, cria `.md` em `_content/noticias/` com imagem, resumo e link para o artigo original
- Script `scripts/import-noticias.py` com extração robusta de imagem (`media:content` e fallback `<img>` na description), suporte a `--reset`, `--max`, `--days`
- Workflow `import-noticias.yml` com disparo manual (parâmetros: max, days, reset) e agendamento diário

### 25/05/2026
- Novo artigo: **Geração de Contas a Receber na Devolução de Compra** (Financeiro → Contas a Receber) com 13 imagens
- **Modal de chamado de suporte** — botão "Abrir Chamado" na home e no rodapé abre formulário com upload de prints/vídeos; envio via Formspree para `suporte@nexuserp.com.br`
- **Dropdown de módulos no nav** — hover (desktop) e toque (mobile) abre painel com os 10 módulos
- **Contatos atualizados** — WhatsApp `5511960304708`, referências de telefone removidas
- Busca integrada na sidebar de todos os 10 módulos
- Novo artigo: **Conciliação Marketplace** (E-commerce → Operações)
- Novo artigo: **Certificado API Bradesco — Boleto Híbrido** (Financeiro → Bancos)
- Novo artigo: **Conciliação da Conta Corrente com Arquivo OFX** (Financeiro → Bancos)
- Novo artigo: **Migração Correios: SIGEP Web → Sigep Via API** (Configurações → Integrações)
- Submenu **Integrações** adicionado ao módulo Configurações
- Módulo Dashboard adicionado (10º módulo); módulos em ordem alfabética

### Sessões anteriores
- Estrutura inicial do portal: Home, Módulos, FAQ, Notícias, Vídeos
- 9 módulos configurados com submenus
- Artigos iniciais: API Itaú, Boleto padrão, Carta de Cobrança, Cadastro de Rota, GNRE, Reforma Tributária, Correios SIGEP→API
- Painel Decap CMS configurado em `/admin`
