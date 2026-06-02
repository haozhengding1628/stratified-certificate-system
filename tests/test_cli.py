import json

from stratcert.cli import main


def test_cli_init_validate_and_report(tmp_path):
    project_dir = tmp_path / "demo"
    report_file = tmp_path / "report.md"

    assert main(["init", str(project_dir)]) == 0
    assert (project_dir / "classification.json").exists()

    assert main(["validate", str(project_dir)]) == 0
    assert main(["report", str(project_dir), "--out", str(report_file)]) == 0

    data = json.loads((project_dir / "classification.json").read_text(encoding="utf-8"))
    report = report_file.read_text(encoding="utf-8")

    assert data["project"]["name"] == "Toy certificate classification"
    assert "# Toy certificate classification" in report
