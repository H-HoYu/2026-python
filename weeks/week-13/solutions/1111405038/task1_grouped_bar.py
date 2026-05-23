from __future__ import annotations

from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

YEARS = [112, 113, 114]
DEFAULT_DATA_DIR = Path(__file__).resolve().parents[4] / "assets" / "stu-data"


def configure_plot_font() -> None:
    """Use a CJK-capable font when available to render Chinese labels."""
    candidates = ["Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC", "SimHei"]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
            break
    plt.rcParams["axes.unicode_minus"] = False


def load_year(year: int, data_dir: Path) -> dict[str, int]:
    """Read one year CSV and return counts by department."""
    csv_path = data_dir / f"{year}年新生資料庫.csv"
    counts: Counter[str] = Counter()

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file_obj:
        # Use plain split to keep dependencies minimal and support BOM files.
        import csv

        reader = csv.DictReader(file_obj)
        for row in reader:
            dept = (row.get("系所名稱") or "").strip()
            if dept:
                counts[dept] += 1

    return dict(counts)


def get_top_depts(year_data: dict[int, dict[str, int]], top_n: int = 8) -> list[str]:
    """Pick departments that are strong in any year and return up to top_n."""
    if top_n <= 0:
        return []

    candidates: dict[str, tuple[int, int]] = {}
    for counts in year_data.values():
        sorted_depts = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        for dept, _ in sorted_depts[:top_n]:
            if dept not in candidates:
                candidates[dept] = (0, 0)

    for dept in list(candidates):
        max_count = max(year_data.get(year, {}).get(dept, 0) for year in year_data)
        total = sum(year_data.get(year, {}).get(dept, 0) for year in year_data)
        candidates[dept] = (max_count, total)

    ranked = sorted(candidates.items(), key=lambda item: (-item[1][0], -item[1][1], item[0]))
    return [dept for dept, _ in ranked[:top_n]]


def plot_grouped_bar(
    year_data: dict[int, dict[str, int]],
    depts: list[str],
    output_path: Path,
) -> None:
    """Draw grouped horizontal bars for selected departments."""
    configure_plot_font()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    y_pos = np.arange(len(depts))
    bar_height = 0.22

    fig, ax = plt.subplots(figsize=(11, 6.5))

    for idx, year in enumerate(YEARS):
        values = [year_data.get(year, {}).get(dept, 0) for dept in depts]
        offset = (idx - 1) * bar_height
        ax.barh(y_pos + offset, values, height=bar_height, label=str(year))

    ax.set_yticks(y_pos)
    ax.set_yticklabels(depts)
    ax.set_xlabel("人數")
    ax.set_ylabel("系所名稱")
    ax.set_title("112-114 學年度各系招生人數（前 8 系並排比較）")
    ax.legend(title="學年度")
    ax.grid(axis="x", linestyle="--", alpha=0.35)

    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def main() -> None:
    year_data = {year: load_year(year, DEFAULT_DATA_DIR) for year in YEARS}
    depts = get_top_depts(year_data, top_n=8)

    output_path = Path(__file__).resolve().parent / "output" / "task1.png"
    plot_grouped_bar(year_data, depts, output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
