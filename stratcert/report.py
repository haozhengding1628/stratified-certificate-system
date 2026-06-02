"""Markdown report generation for classification projects."""

from __future__ import annotations

from collections import Counter
from typing import Any, Mapping


def build_markdown_report(project: Mapping[str, Any]) -> str:
    meta = project["project"]
    strata = project.get("strata", [])
    certificates = project.get("certificates", [])
    gaps = project.get("gaps", [])
    guardrails = project.get("guardrails", [])

    lines = [
        f"# {_text(meta['name'])}",
        "",
        "## Scope",
        "",
        f"- Field: {_text(meta['field'])}",
        f"- Objective: {_text(meta['objective'])}",
        f"- Strata: {len(strata)}",
        f"- Certificates: {len(certificates)}",
        f"- Gaps: {len(gaps)}",
        "",
    ]

    lines.extend(_status_summary(strata))
    lines.extend(_strata_table(strata))
    lines.extend(_certificate_table(certificates))
    lines.extend(_gap_table(gaps))
    lines.extend(_guardrails(guardrails))

    return "\n".join(lines).rstrip() + "\n"


def _status_summary(strata: list[Mapping[str, Any]]) -> list[str]:
    counts = Counter(stratum.get("status", "unknown") for stratum in strata)
    lines = ["## Status Summary", "", "| status | count |", "|---|---:|"]
    if counts:
        for status, count in sorted(counts.items()):
            lines.append(f"| {_cell(status)} | {count} |")
    else:
        lines.append("| none | 0 |")
    lines.append("")
    return lines


def _strata_table(strata: list[Mapping[str, Any]]) -> list[str]:
    lines = [
        "## Strata",
        "",
        "| id | condition | status | quotient dimension | certificates |",
        "|---|---|---|---:|---|",
    ]
    if not strata:
        lines.append("| none |  |  |  |  |")
    for stratum in strata:
        quotient = stratum.get("quotient", {})
        dimension = quotient.get("dimension", "")
        certificate_refs = ", ".join(stratum.get("certificates", []))
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(stratum.get("id", "")),
                    _cell(stratum.get("condition", "")),
                    _cell(stratum.get("status", "")),
                    _cell(dimension),
                    _cell(certificate_refs),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _certificate_table(certificates: list[Mapping[str, Any]]) -> list[str]:
    lines = [
        "## Certificates",
        "",
        "| id | kind | support | claim | artifact |",
        "|---|---|---|---|---|",
    ]
    if not certificates:
        lines.append("| none |  |  |  |  |")
    for certificate in certificates:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(certificate.get("id", "")),
                    _cell(certificate.get("kind", "")),
                    _cell(certificate.get("support", "")),
                    _cell(certificate.get("claim", "")),
                    _cell(certificate.get("artifact", "")),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _gap_table(gaps: list[Mapping[str, Any]]) -> list[str]:
    lines = ["## Gap Queue", "", "| id | status | obligation | next action |", "|---|---|---|---|"]
    if not gaps:
        lines.append("| none | closed | no active gaps | no action |")
    for gap in gaps:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(gap.get("id", "")),
                    _cell(gap.get("status", "")),
                    _cell(gap.get("obligation", "")),
                    _cell(gap.get("next_action", "")),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _guardrails(guardrails: list[Any]) -> list[str]:
    lines = ["## Guardrails", ""]
    if not guardrails:
        lines.append("- No guardrails recorded.")
    for guardrail in guardrails:
        lines.append(f"- {_text(guardrail)}")
    lines.append("")
    return lines


def _cell(value: Any) -> str:
    text = _text(value)
    return text.replace("|", "\\|")


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("\r\n", " ").replace("\n", " ").strip()
