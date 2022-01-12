
def sma(linedict, n, t, index=1):
    sum_of_prices = 0
    for i in range((t - n) + 1, t + 1):
        sum_of_prices += linedict[i][index]
    return sum_of_prices / n 

def double_sma(linedict, n1, n2, t, index=1):
    sum_of_avgs = 0
    for i in range((t - n2) + 1, t + 1):
        sum_of_avgs += sma(linedict, n1, i, index)
    return sum_of_avgs / n2 

def exponential_smoothing(linedict, sc, t, start_t, index=1):
    if t == start_t:
        return linedict[t][index]
    else:
        es_prev = exponential_smoothing(linedict, sc, t-1, start_t, index)
        return es_prev + (sc * (linedict[t][index] - es_prev))

def momentum_smoothing(linedict, sc, t, start_t, momentum_length, index=1):
    mom = linedict[t][index] - linedict[t-momentum_length][index]
    if t == start_t:
        return mom
    else:
        ms_prev = momentum_smoothing(linedict, sc, t-1, start_t, momentum_length, index)
        return ms_prev + (sc * (mom - ms_prev))

def double_es(linedict, first_sc, snd_sc, t, start_t, index=1):
    es = exponential_smoothing(linedict, first_sc, t, start_t, index)
    if t == start_t:
        return es 
    else:
        des = double_es(linedict, first_sc, snd_sc, t-1, start_t, index)
        return des + (snd_sc * (es - des))

def double_ms(linedict, first_sc, snd_sc, t, start_t, mom_length, index=1):
    ms = momentum_smoothing(linedict, first_sc, t, start_t, mom_length, index)
    if t == start_t:
        return ms 
    else:
        dms = double_ms(linedict, first_sc, snd_sc, t-1, start_t, mom_length, index)
        return dms + (snd_sc * (ms - dms))

def triple_es(linedict, first_sc, snd_sc, third_sc, t, start_t, index=1):
    des = double_es(linedict, first_sc, snd_sc, t, start_t, index)
    if t == start_t:
        return des 
    else:
        tes = triple_es(linedict, first_sc, snd_sc, third_sc, t-1, start_t, index)
        es = exponential_smoothing(linedict, first_sc, t-1, start_t, index)
        return tes + (third_sc * (des - es))
def trix(linedict, sc, t, start_t, index=1):
    et = triple_es(linedict, sc, sc, sc, t, start_t, index)
    et_prev = triple_es(linedict, sc, sc, sc,  t-1, start_t, index)
    e = exponential_smoothing(linedict, sc, t-1, start_t, index)
    return (et - et_prev) / e 
