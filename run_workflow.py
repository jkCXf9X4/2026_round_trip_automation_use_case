#!/usr/bin/env python3
"""Execute the case-study workflow from sections/07_case_study.tex."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = ROOT / "artifacts"
MANUAL_DIR = ROOT / "manual"
INPUTS_DIR = MANUAL_DIR / "inputs"

STEP1_DIR = ARTIFACTS_DIR / "01_import_architectural_entry_point"
STEP2_DIR = ARTIFACTS_DIR / "02_develop_analysis_architecture"
STEP3_DIR = ARTIFACTS_DIR / "03_generate_exchange_artifacts"
STEP4_DIR = ARTIFACTS_DIR / "04_introduce_external_modifications"
STEP5_DIR = ARTIFACTS_DIR / "05_synchronize_validated_changes"

MANUAL_ANALYSIS_ARCH_DIR = MANUAL_DIR / "analysis_architecture"
MANUAL_EXTERNAL_DIR = MANUAL_DIR / "external_modifications"

UC_V1_SSD = INPUTS_DIR / "uc_v1.ssd"
UC_V2_SSD = INPUTS_DIR / "uc_v2.ssd"
UC_V2_CANDIDATE_SSD = MANUAL_EXTERNAL_DIR / "uc_v2_candidate.ssd"

COMPOSITION = "UseCaseComposition"


@dataclass
class StepResult:
    step: str
    status: str
    outputs: list[str]
    details: str


def _reset_artifacts() -> None:
    if ARTIFACTS_DIR.exists():
        shutil.rmtree(ARTIFACTS_DIR)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def _relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _normalize_cli_output(line: str) -> str:
    written = line.removeprefix("Wrote ").strip()
    path = Path(written)
    if path.is_absolute():
        return _relative(path)
    return written


def _run_pyssp(*args: str | os.PathLike[str]) -> list[str]:
    command = [sys.executable, "-m", "pyssp_sysml2.cli", *map(os.fspath, args)]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )
    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip() or "pyssp command failed"
        raise RuntimeError(message)
    return [line for line in completed.stdout.splitlines() if line.strip()]


def _copy_tree(src: Path, dst: Path) -> list[Path]:
    dst.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for source in sorted(src.glob("*.sysml")):
        target = dst / source.name
        shutil.copy2(source, target)
        copied.append(target)
    return copied


def _step_1_import_architectural_entry_point() -> StepResult:
    STEP1_DIR.mkdir(parents=True, exist_ok=True)
    raw_ssd = STEP1_DIR / UC_V1_SSD.name
    bootstrap_sysml = STEP1_DIR / "uc_v1_imported.sysml"
    shutil.copy2(UC_V1_SSD, raw_ssd)
    _run_pyssp(
        "generate",
        "sysml",
        "--ssd",
        raw_ssd,
        "--composition",
        COMPOSITION,
        "--output",
        bootstrap_sysml,
    )
    return StepResult(
        step="import_architectural_entry_point",
        status="ok",
        outputs=[_relative(raw_ssd), _relative(bootstrap_sysml)],
        details="Imported UC_V1 as SSP and transformed it into a raw SysML-based architectural representation via the pyssp_sysml2 CLI.",
    )


def _step_2_develop_analysis_architecture() -> StepResult:
    written = _copy_tree(MANUAL_ANALYSIS_ARCH_DIR, STEP2_DIR)
    return StepResult(
        step="develop_analysis_architecture",
        status="ok",
        outputs=[_relative(path) for path in written],
        details="Materialized the maintained SysML v2 analysis architecture from the manual architecture-authoring step described in the case study.",
    )


def _step_3_generate_exchange_artifacts() -> StepResult:
    STEP3_DIR.mkdir(parents=True, exist_ok=True)
    ssd_path = STEP3_DIR / "SystemStructure.ssd"
    ssv_path = STEP3_DIR / "parameters.ssv"
    fmi_dir = STEP3_DIR / "model_descriptions"

    _run_pyssp(
        "generate",
        "ssd",
        "--architecture",
        STEP2_DIR,
        "--composition",
        COMPOSITION,
        "--output",
        ssd_path,
    )
    _run_pyssp(
        "generate",
        "ssv",
        "--architecture",
        STEP2_DIR,
        "--composition",
        COMPOSITION,
        "--output",
        ssv_path,
    )
    fmi_lines = _run_pyssp(
        "generate",
        "fmi",
        "--architecture",
        STEP2_DIR,
        "--composition",
        COMPOSITION,
        "--output-dir",
        fmi_dir,
    )

    outputs = [_relative(ssd_path), _relative(ssv_path)]
    outputs.extend(
        _normalize_cli_output(line)
        for line in fmi_lines
        if line.startswith("Wrote ")
    )
    return StepResult(
        step="generate_exchange_artifacts",
        status="ok",
        outputs=outputs,
        details="Generated SSD, SSV, and FMI model descriptions from the maintained analysis architecture via the pyssp_sysml2 CLI.",
    )


def _step_4_introduce_external_modifications() -> StepResult:
    STEP4_DIR.mkdir(parents=True, exist_ok=True)
    raw_intent = STEP4_DIR / "uc_v2_change_intent.ssd"
    candidate_edit = STEP4_DIR / "uc_v2_candidate.ssd"
    shutil.copy2(UC_V2_SSD, raw_intent)
    shutil.copy2(UC_V2_CANDIDATE_SSD, candidate_edit)
    return StepResult(
        step="introduce_external_modifications",
        status="ok",
        outputs=[_relative(raw_intent), _relative(candidate_edit)],
        details="Staged the externally edited candidate artifact set from the manual downstream modification step, using UC_V2 as change intent and the manual alignment artifacts required for synchronization.",
    )


def _step_5_synchronize_validated_changes() -> StepResult:
    validation_dir = STEP5_DIR / "validation"
    sync_input_dir = STEP5_DIR / "sync_input_architecture"
    synced_arch_dir = STEP5_DIR / "synced_architecture"
    validation_dir.mkdir(parents=True, exist_ok=True)
    _copy_tree(STEP2_DIR, sync_input_dir)

    raw_failure = validation_dir / "raw_uc_v2_sync_failure.txt"
    try:
        _run_pyssp(
            "sync",
            "ssd",
            "--architecture",
            sync_input_dir,
            "--composition",
            COMPOSITION,
            "--ssd",
            STEP4_DIR / "uc_v2_change_intent.ssd",
            "--output-architecture-dir",
            STEP5_DIR / "raw_sync_unexpected_success",
        )
    except RuntimeError as exc:
        raw_failure.write_text(f"{exc}\n", encoding="utf-8")
    else:
        raw_failure.write_text(
            "ERROR: raw UC_V2 synchronized successfully, but a validation failure was expected.\n",
            encoding="utf-8",
        )
        return StepResult(
            step="synchronize_validated_changes",
            status="unexpected_success",
            outputs=[_relative(raw_failure)],
            details="Validation unexpectedly accepted the raw UC_V2 change intent.",
        )

    sync_lines = _run_pyssp(
        "sync",
        "ssd",
        "--architecture",
        sync_input_dir,
        "--composition",
        COMPOSITION,
        "--ssd",
        STEP4_DIR / "uc_v2_candidate.ssd",
        "--output-architecture-dir",
        synced_arch_dir,
    )

    outputs = [_relative(raw_failure)]
    outputs.extend(
        _normalize_cli_output(line)
        for line in sync_lines
        if line.startswith("Wrote ")
    )
    return StepResult(
        step="synchronize_validated_changes",
        status="ok",
        outputs=outputs,
        details="Validated the candidate edit against the maintained architecture, rejected the raw UC_V2 intent, and synchronized the accepted candidate changes back into SysML via the pyssp_sysml2 CLI.",
    )


def main() -> int:
    _reset_artifacts()
    steps = [
        _step_1_import_architectural_entry_point(),
        _step_2_develop_analysis_architecture(),
        _step_3_generate_exchange_artifacts(),
        _step_4_introduce_external_modifications(),
        _step_5_synchronize_validated_changes(),
    ]

    manifest_path = ARTIFACTS_DIR / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "workflow": "uc_case_workflow",
                "composition": COMPOSITION,
                "steps": [asdict(step) for step in steps],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    for step in steps:
        print(f"[{step.status}] {step.step}: {step.details}")
        for output in step.outputs:
            print(f"  - {output}")
    print(f"  - {_relative(manifest_path)}")

    return 1 if any(step.status != "ok" for step in steps) else 0


if __name__ == "__main__":
    raise SystemExit(main())
