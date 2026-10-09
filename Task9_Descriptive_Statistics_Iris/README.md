# Task 9 — Descriptive Statistics Primer (Iris Dataset)

**Internship task:** Calculate and interpret mean, median, mode, standard deviation, and percentiles for numeric columns.

## Tools used
- **Python** — run the analysis
- **Pandas** — data cleaning and statistics
- **Excel** — final summary workbook
- **Streamlit** — optional interactive dashboard

## Project structure
```text
Task9_Descriptive_Statistics_Iris/
├── analysis.py
├── app.py
├── requirements.txt
├── run_analysis.bat
├── data/
│   └── iris.csv
├── outputs/
│   ├── iris_descriptive_statistics.xlsx
│   ├── summary_statistics.csv
│   └── cleaned_iris.csv
└── reports/
    └── interpretation_report.md
```

## Run on Windows / VS Code
1. Extract the ZIP and open the folder in VS Code.
2. Open Terminal → New Terminal.
3. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Run:
   ```bash
   python analysis.py
   ```
5. Open `outputs/iris_descriptive_statistics.xlsx` in Excel.
6. Optional dashboard:
   ```bash
   streamlit run app.py
   ```

The Iris CSV is included in `data/iris.csv`, so no internet is required to run the project.

## Analysis workflow
1. Load the Iris dataset using Pandas.
2. Check the shape, data types, and missing values.
3. Calculate count, missing count, mean, median, mode, standard deviation, minimum, 25th percentile, 50th percentile, 75th percentile, maximum, and interquartile range (IQR).
4. Export the results to Excel and CSV.
5. Compare measurements across the three Iris species.
6. Generate an interpretation report.

## Columns
- `sepal_length` — sepal length in centimeters
- `sepal_width` — sepal width in centimeters
- `petal_length` — petal length in centimeters
- `petal_width` — petal width in centimeters
- `species` — Iris species label

## Statistical concepts
- **Mean:** arithmetic average; can be influenced by extreme values.
- **Median:** middle value; more robust to skew and outliers.
- **Mode:** most frequently occurring value.
- **Standard deviation:** spread around the mean.
- **Percentiles:** the 25th and 75th percentiles define the middle 50% range; IQR = Q3 − Q1.

## Deliverables
- Excel workbook with overall summary, missing values, species-wise summary, first 20 rows, and full data.
- CSV summary and cleaned data.
- Interpretation report with key findings.
- Optional interactive Streamlit dashboard.

## Submission checklist
- [ ] Run `python analysis.py` successfully.
- [ ] Review the Excel workbook and interpretation report.
- [ ] Upload the project to a public GitHub repository if required.
- [ ] Share the completed project on LinkedIn if required by your internship.
