from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "iris.csv"
OUTPUT_DIR = ROOT / "outputs"
REPORT_DIR = ROOT / "reports"

NUMERIC_COLUMNS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
DESCRIPTIONS = {
    "sepal_length": "Sepal length in centimeters",
    "sepal_width": "Sepal width in centimeters",
    "petal_length": "Petal length in centimeters",
    "petal_width": "Petal width in centimeters",
}

def make_summary(df):
    rows = []
    for col in NUMERIC_COLUMNS:
        s = pd.to_numeric(df[col], errors="coerce")
        modes = s.mode(dropna=True)
        rows.append({
            "column": col,
            "description": DESCRIPTIONS[col],
            "count": int(s.count()),
            "missing": int(s.isna().sum()),
            "mean": s.mean(),
            "median": s.median(),
            "mode": ", ".join(f"{x:g}" for x in modes.tolist()) if len(modes) else "N/A",
            "standard_deviation": s.std(),
            "minimum": s.min(),
            "25th_percentile": s.quantile(.25),
            "50th_percentile": s.quantile(.50),
            "75th_percentile": s.quantile(.75),
            "maximum": s.max(),
            "IQR": s.quantile(.75) - s.quantile(.25),
        })
    return pd.DataFrame(rows)

def make_report(df, summary):
    lines = [
        "# Task 9 — Iris Descriptive Statistics Interpretation Report",
        "",
        "## Dataset overview",
        f"- Total observations: **{len(df)}**",
        f"- Total columns: **{df.shape[1]}**",
        f"- Species represented: **{df['species'].nunique()}**",
        f"- Missing cells in the dataset: **{int(df.isna().sum().sum())}**",
        "",
        "## Overall findings",
    ]
    for _, row in summary.iterrows():
        col = row["column"]
        lines.append(
            f"- **{col.replace('_', ' ').title()}**: mean = {row['mean']:.2f} cm, "
            f"median = {row['median']:.2f} cm, standard deviation = {row['standard_deviation']:.2f} cm, "
            f"middle 50% = {row['25th_percentile']:.2f}–{row['75th_percentile']:.2f} cm "
            f"(IQR = {row['IQR']:.2f} cm)."
        )
        if row["mean"] > row["median"]:
            lines.append(f"  The mean is greater than the median for {col.replace('_', ' ')}, which can be consistent with right-skew; check the distribution before drawing a firm conclusion.")
        elif row["mean"] < row["median"]:
            lines.append(f"  The mean is less than the median for {col.replace('_', ' ')}, which can be consistent with left-skew; check the distribution before drawing a firm conclusion.")
        else:
            lines.append(f"  The mean and median are equal for {col.replace('_', ' ')}; these measures alone do not determine the distribution's shape.")
    lines += ["", "## Species comparison", ""]
    grouped = df.groupby("species")[NUMERIC_COLUMNS].mean()
    for species, row in grouped.iterrows():
        lines.append(
            f"- **{species.title()}** average measurements: sepal length {row['sepal_length']:.2f} cm, "
            f"sepal width {row['sepal_width']:.2f} cm, petal length {row['petal_length']:.2f} cm, "
            f"petal width {row['petal_width']:.2f} cm."
        )
    lines += [
        "",
        "## Interpretation",
        "- Compare mean and median to look for possible skew, but inspect histograms to confirm distribution shape.",
        "- Standard deviation measures spread in the original unit (centimeters); larger values mean greater variability.",
        "- The 25th and 75th percentiles describe the middle 50% of measurements.",
        "- Species-wise averages show descriptive differences between groups; they do not, by themselves, prove causation.",
        "",
    ]
    return "\n".join(lines)

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")
    df = pd.read_csv(DATA_FILE)
    missing_columns = [c for c in NUMERIC_COLUMNS + ["species"] if c not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing expected columns: {missing_columns}")

    summary = make_summary(df)
    missing = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(df[c].dtype) for c in df.columns],
        "non_missing_count": [int(df[c].notna().sum()) for c in df.columns],
        "missing_count": [int(df[c].isna().sum()) for c in df.columns],
        "missing_percent": [float(df[c].isna().mean() * 100) for c in df.columns],
    })
    cleaned = df.copy()
    for col in NUMERIC_COLUMNS:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")
        if cleaned[col].notna().any():
            cleaned[col] = cleaned[col].fillna(cleaned[col].median())

    species_summary = df.groupby("species")[NUMERIC_COLUMNS].agg(["count", "mean", "median", "std", "min", "max"])
    species_summary.columns = ["_".join(map(str, c)) for c in species_summary.columns]
    species_summary = species_summary.reset_index()

    summary.to_csv(OUTPUT_DIR / "summary_statistics.csv", index=False)
    cleaned.to_csv(OUTPUT_DIR / "cleaned_iris.csv", index=False)
    (REPORT_DIR / "interpretation_report.md").write_text(make_report(df, summary), encoding="utf-8")

    workbook = OUTPUT_DIR / "iris_descriptive_statistics.xlsx"
    with pd.ExcelWriter(workbook, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="Summary Statistics", index=False)
        missing.to_excel(writer, sheet_name="Missing Values", index=False)
        species_summary.to_excel(writer, sheet_name="Species Comparison", index=False)
        df.head(20).to_excel(writer, sheet_name="First 20 Rows", index=False)
        cleaned.to_excel(writer, sheet_name="Cleaned Data", index=False)
        for ws in writer.book.worksheets:
            ws.freeze_panes = "A2"
            ws.auto_filter.ref = ws.dimensions
            for column_cells in ws.columns:
                max_len = max((len(str(cell.value)) if cell.value is not None else 0) for cell in column_cells)
                ws.column_dimensions[column_cells[0].column_letter].width = min(max(max_len + 2, 12), 42)
            for cell in ws[1]:
                cell.font = cell.font.copy(bold=True)

    print(f"Dataset shape: {df.shape}")
    print("\nSummary statistics:")
    print(summary[["column", "count", "missing", "mean", "median", "mode", "standard_deviation", "25th_percentile", "75th_percentile"]].to_string(index=False))
    print(f"\nExcel workbook created: {workbook}")
    print(f"CSV summary created: {OUTPUT_DIR / 'summary_statistics.csv'}")
    print(f"Interpretation report created: {REPORT_DIR / 'interpretation_report.md'}")

if __name__ == "__main__":
    main()
