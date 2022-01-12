"""A module for the Commodities Channel Index indicator"""

def p_at_t(linedict, t, high_index, low_index, close_index):
    """helper function"""
    h = float(linedict[t][high_index])
    l = float(linedict[t][low_index])
    c = float(linedict[t][close_index])
    m = (h + l + c) / 3
    return m

def adp_at_t(linedict, n, t, hi, li, ci):
    """helper function"""
    s = 0
    for i in range((t - n) + 1, t + 1):
        s += p_at_t(linedict, i, hi, li, ci)
    adp = s / n 
    return adp 

def avg_dev_at_t(linedict, n, t, hi, li, ci):
    """helper function"""
    s = 0
    adp = adp_at_t(linedict, n, t, hi, li, ci)
    for i in range((t - n) + 1, t + 1):
        m = p_at_t(linedict, i, hi, li, ci)
        s += abs(m - adp)
    avg_dev = s / n 
    return avg_dev 

def cci_at_t(linedict : dict[int, list[str]], n : int, t : int, hi=2, li=3, ci=4):
    """Gets the cci at time t, given an indexed set of lines of data, the period n, and the indices of high low and close. Make sure you have at least n pieces of data before t"""
    num = p_at_t(linedict, t, hi, li, ci) - adp_at_t(linedict, n, t, hi, li, ci)
    denom = 0.015 * avg_dev_at_t(linedict, n, t, hi, li, ci)
    return (num / denom)
