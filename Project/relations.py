"""Pure-math core for Poset Quest (Unit III). No UI code here."""
import re
import random

PAIR_RE = re.compile(r"\(\s*([^,()]+?)\s*,\s*([^,()]+?)\s*\)")


def _key(x):
    return (0, int(x), "") if x.lstrip("-").isdigit() else (1, 0, x)


def parse_set(text):
    return sorted({x.strip() for x in text.split(",") if x.strip()}, key=_key)


def parse_pairs(text, A):
    R = set()
    for a, b in PAIR_RE.findall(text):
        if a not in A or b not in A:
            raise ValueError(f"Pair ({a},{b}) uses an element not in A")
        R.add((a, b))
    return R


def matrix(A, R):
    return [[1 if (a, b) in R else 0 for b in A] for a in A]


def properties(A, R):
    """Return {property: (holds, [witness/explanation lines])}."""
    out = {}
    miss = [(a, a) for a in A if (a, a) not in R]
    out["Reflexive"] = (not miss, [f"Missing {p}" for p in miss] or ["All (a,a) present"])
    loops = [(a, a) for a in A if (a, a) in R]
    out["Irreflexive"] = (not loops, [f"Has loop {p}" for p in loops] or ["No (a,a) present"])
    bad = [(a, b) for a, b in R if (b, a) not in R]
    out["Symmetric"] = (not bad, [f"{p} in R but ({p[1]},{p[0]}) not" for p in bad] or ["Every (a,b) has (b,a)"])
    bad = [(a, b) for a, b in R if a != b and (b, a) in R]
    out["Antisymmetric"] = (not bad, [f"{p} and ({p[1]},{p[0]}) both in R, a≠b" for p in bad] or ["No distinct a,b with both aRb and bRa"])
    bad = [(a, b, c) for a, b in R for b2, c in R if b == b2 and (a, c) not in R]
    out["Transitive"] = (not bad, [f"({a},{b}),({b},{c}) in R but ({a},{c}) not" for a, b, c in bad] or ["aRb ∧ bRc ⇒ aRc always"])
    return out


def classify(A, R):
    p = {k: v[0] for k, v in properties(A, R).items()}
    return {
        "Equivalence relation": p["Reflexive"] and p["Symmetric"] and p["Transitive"],
        "Partial order (POSET)": p["Reflexive"] and p["Antisymmetric"] and p["Transitive"],
    }


def reflexive_closure(A, R):
    return set(R) | {(a, a) for a in A}


def symmetric_closure(A, R):
    return set(R) | {(b, a) for a, b in R}


def warshall(A, R):
    """Return list of (label, matrix) – one matrix per Warshall step."""
    n = len(A)
    M = matrix(A, R)
    steps = [("W0 = M_R", [r[:] for r in M])]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if M[i][k] and M[k][j]:
                    M[i][j] = 1
        steps.append((f"W{k+1}: allow '{A[k]}' as intermediate vertex", [r[:] for r in M]))
    return steps


def transitive_closure(A, R):
    M = warshall(A, R)[-1][1]
    return {(A[i], A[j]) for i in range(len(A)) for j in range(len(A)) if M[i][j]}


# ---------- POSET tools ----------
def is_poset(A, R):
    return classify(A, R)["Partial order (POSET)"]


def hasse_edges(A, R):
    strict = {(a, b) for a, b in R if a != b}
    return sorted(
        ((a, b) for a, b in strict
         if not any((a, c) in strict and (c, b) in strict for c in A)),
        key=lambda e: (_key(e[0]), _key(e[1])))


def levels(A, R):
    strict = {(a, b) for a, b in R if a != b}
    memo = {}

    def lv(x):
        if x not in memo:
            preds = [a for a, b in strict if b == x]
            memo[x] = 0 if not preds else 1 + max(lv(p) for p in preds)
        return memo[x]
    return {a: lv(a) for a in A}


def extremal(A, R):
    minimal = [a for a in A if not any(x != a and (x, a) in R for x in A)]
    maximal = [a for a in A if not any(x != a and (a, x) in R for x in A)]
    least = [a for a in A if all((a, x) in R for x in A)]
    greatest = [a for a in A if all((x, a) in R for x in A)]
    return {"Minimal": minimal, "Maximal": maximal, "Least": least, "Greatest": greatest}


def lub(A, R, a, b):
    ub = [u for u in A if (a, u) in R and (b, u) in R]
    least = [u for u in ub if all((u, v) in R for v in ub)]
    return least[0] if least else None


def glb(A, R, a, b):
    lb = [l for l in A if (l, a) in R and (l, b) in R]
    greatest = [l for l in lb if all((v, l) in R for v in lb)]
    return greatest[0] if greatest else None


def lattice_check(A, R):
    """Return (is_lattice, table rows [(a,b,lub,glb)], first failing pair or None)."""
    rows, fail = [], None
    for i, a in enumerate(A):
        for b in A[i:]:
            l, g = lub(A, R, a, b), glb(A, R, a, b)
            rows.append((a, b, l, g))
            if (l is None or g is None) and fail is None:
                fail = (a, b)
    return fail is None, rows, fail


# ---------- Game ----------
def random_divisibility_poset(n, rng=None):
    rng = rng or random
    A = sorted(rng.sample(range(1, 31), n))
    A = [str(x) for x in A]
    R = {(a, b) for a in A for b in A if int(b) % int(a) == 0}
    return A, R
