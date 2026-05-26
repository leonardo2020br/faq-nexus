#!/usr/bin/env python3
"""
import-noticias.py
==================
Importa notícias do RSS do Contabeis (https://www.contabeis.com.br/rss/noticias/)
e cria arquivos Markdown em _content/noticias/ para o site FAQ NEXUS (Eleventy).

Como usar:
  python scripts/import-noticias.py [--max 20] [--days 60]

Flags:
  --max   Número máximo de artigos a importar (padrão: 20)
  --days  Ignorar artigos mais antigos que N dias (padrão: 60)
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

# ── Configurações ──────────────────────────────────────────────────────────────
RSS_URL   = "https://www.contabeis.com.br/rss/noticias/"
OUT_DIR   = "_content/noticias"
THUMB_DEFAULT = "📰"

# Mapeamento de categorias RSS → tags do site
CATEGORY_MAP = {
    "legislação":  "aviso",
    "legislacao":  "aviso",
    "fiscal":      "aviso",
    "tributário":  "aviso",
    "tributario":  "aviso",
    "tutorial":    "tutorial",
    "artigo":      "tutorial",
    "evento":      "evento",
    "release":     "release",
    "atualização": "release",
    "atualizacao": "release",
}


# ── Utilitários ────────────────────────────────────────────────────────────────
def slugify(text):
    """Converte um título em slug kebab-case sem acentos."""
    replacements = {
        'á':'a','à':'a','ã':'a','â':'a','ä':'a',
        'é':'e','è':'e','ê':'e','ë':'e',
        'í':'i','ì':'i','î':'i','ï':'i',
        'ó':'o','ò':'o','õ':'o','ô':'o','ö':'o',
        'ú':'u','ù':'u','û':'u','ü':'u',
        'ç':'c','ñ':'n',
        'Á':'a','À':'a','Ã':'a','Â':'a','Ä':'a',
        'É':'e','È':'e','Ê':'e','Ë':'e',
        'Í':'i','Ì':'i','Î':'i','Ï':'i',
        'Ó':'o','Ò':'o','Õ':'o','Ô':'o','Ö':'o',
        'Ú':'u','Ù':'u','Û':'u','Ü':'u',
        'Ç':'c','Ñ':'n',
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text[:80]  # limita tamanho do slug


def strip_html(raw):
    """Remove tags HTML e decodifica entidades."""
    text = re.sub(r'<[^>]+>', '', raw or '')
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def guess_tag(categories):
    """Infere a tag do site a partir das categorias do RSS."""
    for cat in categories:
        key = cat.lower().strip()
        if key in CATEGORY_MAP:
            return CATEGORY_MAP[key]
        for k, v in CATEGORY_MAP.items():
            if k in key:
                return v
    return "aviso"  # padrão para notícias fiscais/contábeis


def truncate(text, max_chars=220):
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(' ', 1)[0] + '…'


def existing_slugs():
    """Retorna o conjunto de slugs já presentes em _content/noticias/."""
    slugs = set()
    if not os.path.isdir(OUT_DIR):
        return slugs
    for f in os.listdir(OUT_DIR):
        if f.endswith('.md'):
            slugs.add(f[:-3])  # remove .md
    return slugs


def fetch_rss():
    req = urllib.request.Request(
        RSS_URL,
        headers={'User-Agent': 'FAQ-NEXUS-Bot/1.0 (+https://faq-nexus.leossapo-2014.workers.dev)'}
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()


def parse_items(xml_bytes):
    root = ET.fromstring(xml_bytes)
    ns = {'content': 'http://purl.org/rss/1.0/modules/content/'}
    items = []
    for item in root.iter('item'):
        title       = (item.findtext('title') or '').strip()
        link        = (item.findtext('link') or '').strip()
        description = strip_html(item.findtext('description') or '')
        pub_date    = item.findtext('pubDate') or ''
        categories  = [c.text.strip() for c in item.findall('category') if c.text]
        # content:encoded como fallback de descrição mais longa
        content_enc = item.find('content:encoded', ns)
        if content_enc is not None and content_enc.text:
            long_desc = strip_html(content_enc.text)
            if len(long_desc) > len(description):
                description = long_desc

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
        })
    return items


def create_md(item, slug):
    """Gera o conteúdo do arquivo Markdown para uma notícia."""
    date_iso  = item['date'].strftime('%Y-%m-%d')
    date_ptbr = item['date'].strftime('%d/%m/%Y')
    tag       = guess_tag(item['categories'])
    title_esc = item['title'].replace('"', '\\"')
    summary_esc = item['summary'].replace('"', '\\"')

    body = f"""---
layout: noticia.njk
title: "{title_esc}"
date: {date_iso}
tag: {tag}
summary: "{summary_esc}"
thumb: {THUMB_DEFAULT}
source_url: "{item['link']}"
permalink: /noticias/{slug}/index.html
---

> *Fonte: [Contabeis.com.br]({item['link']})*

{item['summary']}

[**Leia o artigo completo no Contabeis →**]({item['link']})
"""
    return body


def main():
    parser = argparse.ArgumentParser(description="Importar notícias do Contabeis RSS")
    parser.add_argument('--max',  type=int, default=20, help='Máximo de artigos (padrão: 20)')
    parser.add_argument('--days', type=int, default=60, help='Ignorar artigos mais antigos que N dias (padrão: 60)')
    args = parser.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    known = existing_slugs()
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)

    print(f"[import-noticias] Buscando RSS: {RSS_URL}")
    try:
        xml_bytes = fetch_rss()
    except Exception as e:
        print(f"[ERRO] Falha ao buscar RSS: {e}")
        sys.exit(1)

    items = parse_items(xml_bytes)
    print(f"[import-noticias] {len(items)} itens no feed")

    created = 0
    skipped = 0

    for item in items:
        if created >= args.max:
            break

        if item['date'] < cutoff:
            skipped += 1
            continue

        slug = slugify(item['title'])
        if not slug:
            continue

        # Evita duplicatas por slug
        if slug in known:
            skipped += 1
            continue

        # Garante slug único se houver colisão
        base_slug = slug
        counter = 2
        while slug in known:
            slug = f"{base_slug}-{counter}"
            counter += 1

        md_path = os.path.join(OUT_DIR, f"{slug}.md")
        content = create_md(item, slug)

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)

        known.add(slug)
        created += 1
        date_str = item['date'].strftime('%Y-%m-%d')
        print(f"  ✅ [{date_str}] {slug}.md")

    print(f"\n[import-noticias] Resultado: {created} criados, {skipped} ignorados.")


if __name__ == '__main__':
    main()
