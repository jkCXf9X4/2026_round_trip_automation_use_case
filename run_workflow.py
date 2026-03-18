#!/usr/bin/env python3
"""Execute the UC case-study workflow and persist a traceable artifact trail."""
from __future__ import annotations

import json
import shutil
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

from pyssp_standard.ssd import SSD

from pyssp_sysml2.fmi import generate_model_descriptions
from pyssp_sysml2.ssd import generate_ssd
from pyssp_sysml2.ssv import generate_parameter_set
from pyssp_sysml2.sync import sync_sysml_from_ssd
from pyssp_sysml2.sysml import generate_sysml_from_ssd


ROOT = Path(__file__).resolve().parent
WORKFLOW_DIR = ROOT
ARTIFACTS_DIR = WORKFLOW_DIR / "artifacts"
INPUTS_DIR = ARTIFACTS_DIR / "01_inputs"
BOOTSTRAP_DIR = ARTIFACTS_DIR / "02_bootstrap"
MAINTAINED_ARCH_DIR = ARTIFACTS_DIR / "03_maintained_architecture"
GENERATED_DIR = ARTIFACTS_DIR / "04_generated"
EXTERNAL_DIR = ARTIFACTS_DIR / "05_external_edit"
SYNC_DIR = ARTIFACTS_DIR / "06_synced_architecture"
REPORTS_DIR = ARTIFACTS_DIR / "07_reports"
ARCHITECTURE_TEMPLATE_DIR = WORKFLOW_DIR / "architecture"
EXTERNAL_PART_DEFS_TEMPLATE = WORKFLOW_DIR / "external_part_definitions.sysml"

COMPOSITION = "UseCaseComposition"
INPUT_TEMPLATES_DIR = WORKFLOW_DIR / "inputs"
RAW_V1 = INPUT_TEMPLATES_DIR / "uc_v1.ssd"
RAW_V2 = INPUT_TEMPLATES_DIR / "uc_v2.ssd"


@dataclass
class StepResult:
    step: str
    status: str
    outputs: list[str]
    details: str


def _reset_artifact_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def _copy_inputs() -> StepResult:
    INPUTS_DIR.mkdir(parents=True, exist_ok=True)
    copied = []
    for source in (RAW_V1, RAW_V2):
        target = INPUTS_DIR / source.name
        shutil.copy2(source, target)
        copied.append(str(target.relative_to(WORKFLOW_DIR)))
    return StepResult(
        step="copy_inputs",
        status="ok",
        outputs=copied,
        details="Copied the supplied SSD inputs into the workflow artifact tree.",
    )


def _bootstrap_sysml() -> StepResult:
    BOOTSTRAP_DIR.mkdir(parents=True, exist_ok=True)
    output = BOOTSTRAP_DIR / "uc_v1_bootstrap.sysml"
    generate_sysml_from_ssd(INPUTS_DIR / RAW_V1.name, output, COMPOSITION)
    return StepResult(
        step="bootstrap_sysml",
        status="ok",
        outputs=[str(output.relative_to(WORKFLOW_DIR))],
        details="Generated the minimal SysML bootstrap directly from uc_v1.ssd.",
    )


def _materialize_maintained_architecture() -> StepResult:
    MAINTAINED_ARCH_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for source in sorted(ARCHITECTURE_TEMPLATE_DIR.glob("*.sysml")):
        target = MAINTAINED_ARCH_DIR / source.name
        shutil.copy2(source, target)
        written.append(str(target.relative_to(WORKFLOW_DIR)))
    return StepResult(
        step="materialize_maintained_architecture",
        status="ok",
        outputs=written,
        details=(
            "Copied the normalized, split SysML analysis architecture with named proxy ports "
            "and canonicalized component definitions."
        ),
    )


def _generate_derived_artifacts() -> StepResult:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    ssd_path = GENERATED_DIR / "SystemStructure.ssd"
    ssv_path = GENERATED_DIR / "parameters.ssv"
    fmi_dir = GENERATED_DIR / "model_descriptions"

    generate_ssd(MAINTAINED_ARCH_DIR, ssd_path, COMPOSITION)
    generate_parameter_set(MAINTAINED_ARCH_DIR, ssv_path, COMPOSITION)
    fmi_paths = generate_model_descriptions(MAINTAINED_ARCH_DIR, fmi_dir, COMPOSITION)

    outputs = [
        str(ssd_path.relative_to(WORKFLOW_DIR)),
        str(ssv_path.relative_to(WORKFLOW_DIR)),
        *(str(path.relative_to(WORKFLOW_DIR)) for path in fmi_paths),
    ]
    return StepResult(
        step="generate_derived_artifacts",
        status="ok",
        outputs=outputs,
        details="Generated the maintained architecture's SSD, SSV, and FMI-facing artifacts.",
    )


def _clean_external_ssd() -> StepResult:
    EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)
    raw_copy = EXTERNAL_DIR / RAW_V2.name
    cleaned_copy = EXTERNAL_DIR / "uc_v2_cleaned.ssd"
    overlay_dir = EXTERNAL_DIR / "architecture_overlay"
    shutil.copy2(INPUTS_DIR / RAW_V2.name, raw_copy)
    shutil.copy2(INPUTS_DIR / RAW_V2.name, cleaned_copy)
    overlay_dir.mkdir(parents=True, exist_ok=True)
    for source in sorted(MAINTAINED_ARCH_DIR.glob("*.sysml")):
        shutil.copy2(source, overlay_dir / source.name)
    shutil.copy2(
        EXTERNAL_PART_DEFS_TEMPLATE,
        overlay_dir / EXTERNAL_PART_DEFS_TEMPLATE.name,
    )

    rename_map = {}
    def normalize(name: str) -> str:
        if name.endswith(".in.y"):
            return f"{name[: -len('.in.y')]}.value"
        if name.endswith(".out.y"):
            return f"{name[: -len('.out.y')]}.value"
        if "." not in name:
            return f"{name}.value"
        return name

    with SSD(cleaned_copy, mode="a") as ssd:
        if ssd.system is None:
            raise ValueError("No system element found in uc_v2.ssd")

        for component in ssd.system.elements:
            for connector in component.connectors:
                updated = normalize(connector.name)
                if updated != connector.name:
                    rename_map[f"{component.name}.{connector.name}"] = f"{component.name}.{updated}"
                    connector.name = updated

        for connection in ssd.system.connections:
            connection.start_connector = normalize(connection.start_connector)
            connection.end_connector = normalize(connection.end_connector)

    report_path = REPORTS_DIR / "external_cleanup.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(rename_map, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return StepResult(
        step="clean_external_ssd",
        status="ok",
        outputs=[
            str(raw_copy.relative_to(WORKFLOW_DIR)),
            str(cleaned_copy.relative_to(WORKFLOW_DIR)),
            str((overlay_dir / EXTERNAL_PART_DEFS_TEMPLATE.name).relative_to(WORKFLOW_DIR)),
            str(report_path.relative_to(WORKFLOW_DIR)),
        ],
        details=(
            "Normalized the external SSD connector names and staged the late-phase part "
            "definitions required for synchronization."
        ),
    )


def _sync_clean_edit() -> StepResult:
    SYNC_DIR.mkdir(parents=True, exist_ok=True)
    written = sync_sysml_from_ssd(
        architecture_path=EXTERNAL_DIR / "architecture_overlay",
        ssd_path=EXTERNAL_DIR / "uc_v2_cleaned.ssd",
        composition=COMPOSITION,
        output_architecture_dir=SYNC_DIR,
    )
    return StepResult(
        step="sync_clean_edit",
        status="ok",
        outputs=[str(path.relative_to(WORKFLOW_DIR)) for path in written],
        details="Applied the cleaned external edit back into the maintained SysML architecture.",
    )


def _record_expected_failure() -> StepResult:
    failure_path = REPORTS_DIR / "raw_uc_v2_sync_failure.txt"
    try:
        sync_sysml_from_ssd(
            architecture_path=EXTERNAL_DIR / "architecture_overlay",
            ssd_path=EXTERNAL_DIR / RAW_V2.name,
            composition=COMPOSITION,
            output_architecture_dir=ARTIFACTS_DIR / "raw_sync_unexpected_success",
        )
    except Exception as exc:  # noqa: BLE001 - report exact failure for traceability
        failure_path.write_text(f"{type(exc).__name__}: {exc}\n", encoding="utf-8")
        return StepResult(
            step="record_expected_failure",
            status="ok",
            outputs=[str(failure_path.relative_to(WORKFLOW_DIR))],
            details="Captured the expected sync validation failure for the uncleaned uc_v2.ssd.",
        )

    failure_path.write_text(
        "ERROR: raw uc_v2.ssd synchronized successfully, but a validation failure was expected.\n",
        encoding="utf-8",
    )
    return StepResult(
        step="record_expected_failure",
        status="unexpected_success",
        outputs=[str(failure_path.relative_to(WORKFLOW_DIR))],
        details="The raw external edit synchronized successfully when a validation failure was expected.",
    )


def main() -> int:
    _reset_artifact_dir(ARTIFACTS_DIR)
    steps = [
        _copy_inputs(),
        _bootstrap_sysml(),
        _materialize_maintained_architecture(),
        _generate_derived_artifacts(),
        _clean_external_ssd(),
        _sync_clean_edit(),
        _record_expected_failure(),
    ]

    manifest = {
        "workflow": "uc_case_workflow",
        "composition": COMPOSITION,
        "steps": [asdict(step) for step in steps],
    }
    manifest_path = REPORTS_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    unexpected = [step for step in steps if step.status != "ok"]
    for step in steps:
        print(f"[{step.status}] {step.step}: {step.details}")
        for output in step.outputs:
            print(f"  - {output}")

    return 1 if unexpected else 0


if __name__ == "__main__":
    sys.exit(main())
