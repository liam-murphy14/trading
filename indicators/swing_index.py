"""***BROKEN*** A module for the Swing Index indicator"""

def si(linedict, t, hi, li, ci, oi):
    h = float(linedict[t][hi])
    l = float(linedict[t][li])
    c = float(linedict[t][ci])
    o = float(linedict[t][oi])
    hp = float(linedict[t - 1][hi])
    lp = float(linedict[t - 1][li])
    cp = float(linedict[t - 1][ci])
    op = float(linedict[t - 1][oi])
    k = max(hp - c, lp - c)
    a = h - cp
    b = l - cp
    c = h - l
    r = 0.0
    m = h - l
    if max(a, b, c) == a:
        r = a - (0.5 * b) + (0.25 * (cp - op))
    elif max(a, b, c) == b:
        r = b - (0.5 * a) + (0.25 * (cp - op))
    else:
        r = (h - l) + (0.25 * (cp - op))
    if r == 0.0:
        r = 0.1
    if m == 0.0:
        m = 0.1
    si = 50 * (((c - cp) + (0.5 * (cp - op)) + (0.25 * (c - o))) / r) * (k / m) 
    return si

def asi(linedict, t, hi, li, ci, oi):
    if t < 1:
        return 0
    else:
        return si(linedict, t, hi, li, ci, oi) + asi(linedict, t - 1, hi, li, ci, oi)