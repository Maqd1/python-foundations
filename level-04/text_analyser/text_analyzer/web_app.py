"""Optional web report. Requires Flask: pip install flask."""

from __future__ import annotations

from pathlib import Path

from .analyzer import TextAnalyzer

try:
    from flask import Flask, request, render_template_string
    _HAS_FLASK = True
except Exception:
    _HAS_FLASK = False


_HTML = """<!doctype html>
<html><head><meta charset="utf-8"><title>Text Analyzer Report</title>
<style>
 body{font-family:system-ui,sans-serif;max-width:820px;margin:2rem auto;padding:0 1rem;color:#222}
 h1{margin-bottom:.2rem} .meta{color:#666;margin-bottom:1.5rem}
 .card{border:1px solid #eee;border-radius:10px;padding:1rem;margin:1rem 0;background:#fafafa}
 .bar{height:10px;background:#4C72B0;border-radius:4px;margin:2px 0}
 code{background:#eee;padding:2px 6px;border-radius:4px}
 .label{font-weight:600;margin-right:.5rem}
</style></head><body>
<h1>📊 Text Analyzer Report</h1>
<p class="meta">{{ words }} words · {{ sentences }} sentences · {{ paragraphs }} paragraphs</p>

<div class="card"><h2>📈 Statistics</h2>
 <p><span class="label">Characters:</span>{{ chars_with }} ({{ chars_without }} without spaces)</p>
 <p><span class="label">Avg word length:</span>{{ avg_word_len }}</p>
 <p><span class="label">Avg sentence length:</span>{{ avg_sent_len }}</p>
 <p><span class="label">Lexical diversity:</span>{{ lexdiv }}</p>
</div>

<div class="card"><h2>📝 Most Common Words</h2>
 {% for w,c in common %}
   <div><code>{{ w }}</code> × {{ c }}<div class="bar" style="width:{{ (c / max