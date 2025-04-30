# extremal_rays_z3_dedup.py
# ─ Requires: z3-solver ─

import itertools
from fractions import Fraction
from z3 import Real, RealVal, Solver, sat, unsat

def subsets(s):
    s = list(s)
    res = []
    for r in range(len(s)+1):
        for comb in itertools.combinations(s, r):
            res.append(set(comb))
    return res

def generate_basis(g, n):
    basis = [('a', None), ('b_irr', None)]
    full = set(range(1, n+1))
    for i in range(g+1):
        for I in subsets(full):
            if i == 0 and not I:       continue
            if i == g and   I == full: continue
            if i > g - i:              continue
            if i == g - i and sorted(I) > sorted(full - I):
                continue
            basis.append(('b', i, frozenset(I)))
    return basis

def vec_to_list(vdict, basis):
    return [vdict.get(b, 0) for b in basis]

def normalize_index(i, I):
    full = set(range(1,n+1))
    if i > g-i or ( i==g-i and sorted(I)>sorted(full-I) ): return g-i, full-I 
    return i,I

def generate_curves_and_ineq(g, n, basis):
    curves, ineq = [], {}
    full = set(range(1, n+1))

    # Type 1
    curves.append('F1')
    v1 = {('a',None):1, ('b_irr',None):-12, ('b',1,frozenset()):1}
    ineq['F1'] = vec_to_list(v1, basis)

    # Type 2
    #curves.append('F2')
    #ineq['F2'] = vec_to_list({('b_irr',None):1}, basis)

    # Type 3
    if g==2 and n>0:
        key = f"F3_{[0]}_{'_'.join(map(str,sorted(full)))}"
        curves.append(key)
        ineq[key] = vec_to_list({('b',0,frozenset(full)):1}, basis)
    elif g==3:
        key = f"F3_{[1]}_{'_'.join(map(str,sorted(full)))}"
        curves.append(key)
        ineq[key] = vec_to_list({('b',1,frozenset(full)):1}, basis)
    elif g==4 and n==0:
        key = f"F3_{[2]}_{'_'.join(map(str,sorted(full)))}"
        curves.append(key)
        ineq[key] = vec_to_list({('b',2,frozenset(full)):1}, basis)

    # Type 4
    for i in range(1, g):
        for I in subsets(full):
            if i==0 and not I:       continue
            if i > g-i:              continue
            if i==g-i and sorted(I)>sorted(full-I):
                continue
            key = f"F4_{[i]}_{'_'.join(map(str,sorted(I)))}"
            v = {('b_irr',None):2, ('b',i,frozenset(I)):-1}
            curves.append(key)
            ineq[key] = vec_to_list(v, basis)

    # Type 5
    cover5=set()
    for i in range(0, g):
        for j in range(0, g-i):
            for I in subsets(full):
                for J in subsets(full - I):
                    if i==0 and not I: continue
                    if j==0 and not J: continue
                    if i>j: continue
                    inner=frozenset( {(i, frozenset(I)), (j, frozenset(J)) } )
                    if inner in cover5:
                        continue
                    cover5.add(inner)
                    key = f"F5_{[i]}_{'_'.join(map(str,sorted(I)))}" \
                        f"_{[j]}_{'_'.join(map(str,sorted(J)))}"
                    a, A = normalize_index(i+j, I|J)
                    ii, II = normalize_index(i, I)
                    jj, JJ = normalize_index(j, J)
                    v = {}
                    v[('b', ii, frozenset(II))] = v.get(('b', ii, frozenset(II)), 0) + 1
                    v[('b', jj, frozenset(JJ))] = v.get(('b', jj, frozenset(JJ)), 0) + 1
                    v[('b', a, frozenset(A))] = v.get(('b', a, frozenset(A)), 0) - 1
                    curves.append(key)
                    ineq[key] = vec_to_list(v, basis)

    # Type 6
    covered=set()
    for i in range(g+1):
        for j in range(g+1-i):
            for k in range(g+1-i-j):
                l = g - i - j - k
                if i>j or j>k or k>l:
                    continue
                for assign in itertools.product(range(4), repeat=n):
                    parts = [set(),set(),set(),set()]
                    for idx, p in enumerate(assign):
                        parts[p].add(idx+1)
                    I,J,K,L = parts
                    inner =frozenset( {(i, frozenset(I)), (j, frozenset(J)), (k, frozenset(K)), (l, frozenset(L))})
                    if inner in covered:
                        continue
                    covered.add(inner)
                    if i==0 and not I: continue
                    if j==0 and not J: continue
                    if k==0 and not K: continue
                    if l==0 and not L: continue
                    key = f"F6_{[i]}_{'_'.join(map(str,sorted(I)))}" \
                          f"_{[j]}_{'_'.join(map(str,sorted(J)))}" \
                          f"_{[k]}_{'_'.join(map(str,sorted(K)))}" \
                          f"_{[l]}_{'_'.join(map(str,sorted(L)))}"
                    a, A = normalize_index(i+j, I|J)
                    b, B = normalize_index(i+k, I|K)
                    c, C = normalize_index(i+l, I|L)
                    i0, I0 = normalize_index(i, frozenset(I))
                    j0, J0 = normalize_index(j, frozenset(J))
                    k0, K0 = normalize_index(k, frozenset(K))
                    l0, L0 = normalize_index(l, frozenset(L))
                    v = {}
                    for (p, cnt) in [
                        (('b', i0, frozenset(I0)), 1),
                        (('b', j0, frozenset(J0)), 1),
                        (('b', k0, frozenset(K0)), 1),
                        (('b', l0, frozenset(L0)), 1),
                    ]:
                        v[p] = v.get(p, 0) + cnt
                    for (p, cnt) in [
                        (('b', a, frozenset(A)), -1),
                        (('b', b, frozenset(B)), -1),
                        (('b', c, frozenset(C)), -1),
                    ]:
                        v[p] = v.get(p, 0) + cnt
                    curves.append(key)
                    ineq[key] = vec_to_list(v, basis)

    return curves, ineq

def find_decomposition(v, generators):
    others = [u for u in generators if u != v]
    solver = Solver()
    alphas = []
    for i, u in enumerate(others):
        alpha = Real(f"α_{i}")
        solver.add(alpha >= 0)
        alphas.append((alpha, u))
    dim = len(v)
    for j in range(dim):
        expr = sum(alpha * RealVal(u[j]) for alpha, u in alphas)
        solver.add(expr == RealVal(v[j]))
    if solver.check() == sat:
        m = solver.model()
        combo = []
        for alpha, u in alphas:
            val = m[alpha]
            if val is not None and str(val) != "0":
                combo.append((str(val), u))
        return combo
    return None

def check_all_extremal2(basis, curves, ineq):
    vector_to_keys = {}
    for key, vec in ineq.items():
        t = tuple(vec)
        vector_to_keys.setdefault(t, []).append(key)

    generators = set(vector_to_keys.keys())

    for C in curves:
        v = tuple(ineq[C])
        combo = find_decomposition(v, generators)

        if combo is None:
            print(f"{C} is an extremal ray")
        else:
            print(f"{C} is NOT an extremal ray")
            terms = []
            for coeff, u in combo:
                keys = vector_to_keys[u]
                keys_str = "/".join(keys)
                terms.append(f"{coeff}*{keys_str}")
            print("  decomposition:", " + ".join(terms))

g, n = 4,2

basis = generate_basis(g,n)
curves, ineq = generate_curves_and_ineq(g, n, basis)
check_all_extremal2(basis, curves, ineq)
