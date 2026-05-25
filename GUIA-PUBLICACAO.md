# Guia de Publicação — Central de Ajuda Nexus

Este guia mostra como tirar o portal do seu computador e colocar no ar como `https://ajuda.nexuserp.com.br/`. Setup leva entre **30 e 60 minutos**, e depois é manutenção zero.

**Stack final:**

- **GitHub** — armazena o código (gratuito)
- **Cloudflare Pages** — hospedagem e build automático (gratuito, ilimitado)
- **Decap CMS** — painel visual para a equipe editar (gratuito)
- **GitHub OAuth** — login do painel `/admin`

---

## ✅ Pré-requisitos

- Conta no GitHub (você já tem)
- Conta no Cloudflare (criar grátis em [dash.cloudflare.com](https://dash.cloudflare.com))
- Acesso ao painel DNS do domínio `nexuserp.com.br` (para apontar o subdomínio)

---

## Etapa 1 — Criar o repositório no GitHub

1. Acesse [github.com/new](https://github.com/new)
2. **Repository name:** `central-de-ajuda-nexus`
3. **Description:** Base de conhecimento web para clientes do Nexus ERP
4. Visibilidade: **Public** (necessário no plano gratuito do Cloudflare para deploy automático sem token; ou Private se quiser e estiver tudo bem configurar token de acesso)
5. **NÃO marque** as opções "Add README", "Add .gitignore", "Choose a license" — vamos subir do nosso lado
6. Clicar em **Create repository**

Anote o nome completo: `seu-usuario/central-de-ajuda-nexus`

---

## Etapa 2 — Atualizar `admin/config.yml` com o nome do repo

Abra `admin/config.yml` no projeto e troque a linha:

```yaml
repo: leonardo2020br/faq-nexus
```

Pelo nome real do seu repositório. Salve.

---

## Etapa 3 — Subir o código no GitHub

Abra o terminal/PowerShell na pasta do projeto (`C:\Users\Léo Nexus\Documents\Claude\Projects\FAQ NEXUS`) e execute:

```bash
git init
git add .
git commit -m "primeira versao do portal"
git branch -M main
git remote add origin https://github.com/leonardo2020br/faq-nexus.git
git push -u origin main
```

Se for a primeira vez usando Git, vai pedir login no GitHub.

---

## Etapa 4 — Conectar ao Cloudflare Pages

1. Acesse [dash.cloudflare.com](https://dash.cloudflare.com) → menu lateral **Workers & Pages**
2. Clicar em **Create application** → aba **Pages** → **Connect to Git**
3. Conectar sua conta GitHub e selecionar o repositório `central-de-ajuda-nexus`
4. **Set up build:**
   - Project name: `ajuda-nexus`
   - Production branch: `main`
   - Framework preset: **Eleventy**
   - Build command: `npm run build`
   - Build output directory: `_site`
   - Root directory: (deixe vazio)
5. Em **Environment variables**, adicionar:
   - `NODE_VERSION` = `20`
6. Clicar em **Save and Deploy**

Aguarde 1-2 minutos. Quando terminar, o Cloudflare te dá uma URL provisória tipo `ajuda-nexus.pages.dev`. Acesse e confirme que o portal está no ar.

---

## Etapa 5 — Apontar o domínio `ajuda.nexuserp.com.br`

### No Cloudflare Pages:

1. No projeto → aba **Custom domains** → **Set up a custom domain**
2. Digite: `ajuda.nexuserp.com.br`
3. Continue

### No painel DNS de `nexuserp.com.br`:

(A localização depende de onde o domínio está hospedado — Registro.br, hospedagem atual da Nexus, etc.)

Crie um registro do tipo:

| Tipo | Nome | Valor |
|---|---|---|
| **CNAME** | `ajuda` | `ajuda-nexus.pages.dev` |

Em 5-30 minutos, `https://ajuda.nexuserp.com.br/` passa a responder com o portal.

> O Cloudflare gera certificado SSL automaticamente — não precisa configurar nada.

---

## Etapa 6 — Configurar o OAuth do Decap CMS (login GitHub)

O painel `/admin` precisa de um "proxy OAuth" para que os editores façam login com GitHub. Existem 3 caminhos:

### Caminho A — Cloudflare Worker (recomendado, 100% gratuito)

1. Criar GitHub OAuth App:
   - Acessar [github.com/settings/developers](https://github.com/settings/developers) → **OAuth Apps** → **New OAuth App**
   - **Application name:** Decap CMS — Ajuda Nexus
   - **Homepage URL:** `https://ajuda.nexuserp.com.br`
   - **Authorization callback URL:** `https://decap-oauth.SEU_SUBDOMINIO.workers.dev/callback`
   - Anotar **Client ID** e **Client Secret**

2. Criar o Worker no Cloudflare:
   - Workers & Pages → **Create application** → **Workers** → **Create Worker**
   - Nome: `decap-oauth`
   - Copiar o código de [github.com/sterlp/decap-cms-oauth-cloudflare-worker](https://github.com/sterlp/decap-cms-oauth-cloudflare-worker) (ou similar)
   - Adicionar como variáveis secretas: `OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET`
   - Deploy

3. Em `admin/config.yml`, ajustar:

```yaml
backend:
  name: github
  repo: leonardo2020br/faq-nexus
  branch: main
  base_url: https://decap-oauth.SEU_SUBDOMINIO.workers.dev
```

4. Commit e push. Em 1-2 minutos o `/admin` está funcionando com login GitHub.

### Caminho B — Netlify Identity (mais simples, mas precisa Netlify)

Se preferir não montar OAuth manualmente, basta:

1. Criar conta gratuita em [netlify.com](https://netlify.com)
2. Importar o repositório lá (Netlify também faz deploy estático)
3. Ativar **Identity** → **Git Gateway**
4. Em `admin/config.yml`, trocar `name: github` por `name: git-gateway`
5. Convidar editores por e-mail (Netlify cria contas para eles)

> Nesse caso, você pode ter dois deploys (Cloudflare Pages como produção pública e Netlify só para servir o `/admin`) ou migrar tudo para Netlify.

### Caminho C — Adiar OAuth (começar editando direto no GitHub)

Enquanto não configurar OAuth, editores podem **editar arquivos `.md` direto pelo GitHub web** (botão "edit this file" no editor do GitHub). Funciona perfeitamente para começar; configure OAuth quando o ritmo de publicação justificar.

---

## Etapa 7 — Convidar a equipe editora

1. No GitHub: **Settings → Collaborators → Add people**
2. Digite o usuário GitHub de cada pessoa que vai editar
3. Eles aceitam o convite por e-mail
4. Pronto — acesso ao `/admin` liberado

---

## Etapa 8 — Configurar o robô do GitHub Actions (opcional)

O projeto já vem com `.github/workflows/build.yml` que:

- Roda `npm install` + `npm run build` a cada push
- Valida que o site compila antes do Cloudflare publicar

Funciona automaticamente — não precisa configurar nada. Se quiser desativar, basta deletar `.github/workflows/`.

---

## 🔁 Fluxo do dia a dia (depois de tudo configurado)

```
Editor abre /admin → escreve artigo → clica em Publish
       ↓
Decap CMS faz commit no GitHub
       ↓
Cloudflare Pages detecta o commit e roda o build
       ↓
Site atualiza em ~1-2 minutos
```

Você não precisa fazer absolutamente nada — apenas garantir que o repositório, o Cloudflare e o OAuth estejam funcionando. Manutenção zero.

---

## 💰 Custo total

| Serviço | Custo |
|---|---|
| GitHub (repositório público) | R$ 0 |
| Cloudflare Pages (até 500 builds/mês) | R$ 0 |
| Cloudflare Worker (OAuth, 100k requisições/dia) | R$ 0 |
| Decap CMS | R$ 0 (open source) |
| Domínio `nexuserp.com.br` | Você já tem |
| **Total mensal** | **R$ 0** |

---

## 🆘 Problemas comuns

**Build falhou no Cloudflare.** Verifique a aba "Deployments" no projeto Pages, abra o deploy com erro e veja o log. Normalmente é variável de ambiente faltando ou syntax error em algum `.md` recém-publicado.

**`/admin` mostra tela em branco.** O `config.yml` está com `repo` errado ou o OAuth não está respondendo. Abra o console do navegador (F12) para ver o erro exato.

**Editor não consegue logar no `/admin`.** Confirme que ele é colaborador do repositório no GitHub e que aceitou o convite por e-mail.

**Mudei um arquivo no GitHub mas o site não atualizou.** Cloudflare Pages só rebuildá se houver commit em arquivos relevantes. Confira a aba Deployments — costuma demorar 30s a 2min.

**Quero voltar uma versão antiga.** Cada deploy fica registrado no Cloudflare Pages com botão "Rollback". Em 5 segundos você volta para uma versão anterior.

---

## 📞 Suporte

Em caso de dúvida sobre a infraestrutura, abra um issue no próprio repositório ou consulte:

- Docs Cloudflare Pages: https://developers.cloudflare.com/pages/
- Docs Decap CMS: https://decapcms.org/docs/intro/
- Docs Eleventy: https://www.11ty.dev/docs/
