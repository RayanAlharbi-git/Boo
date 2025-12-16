

from __future__ import annotations

import json
from pathlib import Path


def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def md_header(title: str) -> list[str]:
    return [f"# {title}\n"]

def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []

    # 1. Header block
    lines.extend(md_header("CSV Profiling Report"))

    # 2. Summary bullets
    summary = report.get("summary", {})
    lines.append(f"- Rows: **{summary.get('rows', 0)}**")
    lines.append(f"- Columns: **{summary.get('columns', 0)}**\n")

    columns = report.get("columns", {})

    # 3. Table: one row per column (type, missing %, unique)
    lines.append("## Column Overview\n")
    lines.append("| Column | Type | Missing % | Unique |")
    lines.append("|--------|------|-----------|--------|")

    total_rows = summary.get("rows", 0)
    for col_name, col_report in columns.items():
        col_type = col_report.get("type", "unknown")
        stats = col_report.get("stats", {})
        missing = stats.get("missing", 0)
        unique = stats.get("unique", 0)
        missing_pct = (missing / total_rows * 100) if total_rows else 0.0
        lines.append(f"| {col_name} | {col_type} | {missing_pct:.2f}% | {unique} |")

    lines.append("")

    # 4. Per-column details
    for col_name, col_report in columns.items():
        lines.append(f"## {col_name} Details\n")
        col_type = col_report.get("type", "unknown")
        stats = col_report.get("stats", {})

        lines.append(f"- Type: **{col_type}**")
        lines.append(f"- Missing: **{stats.get('missing', 0)}**")
        lines.append(f"- Unique: **{stats.get('unique', 0)}**")

        if col_type == "number":
            nums = [v for v in stats.get("top", [])]
            # Show min/max/mean
            all_values = [v["value"] for v in stats.get("top", [])]  # best effort
            if all_values:
                min_val = min(all_values)
                max_val = max(all_values)
                mean_val = sum(all_values) / len(all_values)
                lines.append(f"- Min: {min_val}")
                lines.append(f"- Max: {max_val}")
                lines.append(f"- Mean: {mean_val:.2f}")
            # Top values
            lines.append("- Top values:")
            for v in stats.get("top", []):
                lines.append(f"  - {v['value']} ({v['count']})")
        else:
            # Text: top values
            lines.append("- Top values:")
            for v in stats.get("top", []):
                lines.append(f"  - {v['value']} ({v['count']})")

        lines.append("")

    # Write to file
    path.write_text("\n".join(lines), encoding="utf-8")
