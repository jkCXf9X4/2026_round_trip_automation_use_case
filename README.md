# 2026 Round-Trip Automation Use Case

This repository packages the standalone case-study workflow described in [sections/07_case_study.tex](/home/eriro/pwa/2_work/2026_purpose_driven_modelling/sections/07_case_study.tex).

The workflow is aligned to the five paper steps:

1. Import the architectural entry point.
2. Develop the analysis architecture.
3. Generate exchange artifacts.
4. Introduce external modifications.
5. Synchronize validated changes.

## Notes

Step 2 and step 4 are intentionally represented by versioned manual assets because the case study defines them as human-authored workflow steps. The import, generation, and synchronization phases are executed through `pyssp_sysml2.cli`, and new externally introduced parts are inferred from the supplied candidate SSD during synchronization.

## Layout

- `manual/inputs/`: SSP snapshots used as case-study entry points.
- `manual/inputs/uc_v1.ssd` and `manual/inputs/uc_v2.ssd` for the UC_V1 and UC_V2 SSP snapshots.

- `manual/analysis_architecture/`: manually authored authoritative SysML v2 architecture for step 2.
- `manual/analysis_architecture/*.sysml` for the manually developed step-2 analysis architecture.

- `manual/external_modifications/`: manually prepared step-4 candidate edit artifact.
- `manual/external_modifications/uc_v2_candidate.ssd` for the manually prepared external candidate edit from step 4.

- `artifacts/` is generated on each run. The repository keeps only the source inputs needed to execute the workflow:

No generated workflow outputs are used as source inputs. The automated steps use the `pyssp_sysml2` CLI.

## Run

From inside this repository:

```bash
python3 -m venv venv
source . venv/bin/activate
pip install git+https://github.com/pyssporg/pyssp_sysml2
python3 ./run_workflow.py
```

This regenerates `artifacts/` from scratch and records a `manifest.json` for traceability.

To export the publication DOT graphs after running the workflow:

```bash
python3 ./export_step_dots.py
```

The DOT exports are written to `figures/`.



