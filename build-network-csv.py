#!/usr/bin/env python3
"""
Emit the network scorecard as a single-tab CSV.

Google Drive converts an uploaded CSV into a real Sheet, and cells beginning
with "=" become live formulas -- so this is the way to hand over a working
Sheet link when the rig's OAuth token is dead.

A CSV is one tab, so the rubric and readout stack below the scoring rows
instead of living on their own sheets. Weights sit in F:J directly beneath the
score columns they belong to, which keeps the fit formula short and makes the
weighting self-documenting.
"""

import csv
import io

from importlib.machinery import SourceFileLoader

src = SourceFileLoader("nw", __file__.replace("build-network-csv.py",
                                              "build-network-sheet.py")).load_module()

HEADERS, CRITERIA = src.HEADERS, src.CRITERIA
SEGMENTS, WOULD_BUY = src.SEGMENTS, src.WOULD_BUY
TIER_A, TIER_B, TIER_C = src.TIER_A, src.TIER_B, src.TIER_C

# Pre-filled scoring rows. Kept small because this CSV has to be transcribed
# into the Drive upload by hand; select K:L and drag down for more people.
SCORE_ROWS = 25


def build():
    rows = []
    W = 18

    def pad(r):
        return list(r) + [""] * (W - len(r))

    rows.append(pad(["bedofrice — who would actually buy this?"]))
    rows.append(pad(["Score each person 1-5 in columns F-J. Fit score and Tier "
                     "fill themselves in. Need more rows? Select K:L on the last "
                     "row and drag down. Rubric and readout are below."]))
    rows.append(pad([]))

    header_row = len(rows) + 1          # 4
    rows.append(pad(HEADERS))

    first = len(rows) + 1               # 5
    last = first + SCORE_ROWS - 1       # 44

    # Weights live in F:J of the rubric block, directly under the score
    # columns, so SUMPRODUCT lines up without transposing anything.
    weights_row = last + 4              # blank, RUBRIC heading, then weights

    for r in range(first, last + 1):
        fit = (f'=IF(COUNT(F{r}:J{r})<5,"",'
               f'ROUND(SUMPRODUCT(F{r}:J{r},$F${weights_row}:$J${weights_row})/5*100,0))')
        tier = (f'=IF(K{r}="","",IF(K{r}>=75,"{TIER_A}",'
                f'IF(K{r}>=55,"{TIER_B}","{TIER_C}")))')
        rows.append(pad([""] * 10 + [fit, tier]))

    rows.append(pad([]))                                        # last+1
    rows.append(pad(["RUBRIC — what the scores mean"]))         # last+2
    rows.append(pad(["Criterion", "", "", "", "", "Kids", "Rice culture",
                     "Design taste", "Spend", "Reach"]))        # last+3
    rows.append(pad(["Weights (editable — change these and every score updates)",
                     "", "", "", ""] + [w for _n, w, _a, _b, _c in CRITERIA]))
    assert len(rows) == weights_row, (len(rows), weights_row)

    rows.append(pad([]))
    rows.append(pad(["Criterion", "Weight", "Score 5", "Score 3", "Score 1"]))
    for name, w, a5, a3, a1 in CRITERIA:
        rows.append(pad([name, w, a5, a3, a1]))

    rows.append(pad([]))
    rows.append(pad(["TIER BANDS"]))
    rows.append(pad([TIER_A, "75-100",
                     "Interview these first. Closest thing to the real customer."]))
    rows.append(pad([TIER_B, "55-74",
                     "Would probably buy, but not proof of a market on their own."]))
    rows.append(pad([TIER_C, "under 55",
                     "Useful as a control. If C-tier people want it, the market is wider than you think."]))

    rows.append(pad([]))
    rows.append(pad(["WHAT IS BEING TESTED"]))
    rows.append(pad(["Positioning", "Culture-first: a love letter to the world's most-eaten food. Not character-first cute."]))
    rows.append(pad(["Flagship", "Plush / throw pillow, Squishmallow-adjacent. Kids are the ones who love it. Under $100."]))
    rows.append(pad(["Entry product", "Stickers stay in the line as the cheap way in. Score people on the flagship; the 'Would buy' column records which they'd actually buy."]))
    rows.append(pad(["Audiences", "All three: kawaii/stationery collectors, food-culture people, diaspora 'rice is home'."]))
    rows.append(pad(["Watch for", "Buyer and user are different people. An adult pays, a child hugs it. A high score with no child in their life is a gift-buyer, not a household customer."]))
    rows.append(pad(["Also watch for", "Lots of 'Stickers only' is a real answer, not a failure. It means the brand works and $100 is the wrong first product."]))
    rows.append(pad(["Be honest", "Score people as they are, not as you hope. A sheet of generous 4s tells you nothing you didn't already believe."]))

    rows.append(pad([]))
    rows.append(pad(["READOUT — updates itself as you fill rows in"]))
    K = f"K{first}:K{last}"
    L = f"L{first}:L{last}"
    M = f"M{first}:M{last}"
    N = f"N{first}:N{last}"
    O = f"O{first}:O{last}"
    rows.append(pad(["People scored", f'=COUNTIF({K},">=0")']))
    rows.append(pad(["Average fit score", f'=IFERROR(ROUND(AVERAGE({K}),0),"-")']))
    rows.append(pad(["Average price they would pay",
                     f'=IFERROR(ROUND(AVERAGE({N}),0),"-")']))
    rows.append(pad([]))
    rows.append(pad(["By tier", "Count"]))
    for t in (TIER_A, TIER_B, TIER_C):
        rows.append(pad([t, f'=COUNTIF({L},"{t[0]}*")']))
    rows.append(pad([]))
    rows.append(pad(["By segment", "Count", "Avg fit", "Avg would-pay"]))
    for seg in SEGMENTS:
        rows.append(pad([seg, f'=COUNTIF({M},"{seg}")',
                         f'=IFERROR(ROUND(AVERAGEIF({M},"{seg}",{K}),0),"-")',
                         f'=IFERROR(ROUND(AVERAGEIF({M},"{seg}",{N}),0),"-")']))
    rows.append(pad([]))
    rows.append(pad(["Flagship vs entry product", "Count"]))
    for wb in WOULD_BUY:
        rows.append(pad([wb, f'=COUNTIF({O},"{wb}")']))
    rows.append(pad([]))
    rows.append(pad(["Which criterion drives fit?", "Avg score"]))
    for i, (name, _w, _a, _b, _c) in enumerate(CRITERIA):
        c = chr(ord("F") + i)
        rows.append(pad([name, f'=IFERROR(ROUND(AVERAGE({c}{first}:{c}{last}),1),"-")']))
    rows.append(pad([]))
    rows.append(pad(["Kids signal check", ""]))
    F = f"F{first}:F{last}"
    rows.append(pad(["Scored 4-5 on kids", f'=COUNTIF({F},">=4")']))
    rows.append(pad(["...of those, tier A", f'=COUNTIFS({F},">=4",{L},"A*")']))
    rows.append(pad(["Tier A with NO kids (gift-buyers)",
                     f'=COUNTIFS({F},"<=2",{L},"A*")']))

    return rows, header_row, first, last, weights_row


if __name__ == "__main__":
    rows, header_row, first, last, wrow = build()
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows(rows)
    text = buf.getvalue()

    path = __file__.replace("build-network-csv.py", "bedofrice-network-scorecard.csv")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)

    print(f"header row {header_row}, scoring rows {first}-{last}, weights row {wrow}")
    print(f"{len(rows)} rows, {len(text)} chars, ~{len(text)//4} tokens")
    print("wrote:", path)
