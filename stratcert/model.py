"""Project loading and validation for certificate-driven classifications."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple


Project = Dict[str, Any]

PROJECT_FILE = "classification.json"

REQUIRED_PROJECT_FIELDS = ("name", "field", "objective")
REQUIRED_STRATUM_FIELDS = ("id", "condition", "status", "quotient", "certificates", "bridge")
REQUIRED_CERTIFICATE_FIELDS = ("id", "kind", "claim", "support", "artifact")
REQUIRED_GAP_FIELDS = ("id", "status", "obligation", "next_action")

ALLOWED_STATUSES = {
    "theorem",
    "proposition",
    "support",
    "guardrail",
    "validation",
    "open",
    "closed",
}


def resolve_project_file(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_dir():
        candidate = candidate / PROJECT_FILE
    return candidate


def load_project(path: str | Path) -> Project:
    project_file = resolve_project_file(path)
    with project_file.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{project_file} must contain a JSON object")
    return data


def validate_project(project: Mapping[str, Any]) -> List[str]:
    errors: List[str] = []

    if not isinstance(project, Mapping):
        return ["project must be a JSON object"]

    if project.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'")

    project_meta = project.get("project")
    if not isinstance(project_meta, Mapping):
        errors.append("project metadata must be an object")
    else:
        for field in REQUIRED_PROJECT_FIELDS:
            _require_nonempty_string(project_meta, field, f"project.{field}", errors)

    strata = _require_list(project, "strata", errors)
    certificates = _require_list(project, "certificates", errors)
    gaps = _require_list(project, "gaps", errors)
    _require_list(project, "guardrails", errors)

    certificate_ids = _validate_certificates(certificates, errors)
    _validate_strata(strata, certificate_ids, errors)
    _validate_gaps(gaps, errors)
    _validate_privacy(project, errors)

    return errors


def _require_list(project: Mapping[str, Any], field: str, errors: List[str]) -> List[Any]:
    value = project.get(field)
    if value is None:
        errors.append(f"{field} must be present")
        return []
    if not isinstance(value, list):
        errors.append(f"{field} must be a list")
        return []
    return value


def _require_nonempty_string(
    item: Mapping[str, Any], field: str, label: str, errors: List[str]
) -> None:
    value = item.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be a non-empty string")


def _validate_certificates(certificates: Sequence[Any], errors: List[str]) -> set[str]:
    certificate_ids: set[str] = set()
    for index, certificate in enumerate(certificates):
        label = _item_label(certificate, index, "certificate")
        if not isinstance(certificate, Mapping):
            errors.append(f"certificates[{index}] must be an object")
            continue
        for field in REQUIRED_CERTIFICATE_FIELDS:
            _require_nonempty_string(certificate, field, f"certificates[{label}].{field}", errors)
        cert_id = certificate.get("id")
        if isinstance(cert_id, str):
            if cert_id in certificate_ids:
                errors.append(f"duplicate certificate id '{cert_id}'")
            certificate_ids.add(cert_id)
        support = certificate.get("support")
        if isinstance(support, str) and support not in ALLOWED_STATUSES:
            errors.append(f"certificates[{label}].support has unknown status '{support}'")
    return certificate_ids


def _validate_strata(strata: Sequence[Any], certificate_ids: set[str], errors: List[str]) -> None:
    stratum_ids: set[str] = set()
    for index, stratum in enumerate(strata):
        label = _item_label(stratum, index, "stratum")
        if not isinstance(stratum, Mapping):
            errors.append(f"strata[{index}] must be an object")
            continue
        for field in REQUIRED_STRATUM_FIELDS:
            if field == "quotient":
                continue
            if field == "certificates":
                continue
            _require_nonempty_string(stratum, field, f"strata[{label}].{field}", errors)
        stratum_id = stratum.get("id")
        if isinstance(stratum_id, str):
            if stratum_id in stratum_ids:
                errors.append(f"duplicate stratum id '{stratum_id}'")
            stratum_ids.add(stratum_id)
        status = stratum.get("status")
        if isinstance(status, str) and status not in ALLOWED_STATUSES:
            errors.append(f"strata[{label}].status has unknown status '{status}'")
        quotient = stratum.get("quotient")
        if not isinstance(quotient, Mapping):
            errors.append(f"strata[{label}].quotient must be an object")
        else:
            if "dimension" not in quotient:
                errors.append(f"strata[{label}].quotient.dimension must be present")
            if not isinstance(quotient.get("kernel"), str) or not quotient.get("kernel", "").strip():
                errors.append(f"strata[{label}].quotient.kernel must be a non-empty string")
        refs = stratum.get("certificates")
        if not isinstance(refs, list):
            errors.append(f"strata[{label}].certificates must be a list")
            continue
        for ref in refs:
            if not isinstance(ref, str) or not ref.strip():
                errors.append(f"strata[{label}].certificates contains a non-string reference")
            elif ref not in certificate_ids:
                errors.append(f"strata[{label}] references missing certificate '{ref}'")


def _validate_gaps(gaps: Sequence[Any], errors: List[str]) -> None:
    gap_ids: set[str] = set()
    for index, gap in enumerate(gaps):
        label = _item_label(gap, index, "gap")
        if not isinstance(gap, Mapping):
            errors.append(f"gaps[{index}] must be an object")
            continue
        for field in REQUIRED_GAP_FIELDS:
            _require_nonempty_string(gap, field, f"gaps[{label}].{field}", errors)
        gap_id = gap.get("id")
        if isinstance(gap_id, str):
            if gap_id in gap_ids:
                errors.append(f"duplicate gap id '{gap_id}'")
            gap_ids.add(gap_id)


def _validate_privacy(project: Mapping[str, Any], errors: List[str]) -> None:
    privacy = project.get("privacy", {})
    blocked_terms: List[str] = []
    if isinstance(privacy, Mapping):
        configured = privacy.get("blocked_terms", [])
        if isinstance(configured, list):
            blocked_terms = [term.lower() for term in configured if isinstance(term, str) and term]
        elif configured is not None:
            errors.append("privacy.blocked_terms must be a list when present")
    elif privacy is not None:
        errors.append("privacy must be an object when present")

    if not blocked_terms:
        return

    for path, value in _walk_strings(project):
        if path[:2] == ("privacy", "blocked_terms"):
            continue
        lowered = value.lower()
        for term in blocked_terms:
            if term in lowered:
                joined = ".".join(path)
                errors.append(f"forbidden source-specific term found at {joined}: '{term}'")


def _walk_strings(value: Any, path: Tuple[str, ...] = ()) -> Iterable[Tuple[Tuple[str, ...], str]]:
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, Mapping):
        for key, child in value.items():
            yield from _walk_strings(child, path + (str(key),))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_strings(child, path + (str(index),))


def _item_label(item: Any, index: int, fallback: str) -> str:
    if isinstance(item, Mapping) and isinstance(item.get("id"), str):
        return item["id"]
    return f"{fallback}-{index}"
