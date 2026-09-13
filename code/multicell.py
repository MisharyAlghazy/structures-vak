"""Multi-cell thin-walled torsion (Bredt-Batho).  Units: a (or b) = 1, t_p = 1.
nodes : {name: (y, z)}
walls : {name: (node1, node2, thickness, length or None)}
cells : [(list of node names, counter-clockwise), extra_area]
Solves  sum_w s_iw q_w L_w/t_w = 2 A_i (G theta')  for every cell i,
with q_w the net wall flow, then I_p = sum 2 A_i q_i  (per unit G theta')."""
import numpy as np

def solve(nodes, walls, cells, open_parts=()):
    wl = {}
    for wn, (n1, n2, t, L) in walls.items():
        if L is None:
            L = float(np.linalg.norm(np.subtract(nodes[n2], nodes[n1])))
        wl[frozenset((n1, n2))] = (wn, n1, n2, t, L)
    areas, cellwalls = [], []
    for poly, extra in cells:
        p = np.array([nodes[n] for n in poly]); y, z = p[:, 0], p[:, 1]
        areas.append(0.5*np.sum(y*np.roll(z, -1) - np.roll(y, -1)*z) + extra)
        cw = []
        for i in range(len(poly)):
            n1, n2 = poly[i], poly[(i+1) % len(poly)]
            wn, w1, w2, t, L = wl[frozenset((n1, n2))]
            cw.append((wn, 1 if (w1, w2) == (n1, n2) else -1, t, L))
        cellwalls.append(cw)
    n = len(cells); M = np.zeros((n, n)); rhs = 2*np.array(areas)
    for i, cwi in enumerate(cellwalls):
        for wn, s, t, L in cwi:
            for j, cwj in enumerate(cellwalls):
                for wn2, s2, _, _ in cwj:
                    if wn2 == wn:
                        M[i, j] += s*s2*L/t
    q = np.linalg.solve(M, rhs)                 # cell flows per unit G theta'
    Ip_closed = float(np.sum(2*np.array(areas)*q))
    Ip_open = sum(L*t**3/3 for L, t in open_parts)
    flow = {}                                   # net wall flow per unit M_t
    for wn in walls:
        qs = sum(s2*q[j] for j, cwj in enumerate(cellwalls) for wn2, s2, _, _ in cwj if wn2 == wn)
        flow[wn] = (qs/Ip_closed, walls[wn][2], qs/Ip_closed/walls[wn][2])
    return dict(q=q, areas=areas, Ip_closed=Ip_closed, Ip_open=Ip_open, flow=flow)

if __name__ == "__main__":
    # Example: design B2, starboard half (mirror gives the port half); a = t_p = 1
    N = {'B0': (0, 0), 'IB0': (0, 1), 'B1': (1, 0), 'IB1': (1, 1), 'B25': (2.5, 0),
         'IB25': (2.5, 1), 'B4': (4, 0), 'S1': (4, 1), 'S3': (4, 3), 'S5': (4, 5),
         'BH3': (2.5, 3), 'BH5': (2.5, 5)}
    # centre girder: net flow 0 by symmetry -> effectively no L/t term (thickness -> inf)
    W = {'CG': ('B0', 'IB0', 1e9, None), 'b01': ('B0', 'B1', 3, None), 'b125': ('B1', 'B25', 3, None),
         'b254': ('B25', 'B4', 2, None), 'ss01': ('B4', 'S1', 2, None), 'ib01': ('IB0', 'IB1', 3, None),
         'ib125': ('IB1', 'IB25', 3, None), 'ib254': ('IB25', 'S1', 3, None), 'G1': ('B1', 'IB1', 3, None),
         'bh01': ('B25', 'IB25', 1, None), 'bh13': ('IB25', 'BH3', 1, None), 'bh35': ('BH3', 'BH5', 1, None),
         'ss13': ('S1', 'S3', 2, None), 'ss35': ('S3', 'S5', 2, None), 'str': ('BH3', 'S3', 1, None),
         'dk': ('BH5', 'S5', 3, None)}
    C = [(['B0', 'B1', 'IB1', 'IB0'], 0), (['B1', 'B25', 'IB25', 'IB1'], 0), (['B25', 'B4', 'S1', 'IB25'], 0),
         (['IB25', 'S1', 'S3', 'BH3'], 0), (['BH3', 'S3', 'S5', 'BH5'], 0)]
    r = solve(N, W, C)
    print("I_p full section =", 2*r['Ip_closed'], "a^3 t_p ; cell flows per unit G theta':", r['q'])
