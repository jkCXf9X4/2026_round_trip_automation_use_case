# 2026 Round-Trip Automation Use Case

This repository contains the standalone `uc_case_workflow` used to instantiate the case-study sequence from `sections/07_case_study.tex`.

All workflow-specific inputs and templates required to run the use case are included here:

- `inputs/uc_v1.ssd`
- `inputs/uc_v2.ssd`
- `architecture/*.sysml`
- `external_part_definitions.sysml`
- `run_workflow.py`
- `export_step_dots.py`

The workflow produces a traceable artifact trail under `artifacts/`, with numbered folders matching execution order:

1. Copy the supplied SSD inputs into the workflow artifact tree.
2. Bootstrap a minimal SysML architecture from `uc_v1.ssd`.
3. Materialize/copy in the maintained analysis architecture. This is pre altered, located in `architecture/*.sysml`
4. Generate the derived SSD, SSV, and FMI-facing artifacts.
5. Clean the external `uc_v2.ssd` edit and stage the synchronization overlay.
6. Synchronize the cleaned edit back into SysML.
7. Record the expected synchronization failure for the uncleaned `uc_v2.ssd`.

## Prerequisites

- Python 3
- `pyssp_sysml2` available on `PYTHONPATH`
- `pyssp_standard` and `pycps_sysmlv2` installed in the active environment


Or from inside this repository:

```bash
source ../../venv/bin/activate
PYTHONPATH=../pyssp_sysml2/src ./run_workflow.py
```

To export the publication DOT graphs after running the workflow:

```bash
source ../../venv/bin/activate
PYTHONPATH=../pyssp_sysml2/src ./export_step_dots.py
```

The DOT exports are written to `figures/`.

## Traceability

The maintained architecture template is kept under `architecture/` and copied into the artifact tree on each workflow run before generation.
Late-phase part definitions introduced by the external SSD edit are staged from `external_part_definitions.sysml` into `artifacts/05_external_edit/architecture_overlay/` before synchronization.
