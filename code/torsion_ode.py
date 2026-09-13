"""Generalised torsion equation over 5 ship sections of length L = 20 m,
constant torque M_t:  G Ip theta' - E Iw theta''' = M_t  in every section.
theta'(x) = Mt/(G Ip) + C1 cosh(lam x) + C2 sinh(lam x);  theta = integral + C3.
Boundary conditions: aft end theta = 0, theta'' = 0 (free warping);
bulkheads theta' = 0 on both sides and theta continuous; bow end theta'' = 0."""
import numpy as np
E, G, Mt, L = 205e9, 79e9, 100e6, 20.0
Ip = dict(A=6.72, B1=1.05, B2=0.86, BU=8.71e-4, BUH=7.83, C=6.05)
Iw = dict(A=4.45, B1=23.6, B2=25.7, BU=22.6, BUH=2.71, C=4.00)

def solve_ship(Bkey, n=401):
    secs = ['A', Bkey, Bkey, Bkey, 'C']
    lam = [np.sqrt(G*Ip[s]/(E*Iw[s])) for s in secs]
    k0 = [Mt/(G*Ip[s]) for s in secs]
    rows, rhs = [], []
    def thp(i, x):   # theta' = k0 + C1 cosh + C2 sinh  -> (coefficients, constant)
        r = np.zeros(15); r[3*i] = np.cosh(lam[i]*x); r[3*i+1] = np.sinh(lam[i]*x); return r, k0[i]
    def thpp(i, x):  # theta'' = lam (C1 sinh + C2 cosh)
        r = np.zeros(15); r[3*i] = lam[i]*np.sinh(lam[i]*x); r[3*i+1] = lam[i]*np.cosh(lam[i]*x); return r, 0.0
    def th(i, x):    # theta = k0 x + C1 sinh/lam + C2 (cosh-1)/lam + C3
        r = np.zeros(15); r[3*i] = np.sinh(lam[i]*x)/lam[i]
        r[3*i+1] = (np.cosh(lam[i]*x)-1)/lam[i]; r[3*i+2] = 1.0; return r, k0[i]*x
    def add(r, c, value=0.0):   # r.C + c = value
        rows.append(r); rhs.append(value - c)
    add(*th(0, 0.0)); add(*thpp(0, 0.0))
    for i in range(4):
        add(*thp(i, L)); add(*thp(i+1, 0.0))
        r1, c1 = th(i, L); r2, c2 = th(i+1, 0.0); add(r1-r2, c1-c2)
    add(*thpp(4, L))
    C = np.linalg.solve(np.array(rows), np.array(rhs))
    out = {k: [] for k in ('x', 'th', 'thp', 'thpp', 'thppp')}
    for i in range(5):
        x = np.linspace(0, L, n); c1, c2, c3 = C[3*i:3*i+3]; l = lam[i]
        out['x'].append(x + i*L)
        out['thp'].append(k0[i] + c1*np.cosh(l*x) + c2*np.sinh(l*x))
        out['th'].append(k0[i]*x + c1*np.sinh(l*x)/l + c2*(np.cosh(l*x)-1)/l + c3)
        out['thpp'].append(l*(c1*np.sinh(l*x) + c2*np.cosh(l*x)))
        out['thppp'].append(l*l*(c1*np.cosh(l*x) + c2*np.sinh(l*x)))
    return {k: np.concatenate(v) for k, v in out.items()}

if __name__ == "__main__":
    for key in ('B1', 'B2', 'BU', 'BUH'):
        s = solve_ship(key)
        print(key, "total twist %.3f deg, max theta' %.3f mrad/m" %
              (np.degrees(s['th'][-1]), 1e3*np.max(np.abs(s['thp']))))
