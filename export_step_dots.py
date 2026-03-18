#!/usr/bin/env python3
"""Export conference-friendly DOT graphs for selected UC workflow architecture steps."""
from __future__ import annotations

from pathlib import Path

from pycps_sysmlv2 import NodeType, SysMLParser


ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = ROOT / "artifacts"
FIGURES_DIR = ROOT / "figures"
COMPOSITION = "UseCaseComposition"

STEP_EXPORTS = {
    "03_maintained_architecture": FIGURES_DIR / "usecase_step3_architecture.dot",
    "06_synced_architecture": FIGURES_DIR / "usecase_step6_architecture.dot",
}

GRAPH_TITLES = {
    "03_maintained_architecture": "Step 3: Maintained Analysis Architecture",
    "06_synced_architecture": "Step 6: Synchronized Analysis Architecture",
}

GRAPH_NAMES = {
    "03_maintained_architecture": "usecase_step3_architecture",
    "06_synced_architecture": "usecase_step6_architecture",
}

NODE_LABELS = {
    "adaption": "Adaptation Unit",
    "atmos": "Atmosphere",
    "consumer": "Consumer",
    "ecs_hw": "ECS Hardware",
    "ecs_sw": "ECS Software",
    "fuel": "Fuel System",
    "interface_model": "Aero Interface",
    "valve_model": "Valve Model",
}

NODE_GROUPS = {
    "Atmosphere": {"atmos"},
    "ECS Core": {"ecs_hw", "ecs_sw", "adaption", "consumer"},
    "Additional Couplings": {"fuel", "interface_model", "valve_model"},
}

GROUP_STYLES = {
    "Atmosphere": {"fillcolor": "#F2F2F2"},
    "ECS Core": {"fillcolor": "#FAFAFA"},
    "Additional Couplings": {"fillcolor": "#ECECEC"},
}


def _quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _style_attrs(**kwargs: str) -> str:
    return ", ".join(f'{key}={_quote(value)}' for key, value in kwargs.items())


def _group_for(node_name: str) -> str | None:
    for group_name, members in NODE_GROUPS.items():
        if node_name in members:
            return group_name
    return None


def _render_publication_dot(step_dir_name: str) -> str:
    architecture = SysMLParser(ARTIFACTS_DIR / step_dir_name).parse()
    composition = architecture.defs(NodeType.Part)[COMPOSITION]

    part_names = set(composition.refs(NodeType.Part))
    grouped_edges: set[tuple[str, str]] = set()
    for connection in composition.defs(NodeType.Connection).values():
        part_names.add(connection.src_part)
        part_names.add(connection.dst_part)
        grouped_edges.add((connection.src_part, connection.dst_part))

    lines = [f"digraph {GRAPH_NAMES[step_dir_name]} {{"]
    lines.append(
        f"  graph [{_style_attrs(rankdir='TB', splines='ortho', pad='0.06', margin='0.02', nodesep='0.18', ranksep='0.32', bgcolor='white', labelloc='t', labeljust='c', label=GRAPH_TITLES[step_dir_name], fontname='Helvetica-Bold', fontsize='11')}];"
    )
    lines.append(
        f"  node [{_style_attrs(shape='box', style='rounded,filled', color='#3A3A3A', penwidth='0.9', fillcolor='white', fontname='Helvetica', fontsize='9', margin='0.10,0.06', width='1.0', height='0.32')}];"
    )
    lines.append(
        f"  edge [{_style_attrs(color='#4A4A4A', penwidth='0.8', arrowsize='0.55')}];"
    )
    lines.append("")

    grouped_nodes: dict[str, list[str]] = {}
    ungrouped_nodes: list[str] = []
    for part_name in sorted(part_names):
        group = _group_for(part_name)
        if group is None:
            ungrouped_nodes.append(part_name)
        else:
            grouped_nodes.setdefault(group, []).append(part_name)

    cluster_index = 0
    for group_name, members in grouped_nodes.items():
        cluster_index += 1
        lines.append(f"  subgraph cluster_{cluster_index} {{")
        lines.append(
            f"    graph [{_style_attrs(label=group_name, color='#8C8C8C', penwidth='0.7', style='rounded,dashed,filled', fontname='Helvetica-Bold', fontsize='9', margin='10', **GROUP_STYLES.get(group_name, {}))}];"
        )
        for part_name in members:
            lines.append(
                f"    {_quote(part_name)} [{_style_attrs(label=NODE_LABELS.get(part_name, part_name))}];"
            )
        lines.append("  }")
        lines.append("")

    for part_name in ungrouped_nodes:
        lines.append(
            f"  {_quote(part_name)} [{_style_attrs(label=NODE_LABELS.get(part_name, part_name))}];"
        )

    if ungrouped_nodes:
        lines.append("")

    for src_part, dst_part in sorted(grouped_edges):
        lines.append(f"  {_quote(src_part)} -> {_quote(dst_part)};")

    lines.append("}")
    return "\n".join(lines) + "\n"


def export_step(step_dir_name: str, output_path: Path) -> None:
    output_path.write_text(_render_publication_dot(step_dir_name), encoding="utf-8")


def main() -> int:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    for step_dir_name, output_path in STEP_EXPORTS.items():
        export_step(step_dir_name, output_path)
        print(output_path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
