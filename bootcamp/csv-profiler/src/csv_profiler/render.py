import json
from pathlib import Path
from csv import DictReader
from typing import Union, List, Dict, Any # Added for better type hinting clarity

# --- Data Loading Function ---
def read_csv_rows(path: str | Path) -> List[Dict[str, str]]:
    """Reads a CSV file into a list of dictionaries."""
    path = Path(path)
    # The 'newline=""' argument is crucial for correct CSV reading in Python
    with path.open("r", encoding="utf-8", newline="") as f:
        return [dict(row) for row in DictReader(f)]

# --- Report Output Functions ---

def write_json(report: Dict[str, Any], path: str | Path) -> None:
    """Writes a dictionary report to a JSON file."""
    path = Path(path) 
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # ensure_ascii=False allows non-English characters to be written correctly
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8")

def md_header(title: str) -> List[str]:
    """Generates the main Markdown header for the report."""
    return [
        f"# Data Profile Report: {title}",
        "",
        "---",
        ""
    ]

def md_table_header() -> List[str]:
    """Generates the Markdown table header for column details."""
    return [
        "| Column | Missing | Non-Empty | Missing (%) |",
        "| :--- | ---: | ---: | ---: |"
    ]

def write_markdown(report: Dict[str, Any], path: str | Path) -> None:
    """Writes the data profile report into a Markdown file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True) 

    # Accessing report data
    rows = report["summary"]["rows"]
    
    lines: List[str] = []
    
    lines.extend(md_header("data/sample.csv")) # Placeholder for actual filename
    
    # Summary Section
    lines.append("## Summary")
    lines.append(f"- Rows: {rows:,}")
    # Note: Using 'n_col' from the report summary
    lines.append(f"- Columns: {report['summary']['n_col']:,}") 
    lines.append("")

    # Columns Table Header
    lines.append("## Columns (table)")
    lines.extend(md_table_header()) 

    # Table Content Loop
    # Note: Iterating over the 'columns' key added to the summary for output
    for name, stats in report["columns_stats"].items(): # Use a clearer key name for stats
        missing_count = stats["missing"]
        non_empty_count = stats["non_empty"]
        
        if rows > 0:
            missing_pct = (missing_count / rows) * 100
        else:
            missing_pct = 0.0
        
        lines.append(
            f"| {name} "
            f"| {missing_count:,} "      
            f"| {non_empty_count:,} "    
            f"| {missing_pct:.2f}% |"
        )
    
    path.write_text("\n".join(lines), encoding="utf-8")


# --- Profiling Logic Function ---
def basic_profile(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    """Calculates basic data profile statistics (missing/non-empty counts)."""
    if not rows:
        return {"summary": {"rows": 0, "n_col": 0}, "columns_stats": {}} 

    column_names = rows[0].keys()
    
    # Initialize trackers
    missing = {c: 0 for c in column_names}
    non_empty = {c: 0 for c in column_names}

    # Data Processing Loop
    for row in rows:
        for c in column_names:
            v = (row.get(c) or "").strip() 
            
            if v == "":
                missing[c] += 1
            else:
                non_empty[c]+= 1

    # Format the final report structure
    column_stats = {}
    for c in column_names:
        column_stats[c] = {
            "missing": missing[c],
            "non_empty": non_empty[c],
        }

    return{
        "summary": {
            "rows": len(rows),
            "n_col": len(column_names),
            "columns_defined": list(column_names),
        },
        # Renamed key for clarity in the final report
        "columns_stats": column_stats 
    }

# --- Example Usage (Fixed Entry Point) ---
if __name__ == "__main__":
    
    # Define the actual path to the CSV file
    csv_path = "/Users/rayan/Desktop/Boocamp_2/bootcamp/csv-profiler/src/data/sample.csv"
    
    try:
        # 1. Read the data
        data_rows = read_csv_rows(csv_path)
        
        # 2. Generate the actual profile report
        profile_report = basic_profile(data_rows) 
    
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_path}. Please check the path.")
        exit(1)
    except IndexError:
        print("Error: The CSV file is empty. Cannot generate profile report.")
        exit(1)


    # Define output paths
    output_path_Markdown = Path("./csv-profiler/src/outputs/report.md") # Renamed for clarity
    output_path_Json = Path("./csv-profiler/src/outputs/report.json")   # Changed extension to .json


    # 3. Write reports using the generated profile_report
    write_markdown(profile_report, output_path_Markdown)
    write_json(profile_report, output_path_Json)

    print(f"✅ Report successfully generated using live data.")
    print(f"   - Markdown: {output_path_Markdown.resolve()}")
    print(f"   - JSON:     {output_path_Json.resolve()}")