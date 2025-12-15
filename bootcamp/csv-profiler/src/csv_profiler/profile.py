
def basic_profile(rows: list[dict[str, str]]) -> dict:
    # 1. Handle empty input data
    if not rows:
        # Returns early if there are no rows
        return {"rows": 0, "n_col": 0, "columns_defined": []} 

    # --- FIX APPLIED HERE ---
    # Derive column names from the keys of the first row (dictionary)
    column_names = rows[0].keys()
    
    # Initialize all tracker dictionaries using the correct column names
    # Note: The `columns` dictionary itself is mostly just a placeholder/list of keys
    columns = {c: 0 for c in column_names}
    missing = {c: 0 for c in column_names}
    non_empty = {c: 0 for c in column_names}
    # ------------------------

    # 2. Iterate through all data rows
    for row in rows:
        # 3. Iterate through all defined columns
        for c in column_names: # Iterate over column_names directly for clarity
            
            # v = (row.get(c) or "").strip() 
            # Safely gets the value, defaults to "" if None or missing key, then strips whitespace
            v = (row.get(c) or "").strip() 
            
            # 4. Counting logic
            if v == "":
                # If the value is empty after stripping (missing or blank)
                missing[c] += 1
            else:
                # If the value has content
                non_empty[c]+= 1

    # 5. Return the profiling summary
    return{
        "rows": len(rows),
        "n_col": len(column_names),
        "columns_defined": list(column_names), # Explicitly list the column names
        "missing": missing,
        "non_empty": non_empty
    }


MISSING = {"", "na", "n/a", "null", "none", "nan"}

def is_missing(value: str | None) -> bool:
    if value is None:
     return True
    return value.strip().casefold() in MISSING

def try_float(value: str) -> float | None:
    try:
     return float(value)
    except ValueError:
     return None

def infer_type(values: list[str]) -> str:
   usable = [v for v in values if not is_missing(v)]
   if not usable:
      return "text"
   for v in usable:
      if try_float(v) is None:
         return "text"
      
   return "number"

def numeric_stats(values:  list[str]) -> dict:
 usable = [v for v in values if not is_missing(v)]
 missing = len(values) - len(usable)
 nums: list[float] = []
 for v in usable:
   x = try_float(v)
 if x is None:
   raise ValueError(f"Non-numeric value found: {v!r}")
 nums.append(x)

 count = len(nums)
 unique = len(set(nums))
 return {
 "count": count,

def main():
    # Ensure this path is correct on your machine for the code to run
    file_path = "/Users/rayan/Desktop/Boocamp_2/bootcamp/src/data/sample.csv"
    
    try:
        data_rows = read_csv_rows(file_path)
        profile_report = basic_profile(data_rows)
        
        # Optional: Print the results nicely
        import json
        print(json.dumps(profile_report, indent=4))
        
    except FileNotFoundError:
        print(f"Error: The file path was not found: {file_path}")
    except Exception as e:
        print(f"An error occurred during profiling: {e}")

if __name__=="__main__":
    main()