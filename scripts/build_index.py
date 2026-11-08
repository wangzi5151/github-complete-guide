#!/usr/bin/env python3
"""Generate the zero-dependency GitHub Pages landing page.

Usage:
    python3 scripts/build_index.py          # write index.html
    python3 scripts/build_index.py --check  # fail if index.html is stale

The generated page contains a searchable navigation list and a tiny built-in
Markdown renderer, so the deployed Pages site can display the local .md files
without any external JavaScript dependency.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
HEADING = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def title_of(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = HEADING.search(text)
    if match:
        title = re.sub(r"[`*_\[\]]", "", match.group(1)).strip()
        if title:
            return title
    return path.stem


def collect() -> list[dict[str, str]]:
    groups = [
        ("教程", "docs", "docs/*.md"),
        ("练习", "exercises", "exercises/*.md"),
        ("English Tutorials", "en/docs", "en/docs/*.md"),
        ("English Exercises", "en/exercises", "en/exercises/*.md"),
    ]
    items: list[dict[str, str]] = []
    for label, folder, pattern in groups:
        paths = sorted(ROOT.glob(pattern), key=lambda p: p.name.lower())
        for path in paths:
            items.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "title": title_of(path),
                    "group": label,
                    "folder": folder,
                }
            )
    for name in ("README.md", "BEGINNER.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md"):
        path = ROOT / name
        if path.exists():
            items.append(
                {
                    "path": name,
                    "title": title_of(path),
                    "group": "其他 / Other",
                    "folder": ".",
                }
            )
    return items


def content_file_count() -> int:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    files = [line for line in result.stdout.splitlines() if line]
    prefixes = (".github/workflows/ci.yml", "scripts/", "index.html")
    return len([f for f in files if not any(f == p or f.startswith(p) for p in prefixes)])


def stats() -> dict[str, int]:
    docs = sorted((ROOT / "docs").glob("*.md"))
    exercises = sorted((ROOT / "exercises").glob("*.md"))
    cjk = 0
    for path in docs:
        cjk += len(CJK.findall(path.read_text(encoding="utf-8")))
    return {
        "docs": len(docs),
        "exercises": len(exercises),
        "cjk": cjk,
        "files": content_file_count(),
    }


TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GitHub 完全指南</title>
<style>
  :root {
    --bg: #0d1117; --panel: #161b22; --border: #30363d;
    --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff;
    --code: #1f242c; --ok: #3fb950;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--text);
    font: 16px/1.7 -apple-system, BlinkMacSystemFont, "Segoe UI",
          "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
  }
  header {
    position: sticky; top: 0; z-index: 5; background: rgba(13,17,23,.96);
    border-bottom: 1px solid var(--border); padding: 14px 20px;
    display: flex; gap: 14px; align-items: center; flex-wrap: wrap;
  }
  header h1 { font-size: 18px; margin: 0; white-space: nowrap; }
  header .stats { color: var(--muted); font-size: 13px; }
  #search {
    flex: 1 1 280px; min-width: 200px; padding: 8px 12px; border-radius: 8px;
    border: 1px solid var(--border); background: var(--panel); color: var(--text);
  }
  #search:focus { outline: 2px solid var(--accent); outline-offset: 1px; }
  .layout { display: grid; grid-template-columns: 330px minmax(0, 1fr); min-height: calc(100vh - 64px); }
  nav { border-right: 1px solid var(--border); padding: 12px; overflow: auto; max-height: calc(100vh - 64px); }
  .group { color: var(--muted); font-size: 12px; font-weight: 700; text-transform: uppercase; margin: 16px 8px 6px; }
  .doc {
    display: block; width: 100%; text-align: left; border: 0; cursor: pointer;
    background: transparent; color: var(--text); padding: 7px 9px; border-radius: 7px;
    font: inherit; line-height: 1.35;
  }
  .doc small { display: block; color: var(--muted); font-size: 11px; font-family: monospace; }
  .doc:hover, .doc.active { background: #1f2937; color: #fff; }
  main { padding: 24px clamp(16px, 4vw, 56px) 80px; overflow: auto; }
  #welcome h2 { margin-top: 0; }
  #welcome .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 12px; margin-top: 18px; }
  #welcome .card { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 16px; }
  #welcome .card b { color: var(--accent); font-size: 24px; }
  #content a { color: var(--accent); }
  #content h1, #content h2, #content h3, #content h4 { line-height: 1.3; scroll-margin-top: 80px; }
  #content h1 { border-bottom: 1px solid var(--border); padding-bottom: 8px; }
  #content blockquote {
    border-left: 4px solid var(--accent); margin: 16px 0; padding: 4px 16px;
    color: var(--muted); background: var(--panel);
  }
  #content pre {
    background: var(--code); padding: 14px; border-radius: 8px; overflow: auto;
    border: 1px solid var(--border);
  }
  #content code { background: var(--code); padding: 2px 5px; border-radius: 4px; font-size: .92em; }
  #content pre code { padding: 0; background: none; }
  #content img { max-width: 100%; }
  #content table { border-collapse: collapse; width: 100%; margin: 14px 0; display: block; overflow: auto; }
  #content th, #content td { border: 1px solid var(--border); padding: 7px 11px; }
  #content th { background: var(--panel); }
  #content hr { border: 0; border-top: 1px solid var(--border); margin: 22px 0; }
  .toolbar { display: flex; gap: 12px; align-items: center; margin-bottom: 14px; color: var(--muted); font-size: 13px; }
  .toolbar a { color: var(--accent); }
  .loading { color: var(--muted); }
  @media (max-width: 820px) {
    .layout { grid-template-columns: 1fr; }
    nav { max-height: 38vh; border-right: 0; border-bottom: 1px solid var(--border); }
  }
</style>
</head>
<body>
<header>
  <h1>GitHub 完全指南</h1>
  <span class="stats" id="stats"></span>
  <input id="search" type="search" placeholder="搜索标题或路径… / Search title or path…" autocomplete="off">
</header>
<div class="layout">
  <nav id="nav"></nav>
  <main>
    <div id="welcome">
      <h2>从零开始学习 GitHub</h2>
      <p>按左侧目录浏览教程与练习，或使用上方搜索框。所有内容均来自本仓库 Markdown 文件，由内置渲染器直接展示。</p>
      <div class="grid">
        <div class="card"><b>__DOCS_COUNT__</b><br>篇中文教程</div>
        <div class="card"><b>__EXERCISES__</b><br>个实战练习</div>
        <div class="card"><b>__CJK__</b><br>汉字</div>
        <div class="card"><b>__FILES__</b><br>个内容文件</div>
      </div>
    </div>
    <div id="view" hidden>
      <div class="toolbar">
        <span id="path"></span>
        <a id="raw" href="#" target="_blank" rel="noopener">查看原始 Markdown</a>
      </div>
      <article id="content"></article>
    </div>
  </main>
</div>
<script>
const DOCS = __DOCS_JSON__;
const currentHash = () => decodeURIComponent(location.hash.slice(1));
let currentPath = "";

const $ = (sel) => document.querySelector(sel);
const escapeHtml = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;")
  .replace(/>/g, "&gt;").replace(/"/g, "&quot;");

function inline(s) {
  let out = escapeHtml(s);
  out = out.replace(/`([^`]+)`/g, (_, c) => "<code>" + c + "</code>");
  out = out.replace(/!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g,
    (_, alt, src) => '<img alt="' + alt + '" src="' + src + '" loading="lazy">');
  out = out.replace(/\[([^\]]+)\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g,
    (_, text, href) => '<a href="' + href + '">' + text + '</a>');
  out = out.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  out = out.replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<em>$2</em>");
  out = out.replace(/~~([^~]+)~~/g, "<del>$1</del>");
  return out;
}

function renderMarkdown(md) {
  const lines = md.replace(/\r/g, "").split("\n");
  const html = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    const fence = line.match(/^\s{0,3}(`{3,}|~{3,})(.*)$/);
    if (fence) {
      const ch = fence[1][0], len = fence[1].length, lang = fence[2].trim();
      const buf = [];
      i++;
      while (i < lines.length) {
        const m = lines[i].match(/^\s{0,3}(`{3,}|~{3,})\s*$/);
        if (m && m[1][0] === ch && m[1].length >= len) break;
        buf.push(lines[i]);
        i++;
      }
      i++;
      html.push('<pre><code' + (lang ? ' class="language-' + escapeHtml(lang) + '"' : '') +
        '>' + escapeHtml(buf.join("\n")) + "</code></pre>");
      continue;
    }
    if (/^\s*$/.test(line)) { i++; continue; }
    const heading = line.match(/^(#{1,6})\s+(.*)$/);
    if (heading) {
      const level = heading[1].length;
      html.push("<h" + level + ">" + inline(heading[2].replace(/\s+#+\s*$/, "")) + "</h" + level + ">");
      i++; continue;
    }
    if (/^\s{0,3}([-*_])(?:\s*\1){2,}\s*$/.test(line)) { html.push("<hr>"); i++; continue; }
    if (/^\s{0,3}>/.test(line)) {
      const buf = [];
      while (i < lines.length && /^\s{0,3}>/.test(lines[i])) {
        buf.push(lines[i].replace(/^\s{0,3}>\s?/, ""));
        i++;
      }
      html.push("<blockquote>" + renderMarkdown(buf.join("\n")) + "</blockquote>");
      continue;
    }
    if (/^\s*\|.*\|\s*$/.test(line) && i + 1 < lines.length &&
        /^\s*\|?[\s:|-]+\|[\s:|-]*$/.test(lines[i + 1])) {
      const head = line.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim());
      i += 2;
      const rows = [];
      while (i < lines.length && /^\s*\|.*\|\s*$/.test(lines[i])) {
        rows.push(lines[i].trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim()));
        i++;
      }
      html.push("<table><thead><tr>" + head.map((c) => "<th>" + inline(c) + "</th>").join("") +
        "</tr></thead><tbody>" + rows.map((r) => "<tr>" + r.map((c) => "<td>" + inline(c) + "</td>").join("") + "</tr>").join("") +
        "</tbody></table>");
      continue;
    }
    const ul = line.match(/^\s*[-*+]\s+(.*)$/);
    const ol = line.match(/^\s*\d+[.)]\s+(.*)$/);
    if (ul || ol) {
      const ordered = !!ol;
      const items = [];
      while (i < lines.length) {
        const m = ordered ? lines[i].match(/^\s*\d+[.)]\s+(.*)$/) : lines[i].match(/^\s*[-*+]\s+(.*)$/);
        if (!m) break;
        items.push("<li>" + inline(m[1]) + "</li>");
        i++;
      }
      html.push((ordered ? "<ol>" : "<ul>") + items.join("") + (ordered ? "</ol>" : "</ul>"));
      continue;
    }
    const buf = [line];
    i++;
    while (i < lines.length && !/^\s*$/.test(lines[i]) &&
           !/^(#{1,6})\s+/.test(lines[i]) && !/^\s{0,3}(`{3,}|~{3,})/.test(lines[i]) &&
           !/^\s*[-*+]\s+/.test(lines[i]) && !/^\s*\d+[.)]\s+/.test(lines[i]) &&
           !/^\s*\|.*\|\s*$/.test(lines[i]) && !/^\s{0,3}>/.test(lines[i])) {
      buf.push(lines[i]); i++;
    }
    html.push("<p>" + inline(buf.join(" ")) + "</p>");
  }
  return html.join("\n");
}

function buildNav() {
  const nav = $("#nav");
  const query = $("#search").value.trim().toLowerCase();
  nav.innerHTML = "";
  let lastGroup = "";
  DOCS.filter((d) => !query || d.title.toLowerCase().includes(query) ||
      d.path.toLowerCase().includes(query)).forEach((d) => {
    if (d.group !== lastGroup) {
      lastGroup = d.group;
      const h = document.createElement("div");
      h.className = "group";
      h.textContent = d.group;
      nav.appendChild(h);
    }
    const btn = document.createElement("button");
    btn.className = "doc" + (d.path === currentPath ? " active" : "");
    btn.innerHTML = escapeHtml(d.title) + "<small>" + escapeHtml(d.path) + "</small>";
    btn.addEventListener("click", () => { location.hash = encodeURIComponent(d.path); });
    nav.appendChild(btn);
  });
  if (!nav.children.length) nav.textContent = "没有匹配的文档 / No matches";
}

async function loadDoc(path) {
  if (!path) {
    $("#welcome").hidden = false;
    $("#view").hidden = true;
    currentPath = "";
    buildNav();
    return;
  }
  const doc = DOCS.find((d) => d.path === path);
  currentPath = path;
  buildNav();
  $("#welcome").hidden = true;
  $("#view").hidden = false;
  $("#path").textContent = path;
  $("#raw").href = path;
  $("#content").innerHTML = '<p class="loading">加载中… / Loading…</p>';
  try {
    const response = await fetch(path, { cache: "no-cache" });
    if (!response.ok) throw new Error("HTTP " + response.status);
    const markdown = await response.text();
    $("#content").innerHTML = renderMarkdown(markdown);
    document.title = (doc ? doc.title : path) + " · GitHub 完全指南";
    window.scrollTo({ top: 0, behavior: "instant" });
  } catch (err) {
    $("#content").innerHTML = '<p class="loading">无法加载该文件（' + escapeHtml(String(err)) +
      '）。请直接打开 <a href="' + path + '">原始 Markdown</a>。</p>';
  }
}

// Intercept relative .md links so navigation stays inside the viewer.
$("#content").addEventListener("click", (event) => {
  const link = event.target.closest("a");
  if (!link) return;
  const href = link.getAttribute("href");
  if (!href || href.startsWith("#") || /^[a-z]+:/i.test(href) || href.startsWith("//")) return;
  const target = new URL(href, location.origin + "/" + currentPath).pathname.replace(/^\/+/, "");
  if (target.endsWith(".md")) {
    event.preventDefault();
    location.hash = encodeURIComponent(target);
  }
});

$("#search").addEventListener("input", buildNav);
window.addEventListener("hashchange", () => loadDoc(currentHash()));

const counts = __STATS__;
$("#stats").textContent = counts.docs + " 篇教程 · " + counts.exercises + " 个练习 · " +
  counts.cjk.toLocaleString() + " 汉字";
buildNav();
loadDoc(currentHash());
</script>
</body>
</html>
"""


def render() -> str:
    data = collect()
    s = stats()
    html = TEMPLATE
    html = html.replace("__DOCS_JSON__", json.dumps(data, ensure_ascii=False, indent=2))
    html = html.replace("__STATS__", json.dumps(s, ensure_ascii=False))
    html = html.replace("__DOCS_COUNT__", str(s["docs"]))
    html = html.replace("__EXERCISES__", str(s["exercises"]))
    html = html.replace("__CJK__", f"{s['cjk']:,}")
    html = html.replace("__FILES__", str(s["files"]))
    return html


def main() -> int:
    out = ROOT / "index.html"
    generated = render()
    stale = not out.exists() or out.read_text(encoding="utf-8") != generated

    if "--check" in sys.argv:
        if stale:
            print("index.html is out of date. Run: python3 scripts/build_index.py")
            return 1
        print("index.html is up to date.")
        return 0

    out.write_text(generated, encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)} ({len(generated):,} bytes).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
