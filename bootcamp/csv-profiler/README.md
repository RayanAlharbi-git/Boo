# CSV Profiler

A lightweight Python tool that profiles CSV files and generates:
- A **JSON report** (machine-readable)
- A **Markdown report** (human-readable)

The profiler automatically:
- Detects column types (number / text)
- Ignores missing values
- Computes statistics per column
- Shows top values and missing percentages

---

## Features

- Automatic type inference (numeric vs text)
- Missing value detection (`"", na, n/a, null, none, nan`)
- Numeric statistics:
  - count, missing, unique
  - top values
- Text statistics:
  - count, missing, unique
  - top values
- Outputs:
  - `report.json`
  - `report.md`



