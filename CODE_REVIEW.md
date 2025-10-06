# Code Review — UK Railway Route Finder (Dijkstra)

Overall: ✅ **Correct, clear, and idiomatic** implementation for an Advanced Algorithms assignment.  
It cleanly loads a CSV, builds an undirected weighted graph, runs Dijkstra with a priority queue, reconstructs the path, and prints totals.

Below are **actionable improvements** to make it more robust and user‑friendly, without changing the core logic.

---

## 1) File path robustness
**Current:**  
```python
filename = "task1_3/task1_3_data.csv"
```
If the CSV isn’t in a `task1_3/` subfolder, this breaks.

**Better:** use a path relative to the script:
```python
from pathlib import Path
filename = Path(__file__).with_name("task1_3_data.csv")
graph = load_graph(str(filename))
```

**Or:** allow a `--csv` CLI flag (see §4).

---

## 2) Input normalization & helpful errors
When users type station names, they might use different cases or extra spaces.

**Suggestion:**
- Normalize case (e.g., title‑case or lower‑case mapping).
- Show “Did you mean …?” nearest matches on errors (optional).

Example:
```python
stations = {s.lower(): s for s in graph.keys()}
departure_in = input("Enter departure station: ").strip().lower()
if departure_in not in stations:
    print(f"Station '{departure_in}' not found. Available example: {next(iter(graph))}")
    return
departure = stations[departure_in]
```

---

## 3) CSV header handling
You always `next(reader)` to skip a header. That’s fine if a header exists, but if not, you’ll drop the first data row.

**Safer approach:** check the first row’s length/contents and only skip if it looks like a header, or try/except with a reset. Your numeric parsing with `try/except` already avoids bad rows, but be aware of this edge case.

---

## 4) Add argparse (non‑interactive usage)
This improves reproducibility and makes it scriptable:

```python
import argparse, sys
from pathlib import Path

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--from", dest="start", required=False, help="Departure station")
    p.add_argument("--to", dest="end", required=False, help="Destination station")
    p.add_argument("--mode", choices=["cheapest", "fastest"], default="cheapest")
    p.add_argument("--csv", default=str(Path(__file__).with_name("task1_3_data.csv")))
    return p.parse_args()

def main():
    args = parse_args()
    graph = load_graph(args.csv)
    start = args.start or input("Enter departure station: ").strip()
    end = args.end or input("Enter destination station: ").strip()
    mode = args.mode or input("Enter mode ('cheapest'...'fastest'): ").strip().lower()
    ...
```

---

## 5) Duplicate edges and data validation
If the CSV contains duplicates or multiple entries between the same two stations, you currently keep all copies and pick the **first match** during totals.

**Improvements:**
- On load, keep the **minimum cost/time** per (u, v).
- Validate non‑negative weights.

Example normalization on load:
```python
from collections import defaultdict
tmp = defaultdict(lambda: [float('inf'), float('inf')])  # (cost, time)
for (u, v, c, t) in rows:
    c0, t0 = tmp[(u, v)]
    tmp[(u, v)] = [min(c0, c), min(t0, t)]
# Then build graph from tmp
```

---

## 6) Reconstruct path guards
`reconstruct_path` assumes `previous[end]` exists through a chain. You already check `distances[destination] == inf` before reconstructing — good. Keep that guard in place.

---

## 7) Complexity & comments
Consider adding 1–2 lines in the docstring explaining Dijkstra’s complexity and that you’re using a binary heap (`heapq`) — helpful for assessors:
- Time: **O((V + E) log V)**
- Space: **O(V + E)**

---

## 8) Optional niceties
- **Arg validation:** print available stations count; maybe sample a few names on error.
- **Unit tests:** add a tiny graph and assert the cheapest/fastest routes and totals.
- **Requirements:** none (stdlib only). You can still add a `requirements.txt` with a comment to be explicit.

---

## TL;DR
- ✅ Core algorithm and structure: **Good**
- 🛡 Robustness: add path handling & input normalization
- 🧪 Reproducibility: add `argparse` flags
- 🧼 Data hygiene: deduplicate edges, validate weights

These upgrades make it production‑ish without changing the fundamental approach.
