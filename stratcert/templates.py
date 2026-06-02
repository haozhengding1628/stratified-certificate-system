"""Generic starter data for new classification projects."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict


TOY_PROJECT: Dict[str, Any] = {
    "schema_version": "1.0",
    "project": {
        "name": "Toy certificate classification",
        "field": "algebraically closed field",
        "objective": "classify simple quotients in a finite toy model",
    },
    "privacy": {
        "blocked_terms": [
            "private-project-name",
            "private-dataset-token",
        ]
    },
    "strata": [
        {
            "id": "generic-open",
            "condition": "D(delta)",
            "status": "theorem",
            "quotient": {"dimension": 4, "kernel": "0"},
            "certificates": ["generic-rank"],
            "bridge": "rank certificate implies every singular direction spans the quotient",
        },
        {
            "id": "closed-boundary",
            "condition": "V(delta)",
            "status": "open",
            "quotient": {"dimension": None, "kernel": "unknown"},
            "certificates": [],
            "bridge": "missing quotient-kernel or fullspan certificate",
        },
    ],
    "certificates": [
        {
            "id": "generic-rank",
            "kind": "rank",
            "claim": "toy orbit matrix has full rank on the generic open stratum",
            "support": "theorem",
            "artifact": "certificates/generic-rank.json",
        }
    ],
    "gaps": [
        {
            "id": "boundary-kernel",
            "status": "open",
            "obligation": "compute quotient singular kernel on V(delta)",
            "next_action": "produce a localized rank or fullspan certificate",
        }
    ],
    "guardrails": [
        "finite-field enumeration is validation unless the theorem is finite-field",
        "each theorem row must name the stratum, certificate, and bridge implication",
        "artifact-map rows are not reader-independent quotient rows until quotient data is printed",
    ],
}


def new_toy_project() -> Dict[str, Any]:
    return deepcopy(TOY_PROJECT)
