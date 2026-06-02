from stratcert.report import build_markdown_report


def test_report_contains_summary_tables_without_source_specific_terms():
    project = {
        "schema_version": "1.0",
        "project": {
            "name": "Toy classification",
            "field": "algebraically closed field",
            "objective": "classify simple quotients",
        },
        "strata": [
            {
                "id": "generic",
                "condition": "D(delta)",
                "status": "theorem",
                "quotient": {"dimension": 4, "kernel": "0"},
                "certificates": ["rank-generic"],
                "bridge": "rank certificate implies cyclic generation",
            },
            {
                "id": "boundary",
                "condition": "V(delta)",
                "status": "open",
                "quotient": {"dimension": None, "kernel": "unknown"},
                "certificates": [],
                "bridge": "missing quotient-kernel bridge",
            },
        ],
        "certificates": [
            {
                "id": "rank-generic",
                "kind": "rank",
                "claim": "orbit matrix has full rank",
                "support": "theorem",
                "artifact": "certificates/rank-generic.json",
            }
        ],
        "gaps": [
            {
                "id": "boundary-gap",
                "status": "open",
                "obligation": "compute quotient singular kernel",
                "next_action": "produce localized rank certificate",
            }
        ],
        "guardrails": [
            "finite-field enumeration is validation unless the theorem is finite-field"
        ],
    }

    report = build_markdown_report(project)

    assert "# Toy classification" in report
    assert "| generic | D(delta) | theorem | 4 | rank-generic |" in report
    assert "| boundary-gap | open | compute quotient singular kernel | produce localized rank certificate |" in report
    assert "private-alpha" not in report.lower()
    assert "private-beta" not in report.lower()
