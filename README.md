# Stratified Certificate System

A small, source-agnostic toolkit for running certificate-driven classification
projects.

The system is designed for projects where a parameter space is split into
locally closed strata, each theorem row is backed by named computational or
structural certificates, and the final write-up needs a clear boundary between
the mathematical claim, the machine evidence, validation checks, and remaining
paper-work gaps.

This repository intentionally contains only generic tooling and toy examples.
It does not include private research data, paper-specific certificates, round
logs, parameter tables, or unpublished classification artifacts.

## What It Provides

- A JSON project format for:
  - project scope and field;
  - strata;
  - quotient rows;
  - certificate records;
  - gap ledgers;
  - guardrails;
  - privacy blocked terms.
- A validator that checks:
  - required fields;
  - duplicate IDs;
  - missing certificate references;
  - status vocabulary;
  - configured privacy blocked terms.
- A report compiler that turns the JSON ledger into a markdown status report.
- A CLI that can initialize, validate, and report on a generic project.

## Install

From a checkout:

```bash
python -m pip install -e .
```

Runtime uses only the Python standard library. Tests use `pytest`.

## Mathematical Software Boundary

This toolkit does not require a computer algebra system to run. It records and
checks the evidence ledger around a classification project; the mathematical
computations themselves may be produced elsewhere.

When a row depends on external computation, record the software as metadata in
the certificate. Typical sources include SageMath, Magma, GAP, Singular,
Macaulay2, PARI/GP, Mathematica, or project-specific scripts. The public ledger
should capture enough information for review:

- software name and exact version;
- the certificate type, such as rank, kernel, saturation, normal form,
  Groebner basis, finite-field check, or independent validation;
- a short input/output summary;
- the artifact path or public reproduction note;
- the bridge from the computation to the mathematical claim.

Do not publish private datasets, unpublished tables, raw logs, or
paper-specific computation files in this repository. If a certificate depends on
private or paper-specific material, keep that material outside the public repo
and reference only a sanitized summary.

## Quick Start

Create a starter project:

```bash
stratcert init my-classification
```

Validate it:

```bash
stratcert validate my-classification
```

Compile a report:

```bash
stratcert report my-classification --out my-classification/reports/status.md
```

You can also run without installing:

```bash
python -m stratcert.cli init my-classification
python -m stratcert.cli validate my-classification
python -m stratcert.cli report my-classification --out my-classification/reports/status.md
```

## Project File

Each project is stored in `classification.json`.

Minimal shape:

```json
{
  "schema_version": "1.0",
  "project": {
    "name": "Toy certificate classification",
    "field": "algebraically closed field",
    "objective": "classify simple quotients in a finite toy model"
  },
  "privacy": {
    "blocked_terms": ["private-project-name", "private-dataset-token"]
  },
  "strata": [],
  "certificates": [],
  "gaps": [],
  "guardrails": []
}
```

The `privacy.blocked_terms` list is project-specific. Use it to prevent private
terms, source names, data labels, or unpublished identifiers from entering a
public ledger or report.

## Row Template

A theorem row should carry enough information to audit the claim without
guessing:

```json
{
  "id": "generic-open",
  "condition": "D(delta)",
  "status": "theorem",
  "quotient": {
    "dimension": 4,
    "kernel": "0"
  },
  "certificates": ["generic-rank"],
  "bridge": "rank certificate implies every singular direction spans the quotient"
}
```

The `bridge` field is the important part: it states how the named certificate
implies the mathematical conclusion. A rank, kernel, saturation, or fullspan
calculation should not be treated as self-explanatory.

## Certificate Template

```json
{
  "id": "generic-rank",
  "kind": "rank",
  "claim": "toy orbit matrix has full rank on the generic open stratum",
  "support": "theorem",
  "artifact": "certificates/generic-rank.json",
  "software": {
    "name": "SageMath",
    "version": "record-exact-version",
    "role": "rank computation"
  }
}
```

Use `support` to distinguish theorem evidence from guardrails, validation, and
paper-support material. The `software` object is optional metadata; use it when
the certificate was produced or checked with a named mathematical software
system.

## Development

Run tests:

```bash
python -m pytest -q
```

The tests intentionally use only toy ledgers and generic blocked terms.

## Publication Boundary

This tool helps organize evidence. It does not turn a computation into a theorem
by itself. A publication row should still identify:

- the exact stratum;
- the base ring or localization;
- the module, quotient, or matrix being certified;
- the certificate type;
- the bridge from certificate to the mathematical conclusion;
- any remaining exceptional locus or paper-level presentation gap.
