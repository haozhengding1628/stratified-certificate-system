# Stratified Certificate System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reusable, source-agnostic system for certificate-driven stratified classification workflows.

**Architecture:** The package provides a small Python CLI and library around a JSON project file. It validates strata, certificates, gap ledgers, guardrails, and privacy constraints, then compiles a markdown report from the clean generic records.

**Tech Stack:** Python 3.9+, standard library only for runtime, pytest for tests, GitHub-ready packaging through `pyproject.toml`.

---

### Task 1: Core Validation

**Files:**
- Create: `stratcert/model.py`
- Test: `tests/test_project_validation.py`

- [x] **Step 1: Write failing validation tests**

Tests cover successful project loading, missing certificate references, and source-specific forbidden terms.

- [x] **Step 2: Implement minimal validation**

Add `load_project(path)` and `validate_project(project)` using only the Python standard library.

- [x] **Step 3: Verify**

Run: `pytest tests/test_project_validation.py -q`
Expected: all tests pass.

### Task 2: Markdown Reporting

**Files:**
- Create: `stratcert/report.py`
- Test: `tests/test_report.py`

- [x] **Step 1: Write failing report test**

Test verifies summary tables and confirms no source-specific terms are emitted.

- [x] **Step 2: Implement report builder**

Add `build_markdown_report(project)` with project summary, strata table, certificate table, gap table, and guardrails.

- [x] **Step 3: Verify**

Run: `pytest tests/test_report.py -q`
Expected: all tests pass.

### Task 3: CLI and Example Project

**Files:**
- Create: `stratcert/cli.py`
- Create: `stratcert/templates.py`
- Create: `stratcert/__init__.py`
- Test: `tests/test_cli.py`

- [x] **Step 1: Write failing CLI test**

Test verifies `init`, `validate`, and `report` commands on a temporary project.

- [x] **Step 2: Implement CLI**

Add `init`, `validate`, and `report` commands. `init` writes generic toy data only.

- [x] **Step 3: Verify**

Run: `pytest tests/test_cli.py -q`
Expected: all tests pass.

### Task 4: Repository Packaging and Documentation

**Files:**
- Create: `pyproject.toml`
- Create: `README.md`
- Create: `.gitignore`
- Create: `examples/toy-model/classification.json`
- Create: `examples/toy-model/report.md`

- [x] **Step 1: Add package metadata**

Expose `stratcert = stratcert.cli:main` as the console script.

- [x] **Step 2: Add documentation**

Explain installation, CLI usage, schema, privacy boundary, and GitHub publishing.

- [x] **Step 3: Verify full project**

Run: `pytest -q`
Expected: all tests pass.
