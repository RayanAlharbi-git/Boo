
def basic_profile(rows: list[dict[str, str]], source: str | None = None) -> dict:
    if not rows:
        return {
            "source": source,
            "summary": {"rows": 0, "columns": 0},
            "columns": {}
        }

    column_names = rows[0].keys()
    # Collect all column values
    columns_values: dict[str, list[str]] = {c: [] for c in column_names}
    for row in rows:
        for c in column_names:
            v = row.get(c) or ""
            columns_values[c].append(v.strip())

    columns_profile = {}
    for c, values in columns_values.items():
        col_type = infer_type(values)
        if col_type == "number":
            stats = numeric_stats(values)
        else:
            stats = text_stats(values)
        columns_profile[c] = {
            "type": col_type,
            "stats": stats
        }

    return {
        "source": source,
        "summary": {"rows": len(rows), "columns": len(column_names)},
        "columns": columns_profile
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

from collections import Counter

def text_stats(values: list[str], top_k: int = 5) -> dict:
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)

    count = len(usable)
    unique = len(set(usable))

    counts: dict[str, int] = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1

    top = [{"value": val, "count": c} for val, c in sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_k]]

    return {
        "count": count,
        "missing": missing,
        "unique": unique,
        "top": top
    }

from collections import Counter

def numeric_stats(values: list[str], top_k: int = 5) -> dict:
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
    
    top_counts = Counter(nums).most_common(top_k)
    top = [{"value": val, "count": c} for val, c in top_counts]

    return {
        "count": count,
        "missing": missing,
        "unique": unique,
        "top": top_counts
    }
