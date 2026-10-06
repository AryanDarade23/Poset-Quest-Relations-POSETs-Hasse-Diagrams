# Work Plan (all tasks)
**Phase 1 – Registration (Day 1):** form team of 3–4, choose Unit III + Track A/B, register. Pick team ID.
**Phase 2 – Architecture (Days 2–3):** draw flowchart + UI wireframes; agree module split.
**Phase 3 – Development (Days 4–10):**
- Member 1: `relations.py` property tests, closures + unit tests
- Member 2: POSET/lattice functions (hasse, lub, glb)
- Member 3: Streamlit UI tabs 1–3, matrix display
- Member 4: Game tab, scoring, README, screenshots
Test edge cases: empty relation, single element, non-poset input, malformed pairs.
**Phase 4 – Submission:** public GitHub repo (code, tests, screenshots in `docs/`, README); 2-page PDF; rehearse viva; each member must explain their own module.
**Make it yours:** plagiarism checks run on all submissions — rename functions, change game rules/theme/scoring, add one extra feature (e.g. functions: injective/surjective checker, or Cayley-table tab).

# 2-Page Report Template
1. **Title, names, roll numbers, Team ID**
2. **Unit & Formulation:** Unit III. A relation R ⊆ A×A is a set of pairs; M_R[i][j]=1 iff (aᵢ,aⱼ)∈R. State the five property definitions, Warshall recurrence, Hasse-cover definition, lattice definition (formulas above).
3. **Architecture diagram:** `User input → parser (parse_set/parse_pairs) → relations.py (properties, warshall, hasse, lattice) → Streamlit tabs → matrix/diagram/game score`. Add 3–4 screenshots (tabs 1, 2, 3, 4).
4. **Contribution table:** member | role | modules | % contribution.

# Viva questions to prepare
- Why is Hasse edge removal of transitive/reflexive pairs valid? - Complexity of Warshall (O(n³))? - Divisibility on {1,2,3} – lattice? Why not? - Difference between minimal and least element? - Antisymmetric vs not symmetric?
