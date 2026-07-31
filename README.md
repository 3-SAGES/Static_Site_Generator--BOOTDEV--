<div align="center">

# 🐍 Static Site Generator

**A from-scratch static site generator that turns Markdown into a fully linked HTML website — no frameworks, just Python.**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Static Site](https://img.shields.io/badge/Output-Static%20HTML-orange?style=flat-square)
![Tests](https://img.shields.io/badge/Tests-Unit%20Tested-brightgreen?style=flat-square)
![GitHub Pages](https://img.shields.io/badge/Deployed-GitHub%20Pages-222222?style=flat-square&logo=github)

</div>

---

## Overview

This project builds the same kind of content pipeline that powers tools like **Hugo** and **Jekyll** — a directory of Markdown files goes in, a fully rendered static website comes out. It was built to dig into how those tools actually work under the hood, using nothing but the Python standard library.

It's a from-scratch exercise in:

- 🔁 Recursive file and directory traversal
- 🧩 Custom Markdown → HTML parsing
- 🌳 Object-oriented node/tree structures
- 🖼️ Template-based page rendering
- 📦 Static asset handling
- ✅ Unit testing

---

## ✨ Features

| | |
|---|---|
| 📝 **Markdown parsing** | Headings, paragraphs, lists, blockquotes, code blocks, bold/italic, links, images |
| 🌳 **HTML node tree** | Custom object model used to build and render markup |
| 📁 **Recursive content walk** | Handles arbitrarily nested content directories |
| 🎨 **Shared template** | One `template.html` applied consistently across every page |
| 📦 **Static asset copying** | Images and CSS carried over untouched |
| ✅ **Unit tested** | Core parsing and rendering logic covered by tests |
| 🌐 **Live deploy** | Builds straight to `docs/`, served by GitHub Pages |

---

## 🛠️ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

---

## 📂 Project Structure

```
.
├── content/       # Markdown source files
├── static/        # Assets copied as-is into the built site
├── src/           # Generator source code
├── unit_tests/    # Test suite
├── docs/          # Generated site output (served via GitHub Pages)
├── template.html  # Shared HTML template
├── build.sh       # Build the site
├── main.sh        # Build + serve locally
└── test.sh        # Run the test suite
```

---

## ⚙️ How It Works

1. **Parse** — Markdown files in `content/` are read and parsed into a tree of custom node objects.
2. **Render** — That tree is recursively converted into HTML.
3. **Template** — Each page is dropped into `template.html` to produce a complete HTML document.
4. **Copy** — Static assets are copied over unchanged.
5. **Deploy** — Output lands in `docs/`, which GitHub Pages serves directly.

---

## 🚀 Quick Start

```bash
# Build and serve locally
./main.sh

# Run the test suite
./test.sh
```

---

<div align="center">

Built as a deep dive into how static site generators work — one recursive function at a time.

</div>
