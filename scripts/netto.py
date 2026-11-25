"""Calcolo del netto 2026 identico al calcolatore della home (index.html), nella versione
usata per le pagine statiche: minimo contrattuale, INPS 9,19%, addizionali medie
(regionale 1,73%, comunale 0,8%), nessun familiare a carico, nessun fondo.
Nessuna AI: solo aritmetica."""

SCAGLIONI = [(28000, 0.23), (50000, 0.33), (float("inf"), 0.43)]
INPS = 0.0919
ADD_REG, ADD_COM = 0.0173, 0.008
SOGLIA_IVS = 56224  # 1% aggiuntivo IVS oltre la prima fascia di retribuzione pensionabile 2026


def irpef_lorda(r):
    t, prev = 0.0, 0.0
    for lim, a in SCAGLIONI:
        if r > prev:
            t += (min(r, lim) - prev) * a
        prev = lim
    return t


def detr_lavoro(r):
    if r <= 15000:
        d = 1955
    elif r <= 28000:
        d = 1910 + 1190 * (28000 - r) / 13000
    elif r <= 50000:
        d = 1910 * (50000 - r) / 22000
    else:
        d = 0
    if 25000 < r <= 35000:
        d += 65
    return d


def ulteriore_cuneo(r):
    if r <= 20000 or r > 40000:
        return 0
    if r <= 32000:
        return 1000
    return 1000 * (40000 - r) / 8000


def bonus_cuneo(r, red_lav):
    if r > 20000:
        return 0
    p = 0.071 if r <= 8500 else (0.053 if r <= 15000 else 0.048)
    return red_lav * p


def tratt_integrativo(r, lorda, detrazioni):
    if r <= 15000:
        return 1200 if lorda > detrazioni - 75 else 0
    if r <= 28000:
        return max(0, min(1200, detrazioni - lorda))
    return 0


def annuo(ral):
    """Ritorna dict con i valori annui (arrotondati dal chiamante)."""
    inps = ral * INPS + max(0, ral - SOGLIA_IVS) * 0.01
    r = ral - inps
    lorda = irpef_lorda(r)
    dl, dc = detr_lavoro(r), ulteriore_cuneo(r)
    netta = max(0, lorda - dl - dc)
    bonus = bonus_cuneo(r, r)
    ti = tratt_integrativo(r, lorda, dl + dc)
    add = r * (ADD_REG + ADD_COM)
    netto = ral - inps - netta - add + bonus + ti
    return dict(ral=ral, inps=inps, r=r, lorda=lorda, dl=dl, dc=dc, netta=netta, bonus=bonus, ti=ti, add=add, netto=netto)


def mensile(minimo, mens):
    """Netto di una busta ordinaria: detrazioni su 12 mesi, addizionali a rate (reg /11, com saldo 70% /11, acconto 30% /9)."""
    ral = minimo * mens
    a = annuo(ral)
    inps_m = minimo * INPS
    imp_m = minimo - inps_m
    lorda_m = irpef_lorda(imp_m * 12) / 12
    detr_m = (a["dl"] + a["dc"]) / 12
    netta_m = max(0, lorda_m - detr_m)
    add_reg = a["r"] * ADD_REG
    add_com = a["r"] * ADD_COM
    net = (minimo - inps_m - netta_m - add_reg / 11 - add_com * 0.7 / 11 - add_com * 0.3 / 9
           + a["bonus"] / 12 + a["ti"] / 12)
    return net


def tredicesima(minimo):
    # come mensAgg() del calcolatore: nel mese la 13ª si somma alla busta e l'IVS 1% scatta oltre il rateo mensile della soglia
    sm = round(SOGLIA_IVS / 12)
    inps = minimo * INPS + max(0, 2 * minimo - sm) * 0.01 - max(0, minimo - sm) * 0.01
    imp = minimo - inps
    return minimo - inps - irpef_lorda(imp * 12) / 12
