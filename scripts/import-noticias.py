#!/usr/bin/env python3
"""
import-noticias.py
==================
Importa noticias do RSS do Contabeis (https://www.contabeis.com.br/rss/noticias/)
e cria arquivos Markdown em _content/noticias/ para o site FAQ NEXUS (Eleventy).

Como usar:
  python scripts/import-noticias.py [--max 20] [--days 60] [--reset]

Flags:
  --max    Numero maximo de artigos a importar (padrao: 20)
  --days   Ignorar artigos mais antigos que N dias (padrao: 60)
  --reset  Apaga TODOS os arquivos existentes em _content/noticias/ antes de importar
           (util para reimportar com imagens apos correcao do script)
"""

import os
import re
import sys
import html
import argparse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

# Configuracoes
RSS_URL   = "https://www.contabeis.com.br/rss/noticias/"
OUT_DIR   = "_content/noticias"
THUMB_DEFAULT = "\U0001f4f0"

CATEGORY_MAP = {
    "legislacao":  "aviso",
    "fiscal":      "aviso",
    "tributario":  "aviso",
    "tutorial":    "tutorial",
    "artigo":      "tutorial",
    "evento":      "evento",
    "release":     "release",
    "atualizacao": "release",
}


def slugify(text):
    replacements = {
        'a':['a','a','a','a','a'],'e':['e','e','e','e'],'i':['i','i','i','i'],
        'o':['o','o','o','o','o'],'u':['u','u','u','u'],'c':['c'],'n':['n'],
    }
    import unicodedata
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text[:80]


def strip_html(raw):
    text = re.sub(r'<[^>]+>', '', raw or '')
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def guess_tag(categories):
    import unicodedata
    for cat in categories:
        key = cat.lower().strip()
        key_norm = ''.join(c for c in unicodedata.normalize('NFD', key) if unicodedata.category(c) != 'Mn')
        for k, v in CATEGORY_MAP.items():
            if k in key_norm:
                return v
    return "aviso"


def truncate(text, max_chars=220):
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(' ', 1)[0] + '...'


def existing_slugs():
    slugs = set()
    if not os.path.isdir(OUT_DIR):
        return slugs
    for f in os.listdir(OUT_DIR):
        if f.endswith('.md'):
            slugs.add(f[:-3])
    return slugs


def fetch_rss():
    req = urllib.request.Request(
        RSS_URL,
        headers={'User-Agent': 'FAQ-NEXUS-Bot/1.0 (+https://faq-nexus.leossapo-2014.workers.dev)'}
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()


IMG_RE = re.compile(r'\.(jpg|jpeg|png|gif|webp|avif)(\?|$|#)', re.IGNORECASE)


def _is_image_url(url):
    return bool(url.startswith('http') and IMG_RE.search(url))


def extract_image(item, desc_raw, content_enc_text=''):
    # Debug: mostra desc_raw para diagnostico
    if desc_raw:
        print("  [dbg] desc_raw[:200]: " + repr(desc_raw[:200]))

    # 1. Itera TODOS os filhos procurando atributo url com imagem
    for el in item.iter():
        url = el.get('url', '').strip()
        if _is_image_url(url):
            print("  [img] via element '" + el.tag + "': " + url[:80])
            return url

    # 2. <img src="..."> no HTML da description e content:encoded
    for html_src in (desc_raw or '', content_enc_text or ''):
        img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html_src, re.IGNORECASE)
        if img_match:
            url = img_match.group(1).strip()
            if _is_image_url(url):
                print("  [img] via <img> no HTML: " + url[:80])
                return url

    # 3. Qualquer atributo url sem checar extensao
    for el in item.iter():
        url = el.get('url', '').strip()
        if url.startswith('http'):
            print("  [img] via element '" + el.tag + "' (sem ext): " + url[:80])
            return url

    print("  [img] nenhuma imagem encontrada, usando emoji")
    return THUMB_DEFAULT


def parse_items(xml_bytes):
    root = ET.fromstring(xml_bytes)
    ns = {'content': 'http://purl.org/rss/1.0/modules/content/'}
    items = []
    for item in root.iter('item'):
        title    = (item.findtext('title') or '').strip()
        link     = (item.findtext('link') or '').strip()
        desc_raw = item.findtext('description') or ''
        description = strip_html(desc_raw)
        pub_date    = item.findtext('pubDate') or ''
        categories  = [c.text.strip() for c in item.findall('category') if c.text]

        content_enc = item.find('content:encoded', ns)
        content_enc_text = ''
        if content_enc is not None and content_enc.text:
            content_enc_text = content_enc.text
            long_desc = strip_html(content_enc_text)
            if len(long_desc) > len(description):
                description = long_desc

        thumb = extract_image(item, desc_raw, content_enc_text)

        if not title or not link:
            continue

        try:
            dt = parsedate_to_datetime(pub_date)
            dt = dt.astimezone(timezone.utc)
        except Exception:
            dt = datetime.now(timezone.utc)

        items.append({
            'title':       title,
            'link':        link,
            'summary':     truncate(description),
            'date':        dt,
            'categories':  categories,
            'thumb':       thumb,
        })
    return items


def create_md(item, slug):
    date_iso    = item['date'].strftime('%Y-%m-%d')
    tag         = guess_tag(item['categories'])
    title_esc   = item['title'].replace('"', '\\"')
    summary_esc = item['summary'].replace('"', '\\"')
    thumb       = item.get('thumb', THUMB_DEFAULT)

    if thumb.startswith('http'):
        thumb_yaml = '"' + thumb + '"'
    else:
        thumb_yaml = thumb

    lines = [
        '---',
        'layout: noticia.njk',
        'title: "' + title_esc + '"',
        'date: ' + date_iso,
        'tag: ' + tag,
        'summary: "' + summary_esc + '"',
        'thumb: ' + thumb_yaml,
        'source_url: "' + item['link'] + '"',
        'permalink: /noticias/' + slug + '/index.html',
        '---',
        '',
        '> *Fonte: [Contabeis.com.br](' + item['link'] + ')*',
        '',
        item['summary'],
        '',
        '[**Leia o artigo completo no Contabeis ->**](' + item['link'] + ')',
        '',
    ]
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="Importar noticias do Contabeis RSS")
    parser.add_argument('--max',   type=int, default=20,    help='Maximo de artigos (padrao: 20)')
    parser.add_argument('--days',  type=int, default=60,    help='Ignorar artigos mais antigos que N dias (padrao: 60)')
    parser.add_argument('--reset', action='store_true',     help='Apaga todos os .md existentes antes de importar')
    args = parser.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)

    if args.reset:
        removed = 0
        for f in os.listdir(OUT_DIR):
            if f.endswith('.md'):
                os.remove(os.path.join(OUT_DIR, f))
                removed += 1
        print("--reset: " + str(removed) + " arquivo(s) removido(s) de " + OUT_DIR)

    print("Buscando RSS: " + RSS_URL)
    try:
        xml_bytes = fetch_rss()
    except Exception as e:
        print("ERRO ao buscar RSS: " + str(e), file=sys.stderr)
        sys.exit(1)

    print("RSS obtido (" + str(len(xml_bytes)) + " bytes). Processando itens...")
    items = parse_items(xml_bytes)
    print("Total de itens no RSS: " + str(len(items)))

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    items = [i for i in items if i['date'] >= cutoff]
    print("Itens dentro de " + str(args.days) + " dias: " + str(len(items)))

    slugs_ok = existing_slugs()
    created = 0
    skipped = 0

    for item in items:
        if created >= args.max:
            break
        slug = slugify(item['title'])
        if not slug:
            continue
        if slug in slugs_ok:
            skipped += 1
            continue
        path = os.path.join(OUT_DIR, slug + '.md')
        content = create_md(item, slug)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print("  [+] " + slug + ".md  (thumb: " + str(item['thumb'])[:60] + ")")
        slugs_ok.add(slug)
        created += 1

    print("\nConcluido: " + str(created) + " criado(s), " + str(skipped) + " ignorado(s) (ja existiam).")


if __name__ == '__main__':
    main()
