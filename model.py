#!/usr/bin/env python3
"""
bedofrice — unit economics and the routes to $10k/month.

Every number below is an ESTIMATE to be replaced with a real quote. The value
here is the structure and the sensitivity, not the precision: it shows which
lever actually decides whether this is profitable, and what each route to
$10k/month demands in volume, traffic and cash up front.

    python model.py

Nothing here is a forecast. It is arithmetic on assumptions you can change.
"""

from dataclasses import dataclass

# ---------------------------------------------------------------- assumptions
# Sources: typical DTC/custom-plush ranges. VERIFY ALL OF THESE with real
# supplier quotes before committing money -- especially plush FOB and freight,
# which move the answer more than anything else.

PLUSH_FOB = {          # per unit, FOB China, ~40cm throw-pillow size
    300: 17.00,
    500: 14.00,
    1000: 11.00,
    2000: 9.00,
}
PLUSH_SAMPLE_COST = 600.00      # samples + revisions, one-time
PLUSH_FREIGHT_DUTY = 3.20       # per unit, sea freight + duty into Canada
PLUSH_RETAIL = 75.00
PLUSH_PACKAGING = 1.50          # polybag, hangtag, mailer
PLUSH_SHIP_COST = 15.00         # what it costs you to ship one
PLUSH_SHIP_CHARGED = 10.00      # what the customer pays toward it

STICKER_COST = {200: 0.90, 500: 0.60, 2000: 0.35}   # per die-cut sheet
STICKER_RETAIL = 10.00
STICKER_SHIP_COST = 1.60        # letter mail
STICKER_SHIP_CHARGED = 2.00

# Club: a monthly sticker drop. This is the only genuinely recurring line.
CLUB_PRICE = 15.00
CLUB_COGS = 2.20                # 2-3 sheets + insert
CLUB_FULFIL = 1.80              # pick, pack, label
CLUB_SHIP = 2.60
CLUB_CHURN = 0.07               # monthly. Kawaii/collectible clubs run 5-10%.

PAY_RATE, PAY_FIXED = 0.029, 0.30       # Shopify Payments
PLATFORM_FIXED = 39.00 + 60.00          # Shopify plan + apps/email
CAC_PLUSH = 30.00                       # paid social, $60-80 impulse product
CAC_CLUB = 25.00
CONVERSION = 0.02                       # sitewide, DTC typical 1.5-2.5%

TARGET = 10_000.00


def money(x):
    return f"${x:,.0f}" if abs(x) >= 100 else f"${x:,.2f}"


@dataclass
class Line:
    name: str
    revenue: float
    cogs: float
    fees: float
    ship_net: float
    other: float = 0.0

    @property
    def contribution(self):
        return self.revenue - self.cogs - self.fees - self.ship_net - self.other

    @property
    def margin(self):
        return self.contribution / self.revenue if self.revenue else 0


def fees(price_paid):
    return price_paid * PAY_RATE + PAY_FIXED


def plush_unit(moq):
    landed = PLUSH_FOB[moq] + PLUSH_FREIGHT_DUTY
    paid = PLUSH_RETAIL + PLUSH_SHIP_CHARGED
    return Line("Plush", PLUSH_RETAIL, landed + PLUSH_PACKAGING, fees(paid),
                PLUSH_SHIP_COST - PLUSH_SHIP_CHARGED)


def sticker_unit(qty):
    paid = STICKER_RETAIL + STICKER_SHIP_CHARGED
    return Line("Sticker sheet", STICKER_RETAIL, STICKER_COST[qty],
                fees(paid), STICKER_SHIP_COST - STICKER_SHIP_CHARGED)


def club_unit():
    return Line("Club member / month", CLUB_PRICE, CLUB_COGS,
                fees(CLUB_PRICE), CLUB_SHIP, CLUB_FULFIL)


def hr(title):
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")


def show(line, cac=None):
    print(f"  {line.name}")
    print(f"    revenue                {money(line.revenue):>10}")
    print(f"    product cost           {money(-line.cogs):>10}")
    print(f"    payment fees           {money(-line.fees):>10}")
    print(f"    shipping (net)         {money(-line.ship_net):>10}")
    if line.other:
        print(f"    fulfilment             {money(-line.other):>10}")
    print(f"    contribution           {money(line.contribution):>10}   "
          f"({line.margin*100:.0f}% margin)")
    if cac:
        print(f"    less CAC               {money(-cac):>10}")
        print(f"    profit per unit        {money(line.contribution - cac):>10}")
    return line.contribution


def main():
    hr("UNIT ECONOMICS  (per sale, before fixed costs)")
    for moq in (300, 500, 1000, 2000):
        p = plush_unit(moq)
        print(f"\n  -- plush at MOQ {moq}  (landed "
              f"{money(PLUSH_FOB[moq] + PLUSH_FREIGHT_DUTY)}/unit)")
        show(p, CAC_PLUSH)

    print()
    s = sticker_unit(500)
    show(s, CAC_PLUSH * 0.4)
    print()
    c = club_unit()
    show(c, CAC_CLUB)

    # ---------------------------------------------------------------- routes
    hr(f"ROUTE A — plush store to {money(TARGET)}/month REVENUE (not recurring)")
    p = plush_unit(1000)
    orders = TARGET / PLUSH_RETAIL
    contrib = orders * p.contribution
    mktg = orders * CAC_PLUSH
    net = contrib - mktg - PLATFORM_FIXED
    print(f"  orders needed / month            {orders:>10.0f}")
    print(f"  contribution                     {money(contrib):>10}")
    print(f"  marketing at {money(CAC_PLUSH)} CAC            {money(-mktg):>10}")
    print(f"  platform + tools                 {money(-PLATFORM_FIXED):>10}")
    print(f"  NET PROFIT / month               {money(net):>10}")
    print(f"  site sessions needed at {CONVERSION*100:.1f}%      "
          f"{orders/CONVERSION:>10,.0f}")
    print(f"  units / year                     {orders*12:>10,.0f}")
    print(f"  -> reorders per year at MOQ 1000 {orders*12/1000:>10.1f}")
    print(f"\n  Cash to start: {money(1000*(PLUSH_FOB[1000]+PLUSH_FREIGHT_DUTY) + PLUSH_SAMPLE_COST)}"
          f"  (1,000 units + samples), before any marketing.")
    print("  And it resets to zero every month. This is revenue, not MRR.")

    hr(f"ROUTE B — sticker club to {money(TARGET)}/month TRUE MRR")
    c = club_unit()
    subs = TARGET / CLUB_PRICE
    churn_n = subs * CLUB_CHURN
    contrib = subs * c.contribution
    replace = churn_n * CAC_CLUB
    net = contrib - replace - PLATFORM_FIXED
    print(f"  subscribers needed at {money(CLUB_PRICE)}/mo     {subs:>10.0f}")
    print(f"  contribution                     {money(contrib):>10}")
    print(f"  churn at {CLUB_CHURN*100:.0f}%/mo                    "
          f"{churn_n:>10.0f} members lost")
    print(f"  cost to replace them             {money(-replace):>10}")
    print(f"  platform + tools                 {money(-PLATFORM_FIXED):>10}")
    print(f"  NET PROFIT / month               {money(net):>10}")
    print(f"\n  Cash to start: near zero — stickers print on demand at low MOQ.")
    print(f"  But you must ADD {churn_n:.0f} members every month just to stand still,")
    print(f"  and reach {subs:.0f} in the first place. That is the whole problem.")

    # How long to build the club at various net-add rates
    print("\n  Months to reach 667 members, by net new members per month:")
    for adds in (20, 40, 60, 100):
        n, m = 0.0, 0
        while n < subs and m < 600:
            n = n * (1 - CLUB_CHURN) + adds
            m += 1
        ceiling = adds / CLUB_CHURN
        if n < subs:
            print(f"    {adds:>4}/mo  never — churn caps you at {ceiling:.0f} members")
        else:
            print(f"    {adds:>4}/mo  {m} months   (ceiling {ceiling:.0f})")

    hr("ROUTE C — the blend (what I would actually build)")
    club_subs = 400
    club_rev = club_subs * CLUB_PRICE
    plush_orders = (TARGET - club_rev) / PLUSH_RETAIL
    p = plush_unit(1000)
    c = club_unit()
    contrib = club_subs * c.contribution + plush_orders * p.contribution
    mktg = club_subs * CLUB_CHURN * CAC_CLUB + plush_orders * CAC_PLUSH
    net = contrib - mktg - PLATFORM_FIXED
    print(f"  {club_subs} club members            {money(club_rev):>10}  (recurring)")
    print(f"  {plush_orders:.0f} plush / month             "
          f"{money(plush_orders*PLUSH_RETAIL):>10}  (transactional)")
    print(f"  total revenue                    {money(TARGET):>10}")
    print(f"  contribution                     {money(contrib):>10}")
    print(f"  marketing                        {money(-mktg):>10}")
    print(f"  platform + tools                 {money(-PLATFORM_FIXED):>10}")
    print(f"  NET PROFIT / month               {money(net):>10}")
    print(f"\n  The club carries {club_rev/TARGET*100:.0f}% of revenue as genuine MRR and funds")
    print("  acquisition; the plush is the thing people show each other.")

    # ------------------------------------------------------------ what breaks
    hr("WHAT ACTUALLY DECIDES THIS")
    p = plush_unit(1000)
    print(f"  Contribution per plush           {money(p.contribution)}")
    print(f"  Break-even CAC                   {money(p.contribution)}  "
          f"(above this you lose money on every sale)")
    print(f"  Assumed CAC                      {money(CAC_PLUSH)}")
    print(f"  Headroom                         {money(p.contribution - CAC_PLUSH)}/unit\n")
    for cac in (20, 30, 40, 50):
        orders = TARGET / PLUSH_RETAIL
        net = orders * (p.contribution - cac) - PLATFORM_FIXED
        verdict = "viable" if net > 2000 else ("thin" if net > 0 else "LOSS")
        print(f"    CAC {money(cac):>6}  ->  net {money(net):>8}/mo   {verdict}")
    print("\n  Shipping a bulky plush is the quiet killer:")
    for charged in (0, 10, 15):
        pp = PLUSH_RETAIL + charged
        line = Line("x", PLUSH_RETAIL, PLUSH_FOB[1000] + PLUSH_FREIGHT_DUTY + PLUSH_PACKAGING,
                    fees(pp), PLUSH_SHIP_COST - charged)
        print(f"    customer pays {money(charged):>6} shipping  ->  "
              f"contribution {money(line.contribution):>7}  ({line.margin*100:.0f}%)")


def channels():
    """What $10k/month looks like through each sales channel.

    DTC is the only channel where you pay for every visitor. The reason the
    business reads as 'content trying to be product' is entirely the channel
    mix -- not the product. Wholesale and marketplace rent someone else's
    audience, which is what makes a product business a product business.
    """
    landed = PLUSH_FOB[1000] + PLUSH_FREIGHT_DUTY

    # -- DTC ---------------------------------------------------------------
    dtc = plush_unit(1000)
    dtc_cac = CAC_PLUSH

    # -- Wholesale: retailer buys at ~50% of MSRP, you ship cases -----------
    WHOLESALE = PLUSH_RETAIL * 0.50
    ws_contrib = WHOLESALE - landed - 0.60          # case pack, not retail mailer
    ws_cac = 1.50                                   # outreach/samples amortised

    # -- Marketplace (Amazon FBA): their traffic, their fees ----------------
    MP_REFERRAL = 0.15
    MP_FBA = 9.50                                   # bulky/oversize plush
    mp_contrib = PLUSH_RETAIL * (1 - MP_REFERRAL) - landed - MP_FBA - 1.50
    mp_cac = 12.00                                  # sponsored products

    rows = [
        ("DTC (your own store)", PLUSH_RETAIL, dtc.contribution, dtc_cac, True),
        ("Wholesale (shops)", WHOLESALE, ws_contrib, ws_cac, False),
        ("Marketplace (Amazon)", PLUSH_RETAIL, mp_contrib, mp_cac, False),
    ]

    hr("CHANNEL COMPARISON — the same plush, three ways to sell it")
    print(f"{'channel':<24}{'you get':>9}{'contrib':>9}{'CAC':>8}"
          f"{'net/unit':>10}{'units for $10k':>15}{'your traffic?':>15}")
    for name, price, contrib, cac, needs_traffic in rows:
        net = contrib - cac
        units = TARGET / price
        print(f"{name:<24}{money(price):>9}{money(contrib):>9}{money(cac):>8}"
              f"{money(net):>10}{units:>15.0f}{'YES' if needs_traffic else 'no':>15}")

    print(f"\n  At $10k/month revenue:")
    for name, price, contrib, cac, needs_traffic in rows:
        units = TARGET / price
        profit = units * (contrib - cac) - PLATFORM_FIXED
        sessions = f"{units/CONVERSION:,.0f} sessions" if needs_traffic else "none of your own"
        print(f"    {name:<24} net {money(profit):>8}/mo   traffic needed: {sessions}")

    print("\n  Wholesale needs far more units but no audience. The trade is")
    print("  margin for reach, and it is the classic product-business trade.")

    # -- A cast, not a character -------------------------------------------
    hr("WHY ONE SKU IS THE REAL PROBLEM")
    print("  A single plush has no repeat purchase. Collectibility is what makes")
    print("  Squishmallows a business rather than a toy: people buy the set.\n")
    for skus, repeat in ((1, 1.0), (3, 1.5), (6, 2.1), (10, 2.6)):
        orders = TARGET / PLUSH_RETAIL
        customers = orders / repeat
        blended_cac = CAC_PLUSH * customers / orders
        net = orders * (plush_unit(1000).contribution - blended_cac) - PLATFORM_FIXED
        print(f"    {skus:>2} characters  ->  {repeat:.1f} units per customer   "
              f"effective CAC {money(blended_cac):>6}   net {money(net):>8}/mo")
    print("\n  Same revenue, same product cost. The only thing that changed is")
    print("  how many times one acquired customer buys. That is the whole game.")

    # -- Working capital ----------------------------------------------------
    hr("CASH, NOT PROFIT, IS WHAT KILLS PRODUCT BUSINESSES")
    for moq in (500, 1000, 2000):
        cash = moq * (PLUSH_FOB[moq] + PLUSH_FREIGHT_DUTY) + PLUSH_SAMPLE_COST
        months = moq / (TARGET / PLUSH_RETAIL)
        print(f"    MOQ {moq:>5}  ->  {money(cash):>8} tied up   "
              f"{months:.1f} months of stock at 133 units/mo")
    print("\n  Wholesale usually pays net 30-60, so you fund production, ship,")
    print("  and wait two more months to be paid. Plan the float, not the margin.")


COMPLIANCE_PER_SKU = 1500.00    # CPSIA / CCPSA testing, cert, labelling
DEPOSIT = 0.30                  # standard: 30% on order, 70% on shipment
LEAD_MONTHS = 3                 # production + sea freight before goods land

RAMPS = {
    "optimistic": [15, 30, 50, 70, 90, 110, 133, 133, 133, 133, 133, 133,
                   133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133],
    "realistic":  [8, 15, 22, 32, 45, 60, 75, 90, 105, 120, 133, 133,
                   133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133],
    "slow":       [5, 8, 12, 18, 25, 32, 40, 50, 60, 70, 80, 90,
                   100, 110, 120, 133, 133, 133, 133, 133, 133, 133, 133, 133],
}


def cashflow(ramp_name, moq=500, skus=3, price=PLUSH_RETAIL, cac=CAC_PLUSH,
             months=24, verbose=True):
    """Month-by-month cash for a DTC launch, from first sample to steady state.

    Returns (trough, trough_month, payback_month, rows). The trough is the
    number that answers 'how much do I need to float' -- profit per unit is
    not the constraint, the gap between paying for stock and selling it is.
    """
    landed = PLUSH_FOB[moq] + PLUSH_FREIGHT_DUTY
    contrib_per = plush_unit(moq).contribution
    ramp = RAMPS[ramp_name]

    cash = 0.0
    stock = 0
    rows = []
    reorders = 0

    # Month 0: samples + compliance, before anything exists.
    cash -= PLUSH_SAMPLE_COST + COMPLIANCE_PER_SKU * skus
    rows.append((0, "samples + compliance", 0, cash, 0))

    po_units = moq * skus
    cash -= po_units * landed * DEPOSIT
    rows.append((1, f"deposit on {po_units} units", 0, cash, 0))

    for m in range(2, months + 1):
        note = ""
        sold = 0
        if m == LEAD_MONTHS:
            cash -= po_units * landed * (1 - DEPOSIT)
            note = "balance paid, goods ship"
        elif m == LEAD_MONTHS + 1:
            stock += po_units
            note = "stock lands, selling starts"

        if stock > 0 and m > LEAD_MONTHS:
            idx = m - LEAD_MONTHS - 1
            want = ramp[idx] if idx < len(ramp) else ramp[-1]
            sold = min(want, stock)
            stock -= sold
            cash += sold * (contrib_per + (price - PLUSH_RETAIL))
            cash -= sold * cac
            cash -= PLATFORM_FIXED

            # Reorder when under ~2 months of cover, at the current run rate.
            if stock < sold * 2 and sold > 0:
                cash -= po_units * landed * DEPOSIT
                reorders += 1
                note = (note + "; " if note else "") + f"reorder #{reorders} deposit"
                stock += po_units  # simplification: treat as arriving on time

        rows.append((m, note, sold, cash, stock))

    trough = min(r[3] for r in rows)
    trough_month = next(r[0] for r in rows if r[3] == trough)
    payback = next((r[0] for r in rows if r[3] > 0), None)

    if verbose:
        print(f"\n  -- {ramp_name.upper()}  ({skus} characters, MOQ {moq} each, "
              f"{money(price)} retail, {money(cac)} CAC)")
        print(f"     {'mo':>3} {'sold':>5} {'stock':>6} {'cash':>11}   note")
        for m, note, sold, c, st in rows:
            if m <= 14 or note or m == months:
                print(f"     {m:>3} {sold:>5} {st:>6} {money(c):>11}   {note}")
    return trough, trough_month, payback, rows


def cash_section():
    hr("THE CASH QUESTION — what you actually need to float")
    print("  Assumes 3 characters, MOQ 500 each (1,500 units), $75 retail,")
    print("  $30 CAC, 30% deposit, 3-month lead time, compliance testing per SKU.")

    for name in ("optimistic", "realistic", "slow"):
        cashflow(name, moq=500, skus=3, verbose=True, months=24)

    hr("SUMMARY — the float, by scenario and scale")
    print(f"  {'scenario':<14}{'SKUs':>5}{'MOQ':>6}{'units':>7}"
          f"{'worst cash':>13}{'at month':>10}{'positive by':>13}")
    for skus, moq in ((1, 500), (2, 500), (3, 500), (3, 1000)):
        for name in ("optimistic", "realistic", "slow"):
            t, tm, pb, _ = cashflow(name, moq=moq, skus=skus, verbose=False)
            pbs = f"month {pb}" if pb else "not in 24mo"
            print(f"  {name:<14}{skus:>5}{moq:>6}{skus*moq:>7}"
                  f"{money(t):>13}{tm:>10}{pbs:>13}")
        print()

    hr("PRICE IS THE CHEAPEST LEVER YOU HAVE")
    for price in (75, 85, 95):
        t, tm, pb, _ = cashflow("realistic", moq=500, skus=3, price=price, verbose=False)
        pbs = f"month {pb}" if pb else "not in 24mo"
        print(f"    {money(price)} retail  ->  worst cash {money(t):>10}   "
              f"cash-positive {pbs}")
    print("\n  Same product, same costs, same customers. 'Under $100' allows $95.")


if __name__ == "__main__":
    main()
    channels()
    cash_section()
