# Poset Quest — Discrete Mathematics (7MA206) ISE-2
Unit III: Relations, POSETs & Functions | Track A (game) + Track B (tool)

## Features
1. **Relation Lab** – arbitrary set/relation input, matrix, reflexive/irreflexive/symmetric/antisymmetric/transitive tests with counter-example witnesses, equivalence/POSET classification.
2. **Closures** – reflexive, symmetric, transitive closure; Warshall's algorithm matrix at every step.
3. **POSET & Hasse** – covering relation, Hasse diagram, minimal/maximal/least/greatest, lub/glb table, lattice test.
4. **Game** – identify the Hasse edges of random divisibility posets; levels grow in size, scoring with hints/penalties.

## Setup
```bash
pip install -r requirements.txt
streamlit run app.py
pytest tests/
```
## Structure
`relations.py` (math, no UI) · `app.py` (GUI) · `tests/` · `docs/` (screenshots, report)

## Math summary
- Hasse edge (a,b): a<b and no c with a<c<b.
- Warshall: W_k[i][j] = W_{k-1}[i][j] ∨ (W_{k-1}[i][k] ∧ W_{k-1}[k][j]).
- Lattice: every pair has lub and glb.

## Team
| Name | Roll | Role |
|---|---|---|
