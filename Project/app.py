"""Poset Quest – Streamlit GUI.  Run: streamlit run app.py"""
import random
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import relations as rl

st.set_page_config(page_title="Poset Quest", layout="wide")
st.title("🎯 Poset Quest — Relations, POSETs & Hasse Diagrams")


def draw_hasse(A, R, edges):
    lv = rl.levels(A, R)
    by = {}
    for a in A:
        by.setdefault(lv[a], []).append(a)
    pos = {}
    for l, items in by.items():
        for i, a in enumerate(items):
            pos[a] = ((i + 1) / (len(items) + 1), l)
    fig, ax = plt.subplots(figsize=(5, 4))
    for a, b in edges:
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], "k-", zorder=1)
    for a in A:
        ax.scatter(*pos[a], s=600, c="#cfe8ff", edgecolors="k", zorder=2)
        ax.text(*pos[a], a, ha="center", va="center", zorder=3)
    ax.axis("off")
    return fig


def show_matrix(A, M):
    st.dataframe(pd.DataFrame(M, index=A, columns=A))


def read_inputs(prefix):
    a_txt = st.text_input("Set A (comma separated)", "1,2,3,4,6,12", key=prefix + "A")
    r_txt = st.text_area("Relation R as pairs", "", key=prefix + "R",
                         placeholder="(1,1),(1,2),(2,4) …")
    use_div = st.checkbox("Auto-fill R = divisibility ('a divides b') on A", key=prefix + "div")
    A = rl.parse_set(a_txt)
    try:
        if use_div and all(x.lstrip("-").isdigit() for x in A):
            R = {(a, b) for a in A for b in A if int(a) != 0 and int(b) % int(a) == 0}
        else:
            R = rl.parse_pairs(r_txt, A)
    except ValueError as e:
        st.error(str(e))
        return A, None
    return A, R


t1, t2, t3, t4 = st.tabs(["1 Relation Lab", "2 Closures (Warshall)", "3 POSET & Hasse", "4 🎮 Game"])

with t1:
    A, R = read_inputs("t1")
    if R is not None and A:
        st.subheader("Matrix M_R")
        show_matrix(A, rl.matrix(A, R))
        st.subheader("Property tests (with witnesses)")
        for name, (ok, why) in rl.properties(A, R).items():
            with st.expander(("✅ " if ok else "❌ ") + name):
                for w in why:
                    st.write("• " + w)
        for k, v in rl.classify(A, R).items():
            st.write(f"**{k}:** {'Yes' if v else 'No'}")

with t2:
    A, R = read_inputs("t2")
    if R is not None and A:
        st.write("Reflexive closure:", sorted(rl.reflexive_closure(A, R)))
        st.write("Symmetric closure:", sorted(rl.symmetric_closure(A, R)))
        st.subheader("Warshall's algorithm – step by step")
        for label, M in rl.warshall(A, R):
            st.caption(label)
            show_matrix(A, M)
        st.write("Transitive closure:", sorted(rl.transitive_closure(A, R)))

with t3:
    A, R = read_inputs("t3")
    if R is not None and A:
        if not rl.is_poset(A, R):
            st.warning("R is not a partial order — see tab 1 for failing property.")
        else:
            edges = rl.hasse_edges(A, R)
            c1, c2 = st.columns(2)
            with c1:
                st.pyplot(draw_hasse(A, R, edges))
                st.write("Covering pairs (Hasse edges):", edges)
            with c2:
                for k, v in rl.extremal(A, R).items():
                    st.write(f"**{k}:** {v or 'none'}")
                ok, rows, fail = rl.lattice_check(A, R)
                st.write(f"**Lattice:** {'Yes' if ok else f'No – pair {fail} lacks lub or glb'}")
                st.dataframe(pd.DataFrame(rows, columns=["a", "b", "lub", "glb"]))

with t4:
    ss = st.session_state
    if "level" not in ss:
        ss.level, ss.score, ss.hints = 1, 0, 0
        ss.A, ss.R = rl.random_divisibility_poset(4)
    st.write(f"**Level {ss.level}** | **Score {ss.score}**")
    st.info("Divisibility poset on A = %s. Select exactly the edges of its Hasse diagram "
            "(covering pairs a → b)." % ss.A)
    strict = sorted((a, b) for a, b in ss.R if a != b)
    labels = [f"{a} → {b}" for a, b in strict]
    pick = st.multiselect("Hasse edges", labels)
    if st.button("💡 Hint (−3 pts)"):
        ss.score -= 3
        st.write("Hint: (a,b) is a cover iff no c with a|c and c|b, c∉{a,b}. "
                 "Number of edges =", len(rl.hasse_edges(ss.A, ss.R)))
    if st.button("Submit"):
        truth = {f"{a} → {b}" for a, b in rl.hasse_edges(ss.A, ss.R)}
        chosen = set(pick)
        if chosen == truth:
            ss.score += 10 * ss.level
            ss.level += 1
            st.success("Correct! Next level.")
            ss.A, ss.R = rl.random_divisibility_poset(min(3 + ss.level, 9))
            st.rerun()
        else:
            ss.score -= 2
            st.error(f"Wrong. Missing: {sorted(truth - chosen)} | Extra: {sorted(chosen - truth)}")
            st.caption("Remember: transitive edges (e.g. 1→4 when 1→2→4) are NOT drawn.")
    if st.button("Reveal solution"):
        st.pyplot(draw_hasse(ss.A, ss.R, rl.hasse_edges(ss.A, ss.R)))
    if st.button("Restart game"):
        for k in ["level", "score", "hints", "A", "R"]:
            ss.pop(k, None)
        st.rerun()
