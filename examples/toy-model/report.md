# Toy certificate classification

## Scope

- Field: algebraically closed field
- Objective: classify simple quotients in a finite toy model
- Strata: 2
- Certificates: 1
- Gaps: 1

## Status Summary

| status | count |
|---|---:|
| open | 1 |
| theorem | 1 |

## Strata

| id | condition | status | quotient dimension | certificates |
|---|---|---|---:|---|
| generic-open | D(delta) | theorem | 4 | generic-rank |
| closed-boundary | V(delta) | open |  |  |

## Certificates

| id | kind | support | claim | artifact |
|---|---|---|---|---|
| generic-rank | rank | theorem | toy orbit matrix has full rank on the generic open stratum | certificates/generic-rank.json |

## Gap Queue

| id | status | obligation | next action |
|---|---|---|---|
| boundary-kernel | open | compute quotient singular kernel on V(delta) | produce a localized rank or fullspan certificate |

## Guardrails

- finite-field enumeration is validation unless the theorem is finite-field
- each theorem row must name the stratum, certificate, and bridge implication
- artifact-map rows are not reader-independent quotient rows until quotient data is printed
