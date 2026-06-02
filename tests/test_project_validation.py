import json

import pytest

from stratcert.model import load_project, validate_project


def test_valid_project_loads_and_reports_no_errors(tmp_path):
    project_file = tmp_path / "classification.json"
    project_file.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "project": {
                    "name": "Toy classification",
                    "field": "algebraically closed field",
                    "objective": "classify simple quotients in a finite model",
                },
                "strata": [
                    {
                        "id": "generic",
                        "condition": "D(delta)",
                        "status": "theorem",
                        "quotient": {"dimension": 4, "kernel": "0"},
                        "certificates": ["rank-generic"],
                        "bridge": "full-rank orbit certificate proves cyclic generation",
                    }
                ],
                "certificates": [
                    {
                        "id": "rank-generic",
                        "kind": "rank",
                        "claim": "orbit matrix has full rank on D(delta)",
                        "support": "theorem",
                        "artifact": "certificates/rank-generic.json",
                    }
                ],
                "gaps": [],
                "guardrails": [
                    "finite-field enumeration is validation unless the theorem is finite-field"
                ],
            }
        ),
        encoding="utf-8",
    )

    project = load_project(project_file)

    assert validate_project(project) == []


def test_validation_rejects_unknown_certificate_reference():
    project = {
        "schema_version": "1.0",
        "project": {
            "name": "Toy classification",
            "field": "k",
            "objective": "classify quotients",
        },
        "strata": [
            {
                "id": "closed-point",
                "condition": "V(t)",
                "status": "theorem",
                "quotient": {"dimension": 1, "kernel": "maximal-kernel"},
                "certificates": ["missing-cert"],
                "bridge": "certificate proves quotient simplicity",
            }
        ],
        "certificates": [],
        "gaps": [],
        "guardrails": [],
    }

    errors = validate_project(project)

    assert "strata[closed-point] references missing certificate 'missing-cert'" in errors


@pytest.mark.parametrize("forbidden", ["private-alpha", "private-beta", "internal-dictionary"])
def test_validation_rejects_forbidden_source_specific_terms(forbidden):
    project = {
        "schema_version": "1.0",
        "project": {
            "name": "Leak check",
            "field": "k",
            "objective": f"do not leak {forbidden}",
        },
        "privacy": {"blocked_terms": ["private-alpha", "private-beta", "internal-dictionary"]},
        "strata": [],
        "certificates": [],
        "gaps": [],
        "guardrails": [],
    }

    errors = validate_project(project)

    assert any("forbidden source-specific term" in error for error in errors)
