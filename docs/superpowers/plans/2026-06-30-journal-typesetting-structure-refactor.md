# journal-typesetting 结构重构实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 `journal-typesetting` 从“长 SKILL.md + 分散经验规则”重构成“短调度层 + 专项 references + 可执行审计脚本”。

**Architecture:** `SKILL.md` 作为工作流调度层；深规则沉淀到 `references/`；重复、可验证、易出错的 DOI/page 和输出治理交给 `scripts/`。现有文章目录只作为只读验证样本，不修改成品 HTML/PDF。

**Tech Stack:** Markdown skill docs, Python 3 standard library `unittest`/`argparse`, existing Node Playwright layout validator.

---

## Tasks

### Task 1: Preflight snapshot

**Files:**
- Create: `docs/superpowers/plans/2026-06-30-journal-typesetting-structure-refactor.md`

- [ ] Run `git status --short` and `git diff --stat`.
- [ ] Confirm no destructive action is needed.
- [ ] Save this plan document.

### Task 2: Add script tests first

**Files:**
- Create: `tests/test_sequence_manager.py`
- Create: `tests/test_audit_visible_outputs.py`
- Create: `tests/test_audit_doi_pages.py`

- [ ] Write tests for sequence allocation, activation, page updates, output visibility, and DOI/page checks.
- [ ] Run `python3 -m unittest discover -s tests -p 'test_*.py'` and confirm missing scripts fail before implementation.

### Task 3: Implement sequence manager

**Files:**
- Create: `scripts/sequence_manager.py`

- [ ] Implement pure functions and CLI commands: `validate`, `next`, `assign`, `activate`, `update-pages`.
- [ ] Use atomic JSON writes for mutating commands.
- [ ] Run `python3 -m unittest tests.test_sequence_manager -v`.

### Task 4: Implement visible output audit

**Files:**
- Create: `scripts/audit_visible_outputs.py`

- [ ] Audit `mbamNN-*` folders.
- [ ] Allow only `two-column-{short}.html`, `single-column-{short}.html`, and optionally `10.65079/mbamNN.pdf`.
- [ ] Ignore hidden directories and known root housekeeping.
- [ ] Run `python3 -m unittest tests.test_audit_visible_outputs -v`.

### Task 5: Implement DOI/page audit

**Files:**
- Create: `scripts/audit_doi_pages.py`

- [ ] Validate DOI strings in HTML.
- [ ] Reject malformed DOI variants.
- [ ] Check two-column HTML footer page range where possible.
- [ ] Add optional PDF checks with warning fallback.
- [ ] Run `python3 -m unittest tests.test_audit_doi_pages -v`.

### Task 6: Refactor references

**Files:**
- Create: `references/sequence-and-output.md`
- Create: `references/layout-gates.md`
- Create: `references/output-hygiene.md`
- Modify: `references/typesetting-rules.md`
- Modify: `references/pagination-rules.md`
- Modify: `references/validation-checklist.md`

- [ ] Move repeated DOI/page, layout gate, and output hygiene rules out of `SKILL.md`.
- [ ] Keep detailed historical rules in references.
- [ ] Add cross-links so future agents know which file is authoritative.

### Task 7: Rewrite `SKILL.md` as orchestrator

**Files:**
- Modify: `SKILL.md`

- [ ] Keep frontmatter, overview, trigger context, and high-priority invariants.
- [ ] Add required reads by step.
- [ ] Add required scripts by checkpoint.
- [ ] Keep 7-step workflow concise and route to references/scripts.

### Task 8: Validate against current real workspace

- [ ] Run `python3 -m unittest discover -s tests -p 'test_*.py'`.
- [ ] Run sequence validation against `/Users/jikunren/Documents/期刊排版/.sequence/medba-issue-sequence.json`.
- [ ] Run visible output audit against `/Users/jikunren/Documents/期刊排版` with `--allow-pdf`.
- [ ] Run DOI/page audit against the same workspace with `--check-pdf`.

### Task 9: Final review, commit, push

- [ ] Review `git diff --stat` and relevant diff.
- [ ] Append concise logs to `/Users/jikunren/Documents/期刊排版/.logs/progress.md` and `changes.md`.
- [ ] Stage specific files only.
- [ ] Commit `refactor(skill): split journal typesetting workflow and add audits`.
- [ ] Push `origin main` and verify no unpushed commits remain.
