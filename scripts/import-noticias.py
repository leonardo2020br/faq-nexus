#!/usr/bin/env python3
"""
import-noticias.py
==================
Importa notícias do RSS do Contabeis (https://www.contabeis.com.br/rss/noticias/)
e cria arquivos Markdown em _content/noticias/ para o site FAQ NEXUS (Eleventy).

Como usar:
  python scripts/import-noticias.py [--max 20] [--days 60] [--reset]

Flags:
  --max    Número máximo de artigos a importar (padrão: 20)
  --days   Ignorar artigos mais antigos que N dias (padrão: 60)
  --reset  Apaga TODOS os arquivos existentes em _content/noticias/ antes de importar
           (útil para reimportar com imagens após correção do script)
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


def extract_image(item, desc_raw):
    """Extrai a URL da imagem do item RSS.

    Tenta, em ordem:
      1. Tag <media:content url="..."> (namespace Yahoo Media RSS)
      2. Primeiro <img src="..."> dentro do HTML da <description>
      3. Fallback: emoji padrão
    """
    # 1. media:content (formato que o Contabeis usa)
    MEDIA_NS = 'http://search.yahoo.com/mrss/'
    media_el = item.find(f'{{{MEDIA_NS}}}content')
    if media_el is not None:
        url = media_el.get('url', '').strip()
        if url.startswith('http'):
            return url

    # 2. <img src="..."> no HTML da description
    img_match = re.search(r'<img\s[^>]*src=["\']([^"\']+)["\']', desc_raw or '', re.IGNORECASE)
    if img_match:
        url = img_match.group(1).strip()
        if url.startswith('http'):
            return url

    # 3. Fallback emoji
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

        # content:encoded como fallback de descrição mais longa
        content_enc = item.find('content:encoded', ns)
        if content_enc is not None and content_enc.text:
            long_desc = strip_html(content_enc.text)
            if len(long_desc) > len(description):
                description = long_desc

        # Extrai imagem
        thumb = extract_image(item, desc_raw)

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
    """Gera o conteúdo do arquivo Markdown para uma notícia."""
    date_iso    = item['date'].strftime('%Y-%m-%d')
    tag         = guess_tag(item['categories'])
    title_esc   = item['title'].replace('"', '\\"')
    summary_esc = item['summary'].replace('"', '\\"')
    thumb       = item.get('thumb', THUMB_DEFAULT)

    # thumb: URL → string entre aspas; emoji → sem aspas
    if thumb.startswith('http'):
        thumb_yaml = f'"{thumb}"'
    else:
        thumb_yaml = thumb

    body = f"""---
layout: noticia.njk
title: "{title_esc}"
date: {date_iso}
tag: {tag}
summary: "{summary_esc}"
thumb: {thumb_yaml}
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
    parser.add_argument('--max',   type=int, default=20,    help='Máximo de artigos (padrão: 20)')
    parser.add_argument('--days',  type=int, default=60,    help='Ignorar artigos mais antigos que N dias (padrão: 60)')
    parser.add_argument('--reset', action='store_true',     help='Apaga todos os .md existentes antes de importar')
    args = parser