# UK Railway Route Finder (Dijkstra’s Algorithm)

This project finds the **cheapest or fastest route** between UK railway stations using **Dijkstra’s shortest-path algorithm**.  
It reads a CSV of station connections (with **cost** and **time**), builds a weighted undirected graph, and outputs the optimal route, total cost, and total time.

---

## 🚉 Features
- Loads station connections from CSV (Departure, Destination, Cost, Time).
- Builds an **undirected** graph with two edge weights: *cost* and *time*.
- Runs **Dijkstra’s algorithm** minimizing either **cheapest** (cost) or **fastest** (time).
- Prints the full route + totals.

---

## 📦 Files
| File | Description |
|---|---|
| `task1_3.py` | Main program (loads CSV, runs Dijkstra, prints results) |
| `task1_3_data.csv` | Station connections and edge weights |
| `task1_3_UK_Railway_Map.pdf` | UK railway map for reference |

---

## 🧩 Data format (`task1_3_data.csv`)
CSV columns (header allowed):  
```
Departure,Destination,Cost,Time
Bristol,Swindon,15,40
Swindon,Reading,12,35
Reading,London,18,45
...
```
- **Cost** = ticket cost (float)  
- **Time** = minutes (float)  
- Graph is treated as **undirected** (edges added both ways).

---

## 🧪 How to run

> **Important:** In `task1_3.py`, the default path is `task1_3/task1_3_data.csv`.  
> If your CSV sits next to the script, either **move the CSV into a `task1_3/` folder** or **change the filename** line to `task1_3_data.csv`. See the “Notes” below.

### Option A — Run interactively
```bash
python3 task1_3.py
# Example prompts:
# Enter departure station: Bristol
# Enter destination station: London
# Enter mode ('cheapest' for lowest cost, 'fastest' for shortest time): fastest
```
**Example output**
```
Route found:
Bristol -> Swindon -> Reading -> London
Total cost: 45.0
Total time: 120.0 minutes
```

### Option B — (Recommended) Non‑interactive CLI (optional edit)
If you add `argparse` flags in the script (see CODE_REVIEW.md suggestions), you can do:
```bash
python3 task1_3.py --from "Bristol" --to "London" --mode fastest --csv task1_3_data.csv
```

---

## 🧠 How it works (Dijkstra overview)
1. **Load graph:** Parse CSV rows into adjacency lists: `graph[station] = [(neighbor, cost, time), ...]`  
2. **Choose weight:** `cost` for `cheapest`, `time` for `fastest`  
3. **Dijkstra:** Use a min‑heap (priority queue) to expand the cheapest/fastest frontier, storing `distances` and `previous` nodes  
4. **Reconstruct path:** Walk back from destination via `previous` to get full route  
5. **Summarize:** Accumulate total cost and time along the path

**Complexity:** O((V + E) log V) with a binary heap.

---

## 📁 Suggested repository layout
```
UK_Railway_Pathfinder/
├─ task1_3.py
├─ task1_3_data.csv
├─ task1_3_UK_Railway_Map.pdf
└─ README.md
```

---

## 📝 Notes & gotchas
- The script currently expects: `filename = "task1_3/task1_3_data.csv"`  
  - Either create a `task1_3/` folder and put the CSV inside it, **or** change that line to `filename = "task1_3_data.csv"`  
  - Even better (see review): compute the path relative to the script using `Path(__file__).with_name("task1_3_data.csv")`
- Station names are **case-sensitive** as written in the CSV. Use exact names or add a normalization step (see review).

---

## 📜 License
Academic assignment for the **Advanced Algorithms** module.  
© 2025 Adel Mansour
