#!/usr/bin/env python3
"""
Build the bedofrice network-scoring spreadsheet.

Purpose: work out who the real buyer is for a culture-first rice-character
plush under $100, by scoring actual people Charles knows instead of inventing
a persona. For a kids' product the buyer and the user are different people, so
the rubric scores whether there is a child in their life AND whether the adult
would actually spend.

    python build-network-sheet.py            # writes the .xlsx (works offline)
    python build-network-sheet.py --gsheet   # creates it in Google Sheets

The .xlsx opens directly in Google Sheets (upload to Drive, open with Sheets)
and keeps its formulas, dropdowns and conditional formatting. The --gsheet path
needs a live token.json; as of 2026-08-01 the rig's token is revoked.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TOKEN = os.path.join(ROOT, "token.json")

TITLE = "bedofrice — Who would actually buy this?"
OUT_XLSX = os.path.join(HERE, "bedofrice-network-scorecard.xlsx")

ROWS = 200

# Weight per criterion. Kids leads because Charles called it the most important
# signal; rice culture next because it is the brand's entire premise.
CRITERIA = [
    ("1. Kids in their life", 0.30,
     "Own kids roughly 2-8 — the plush-hugging years",
     "Kids 9-12, or a niece/nephew/godchild they buy for often",
     "No children in their orbit at all"),
    ("2. Rice-culture resonance", 0.25,
     "Rice is a daily staple AND they are vocal about food heritage",
     "Rice-centric home cuisine, but not something they talk about",
     "No particular connection to rice as a food culture"),
    ("3. Design / kawaii taste", 0.20,
     "Owns Sanrio / Squishmallow / indie design objects; follows design brands",
     "Appreciates good design, buys occasionally",
     "Indifferent to design objects"),
    ("4. Spend behaviour", 0.15,
     "Has bought a $50-100 plush or gift online in the last year",
     "Buys online from indie brands, but at lower price points",
     "Price-sensitive, or never buys this category"),
    ("5. Reach / advocacy", 0.10,
     "Would post it to a real audience, or buys in multiples as gifts",
     "Would mention it to a few friends",
     "Private buyer, one for themselves at most"),
]

HEADERS = [
    "Name", "Relationship", "Where they live", "Heritage / home cuisine",
    "Kids in their life (ages)",
    "1. Kids (30%)", "2. Rice culture (25%)", "3. Design taste (20%)",
    "4. Spend (15%)", "5. Reach (10%)",
    "Fit score", "Tier", "Primary segment", "Would pay ($)",
    "Would buy", "Asked?", "What they said", "Notes",
]

RELATIONSHIPS = ["Family", "Close friend", "Friend", "Colleague", "Acquaintance"]
SEGMENTS = ["Kids / parents", "Diaspora / food culture", "Design / kawaii", "Blend"]
ASKED = ["Not yet", "Asked", "Replied", "Bought"]
# Stickers stay in the line as the cheap entry product; the plush is the
# flagship. Separating them is the point -- someone who buys stickers but not a
# pillow validates the brand without validating the flagship.
WOULD_BUY = ["Plush (flagship)", "Stickers only", "Both", "Neither", "Unknown"]

TIER_A, TIER_B, TIER_C = "A - ask first", "B - likely", "C - unlikely"


def fit_formula(r):
    # Weights live in Rubric!B5:B9 -- row 4 is that table's header.
    return (f'=IF(COUNT(F{r}:J{r})<5,"",'
            f'ROUND((F{r}*Rubric!$B$5+G{r}*Rubric!$B$6+H{r}*Rubric!$B$7'
            f'+I{r}*Rubric!$B$8+J{r}*Rubric!$B$9)/5*100,0))')


def tier_formula(r):
    return (f'=IF(K{r}="","",IF(K{r}>=75,"{TIER_A}",'
            f'IF(K{r}>=55,"{TIER_B}","{TIER_C}")))')


def rubric_rows():
    rows = [
        ["bedofrice — scoring rubric", "", "", "", ""],
        ["Score each person 1-5 on the five criteria in the Network tab. The "
         "anchors below describe 5, 3 and 1 — use 2 and 4 for in-between. "
         "Weights are editable: change column B and every Fit score updates.",
         "", "", "", ""],
        ["", "", "", "", ""],
        ["Criterion", "Weight", "Score 5", "Score 3", "Score 1"],
    ]
    for name, w, a5, a3, a1 in CRITERIA:
        rows.append([name, w, a5, a3, a1])
    rows += [
        ["Total", "=SUM(B5:B9)", "must equal 100%", "", ""],
        ["", "", "", "", ""],
        ["Tier bands", "", "", "", ""],
        [TIER_A, "75-100", "Interview these first. Closest thing you have to "
         "the real customer.", "", ""],
        [TIER_B, "55-74", "Would probably buy, but not proof of a market on "
         "their own.", "", ""],
        [TIER_C, "under 55", "Useful as a control. If C-tier people want it, "
         "the market is wider than you think.", "", ""],
        ["", "", "", "", ""],
        ["What is being tested", "", "", "", ""],
        ["Positioning", "Culture-first: a love letter to the world's "
         "most-eaten food. Not character-first cute.", "", "", ""],
        ["Flagship", "Plush / throw pillow, Squishmallow-adjacent, soft and "
         "squishy. Kids are the ones who love it. Under $100.", "", "", ""],
        ["Entry product", "Stickers stay in the line as the cheap way in. "
         "Score people on the flagship — the 'Would buy' column records "
         "whether they are a pillow buyer, a sticker buyer, or both.", "", "", ""],
        ["Audiences in play", "All three: kawaii/stationery collectors, "
         "food-culture people, and the diaspora 'rice is home' audience.",
         "", "", ""],
        ["", "", "", "", ""],
        ["Watch for", "The buyer and the user are different people. An adult "
         "pays; a child hugs it. A high score with no child in their life is a "
         "gift-buyer, not a household customer — track them separately.",
         "", "", ""],
        ["Also watch for", "Lots of 'Stickers only' is a real answer, not a "
         "failure. It means the brand works and the $100 plush is the wrong "
         "first product — go cheaper or smaller, or let stickers lead and the "
         "plush follow once there is an audience.", "", "", ""],
        ["Be honest", "Score people as they are, not as you hope. A sheet of "
         "generous 4s tells you nothing you did not already believe.",
         "", "", ""],
    ]
    return rows


def readout_rows():
    rows = [
        ["Readout", "", "", ""],
        ["Updates itself as you fill in the Network tab.", "", "", ""],
        ["", "", "", ""],
        ["People scored", '=COUNTIF(Network!K2:K1000,">=0")', "", ""],
        ["Average fit score", '=IFERROR(ROUND(AVERAGE(Network!K2:K1000),0),"-")', "", ""],
        ["Average price they would pay",
         '=IFERROR(TEXT(ROUND(AVERAGE(Network!N2:N1000),0),"$#,##0"),"-")', "", ""],
        ["", "", "", ""],
        ["By tier", "Count", "", ""],
        [TIER_A, '=COUNTIF(Network!L2:L1000,"A*")', "", ""],
        [TIER_B, '=COUNTIF(Network!L2:L1000,"B*")', "", ""],
        [TIER_C, '=COUNTIF(Network!L2:L1000,"C*")', "", ""],
        ["", "", "", ""],
        ["By segment", "Count", "Avg fit", "Avg would-pay"],
    ]
    for seg in SEGMENTS:
        rows.append([
            seg,
            f'=COUNTIF(Network!M2:M1000,"{seg}")',
            f'=IFERROR(ROUND(AVERAGEIF(Network!M2:M1000,"{seg}",Network!K2:K1000),0),"-")',
            f'=IFERROR(TEXT(ROUND(AVERAGEIF(Network!M2:M1000,"{seg}",Network!N2:N1000),0),"$#,##0"),"-")',
        ])
    rows += [["", "", "", ""], ["Flagship vs entry product", "Count", "", ""]]
    for wb in WOULD_BUY:
        rows.append([wb, f'=COUNTIF(Network!O2:O1000,"{wb}")', "", ""])
    rows += [["", "", "", ""],
             ["Which criterion drives fit?", "Avg score", "", ""]]
    for i, (name, _w, _a, _b, _c) in enumerate(CRITERIA):
        c = chr(ord("F") + i)
        rows.append([name, f'=IFERROR(ROUND(AVERAGE(Network!{c}2:{c}1000),1),"-")', "", ""])
    rows += [
        ["", "", "", ""],
        ["Kids signal check", "", "", ""],
        ["Scored 4-5 on kids", '=COUNTIF(Network!F2:F1000,">=4")', "", ""],
        ["...of those, tier A",
         '=COUNTIFS(Network!F2:F1000,">=4",Network!L2:L1000,"A*")', "", ""],
        ["Tier A with NO kids (gift-buyers)",
         '=COUNTIFS(Network!F2:F1000,"<=2",Network!L2:L1000,"A*")', "", ""],
    ]
    return rows


# ---------------------------------------------------------------- xlsx writer
def write_xlsx(path):
    from openpyxl import Workbook
    from openpyxl.formatting.rule import ColorScaleRule, FormulaRule
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation

    HEAD_FILL = PatternFill("solid", fgColor="2A3038")
    SOFT_FILL = PatternFill("solid", fgColor="F1EFE9")
    TIERA_FILL = PatternFill("solid", fgColor="EDF5F0")
    HEAD_FONT = Font(bold=True, size=10, color="FFFFFF")
    BOLD = Font(bold=True)

    wb = Workbook()

    # -- Network -------------------------------------------------------------
    ws = wb.active
    ws.title = "Network"
    ws.append(HEADERS)
    for r in range(2, ROWS + 2):
        row = [None] * 10 + [fit_formula(r), tier_formula(r)] + [None] * 6
        ws.append(row)

    for c in range(1, len(HEADERS) + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill, cell.font = HEAD_FILL, HEAD_FONT
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[1].height = 42
    ws.freeze_panes = "B2"

    for a, b, w in [(1, 1, 22), (2, 2, 14), (3, 3, 17), (4, 4, 24), (5, 5, 20),
                    (6, 10, 12), (11, 11, 10), (12, 12, 14), (13, 13, 22),
                    (14, 14, 13), (15, 15, 17), (16, 16, 11), (17, 17, 34),
                    (18, 18, 34)]:
        for c in range(a, b + 1):
            ws.column_dimensions[get_column_letter(c)].width = w

    for c in range(6, 13):
        for r in range(2, ROWS + 2):
            ws.cell(row=r, column=c).alignment = Alignment(horizontal="center")
    for r in range(2, ROWS + 2):
        ws.cell(row=r, column=14).number_format = '"$"#,##0'
        for c in (17, 18):
            ws.cell(row=r, column=c).alignment = Alignment(wrap_text=True, vertical="top")

    def dv(values, ref, allow_blank=True):
        d = DataValidation(type="list",
                           formula1='"' + ",".join(values) + '"',
                           allow_blank=allow_blank, showDropDown=False)
        ws.add_data_validation(d)
        d.add(ref)

    last = ROWS + 1
    dv(RELATIONSHIPS, f"B2:B{last}")
    dv(["1", "2", "3", "4", "5"], f"F2:J{last}")
    dv(SEGMENTS, f"M2:M{last}")
    dv(WOULD_BUY, f"O2:O{last}")
    dv(ASKED, f"P2:P{last}")

    ws.conditional_formatting.add(
        f"K2:K{last}",
        ColorScaleRule(start_type="num", start_value=30, start_color="F7F5EE",
                       end_type="num", end_value=90, end_color="4A8760"))
    # Match on the leading letter so the band survives any relabelling.
    ws.conditional_formatting.add(
        f"A2:R{last}",
        FormulaRule(formula=['=LEFT($L2,1)="A"'], fill=TIERA_FILL, stopIfTrue=False))

    ws.auto_filter.ref = f"A1:R{last}"

    # -- Rubric --------------------------------------------------------------
    rb = wb.create_sheet("Rubric")
    for row in rubric_rows():
        rb.append(row)
    for a, w in [(1, 26), (2, 12), (3, 46), (4, 46), (5, 46)]:
        rb.column_dimensions[get_column_letter(a)].width = w
    for r in range(1, rb.max_row + 1):
        for c in range(1, 6):
            rb.cell(row=r, column=c).alignment = Alignment(wrap_text=True, vertical="top")
    for c in range(1, 6):
        cell = rb.cell(row=4, column=c)
        cell.fill, cell.font = HEAD_FILL, HEAD_FONT
    for r in (1, 10, 12, 17):  # title, Total, "Tier bands", "What is being tested"
        rb.cell(row=r, column=1).font = BOLD
        for c in range(1, 6):
            rb.cell(row=r, column=c).fill = SOFT_FILL
    for r in range(5, 10):
        rb.cell(row=r, column=2).number_format = "0%"
    rb.cell(row=1, column=1).font = Font(bold=True, size=13)

    # -- Readout -------------------------------------------------------------
    ro = wb.create_sheet("Readout")
    for row in readout_rows():
        ro.append(row)
    for a, w in [(1, 34), (2, 14), (3, 14), (4, 16)]:
        ro.column_dimensions[get_column_letter(a)].width = w
    for r in range(1, ro.max_row + 1):
        v = ro.cell(row=r, column=1).value
        if v in ("Readout", "By tier", "By segment", "Flagship vs entry product",
                 "Which criterion drives fit?", "Kids signal check"):
            for c in range(1, 5):
                ro.cell(row=r, column=c).font = BOLD
                ro.cell(row=r, column=c).fill = SOFT_FILL
    ro.cell(row=1, column=1).font = Font(bold=True, size=13)

    wb.save(path)
    return path


# -------------------------------------------------------------- sheets writer
def write_gsheet():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    if not os.path.exists(TOKEN):
        sys.exit(f"No token.json at {TOKEN}")
    creds = Credentials.from_authorized_user_file(TOKEN)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN, "w", encoding="utf-8") as fh:
                fh.write(creds.to_json())
        else:
            sys.exit("token.json cannot be refreshed — re-run the OAuth flow at the rig.")

    sheets = build("sheets", "v4", credentials=creds)
    created = sheets.spreadsheets().create(body={
        "properties": {"title": TITLE},
        "sheets": [{"properties": {"title": t}} for t in ("Network", "Rubric", "Readout")],
    }).execute()
    sid, url = created["spreadsheetId"], created["spreadsheetUrl"]

    net = [HEADERS]
    for r in range(2, ROWS + 2):
        net.append([""] * 10 + [fit_formula(r), tier_formula(r)] + [""] * 6)

    sheets.spreadsheets().values().batchUpdate(spreadsheetId=sid, body={
        "valueInputOption": "USER_ENTERED",
        "data": [{"range": "Network!A1", "values": net},
                 {"range": "Rubric!A1", "values": rubric_rows()},
                 {"range": "Readout!A1", "values": readout_rows()}],
    }).execute()
    print("created:", url)
    return url


if __name__ == "__main__":
    if "--gsheet" in sys.argv:
        write_gsheet()
    else:
        p = write_xlsx(OUT_XLSX)
        from openpyxl import load_workbook
        wb = load_workbook(p)
        print("wrote:", p)
        for name in wb.sheetnames:
            ws = wb[name]
            print(f"  {name:<9} {ws.max_row} rows x {ws.max_column} cols")
        print("  weights:", [wb["Rubric"].cell(row=r, column=2).value for r in range(5, 10)])
