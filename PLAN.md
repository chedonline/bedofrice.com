# bedofrice — PLAN
> Sticker / art / merch brand. Working hypothesis: **kawaii art × cooking-culture adjacency**, rice as the mascot motif.
> Status: concept phase. This doc is a set of prompts for Charles to riff on, not settled decisions.
> Created 2026-07-13.

## Game spin-off (2026-11-24)
Bed of Rice the video game: a controller-first diner-dash × placement-puzzle × roguelike-deckbuilder, the sticker cast as the pieces. Engine: **Godot 4 + GDScript** (web build first, then iPad, then Steam). Code will live in `game/`.
Design doc (draft, open questions numbered at the end):
https://claude.ai/artifact/Bnk4XNHTJGDkGbFoQK2bpc
Decided 2026-11-24: turn-based with a ticket clock (every action = 1 tick, 30-tick shifts), a row of 5 beds (6 in co-op), sushi counter first, cozy tone, 3 stars + tip target, couch co-op designed in from the start, title = Bed of Rice.
Decided 2026-11-25: co-op is 1–4 players Mario Party style on a mixed couch: each player steers a free party cursor on one shared counter (one extra bed per extra player), soft clock in co-op (ticks when everyone has acted or a Relaxed/5 s/3 s timer runs out), per-player helpers. Touch works Balatro-style through the same cursor input layer, but the controller (with rumble) is the main way to play. Retro pixel art is an acceptable style; the art pass compares it against flat sticker vector.
Controls (2026-11-25): stick + 2 buttons (A does, B serves). Decisions stay turn-based, but every press is a timing action (hold A, release in the sweet spot = Perfect +1 Mult; per-topping windows; Perfect streaks), so it's easy to learn, hard to master.
Going broad (2026-11-25): the counter game is one of three paths, all in the doc's "Other directions": **Kitchen** (the counter / Diner Dash, maybe a real-time Rush mode), **Puzzle** (B. Tuck-in: an ice-slide puzzle where every swipe moves every topping until it lands on a rice bed; touch-first), **Simple** (D. Rice Run: a Subway Surfers-style 3-lane conveyor runner with Perfect tuck-ins). C. Party pack (Mario Party-style 1–4P minigames) can hold all of them. Plus **Simple yet deep** (E. Hungry Horde: Brotato-style arena survivor kept cozy: you're a rice cooker, toppings auto-fling to FEED a crowd of hungry customers, 60 s waves + shop, 6 topping slots with synergies, 1–4 cookers in one arena with a Hand-off double-tip). Plus **Kitchen, real-time** (F. The Sushi Ladder: simplified Overcooked, 1–4 cooks, climb a ladder of restaurants (home kitchen hub → omakase counter → ramen → izakaya → kaiten conveyor → food hall/buffet end game), one new mechanic per rung; the irony "at home you eat on a bed of rice, out you don't" is the story; the master is a made-up character, not a real chef). **Leaning this way (2026-11-25):** stick + ONE context button: tap = pick up / put down / serve, hold = work a station (slice, wash, fan), tap with nothing in reach = dash (empty-handed) or throw (carrying). Lots of interactables on that one verb (auto rice cooker with okoge, belt, sink, cat, spilled soy, swinging noren); each restaurant adds one or two. Hungry Horde is the strongest fit on paper (stick only, deep, co-op for free). Plan: an evening-sized web toy of each, play them, take the winner to Godot.
Apple TV (2026-11-25): AirPlay from the Mac (extended display, controllers paired to the Mac) is enough; no native tvOS app needed, so Godot stays. Steam Deck = browser now, Godot Linux export later.
Art direction (2026-11-26): soft 3D kawaii in the spirit of Boomerang Fu (chunky round food characters, soft-toon shading, tilted top-down camera, very expressive squash-and-stretch animation). 3D is the lean, not locked; fallback = the same look as soft 2D. Toys stay grey-box until a game is picked. Charles likes 3D for zooming in and the Street Fighter route (cel-shaded polygons = most control over animation); pixel/retro is fine only if it's the easy path. Look test `_toys/look-test/` compares soft clay vs cel + ink on one onigiri cook (frames in `_concept/look-test/`). References: Dribbble / ArtStation / Pinterest for characters; Mobbin (connector available) only for menus and UI.
Exploring the name (2026-11-26/27): looked at what "bed of rice" can mean (dug layers, seedbed, paddy, sleep, foundation, rice = meal/livelihood) and walked through a Stardew-style farm-to-plate chain, a tower-defence roguelite, and a Cordillera rice-terrace setting (Ifugao, *tinawon* = once-a-year rice; needs care and consultation if used). Then went super simple: **Nigiri Drop** (`_toys/nigiri-drop/`), one button, drop the topping square on a rice bed rolling by on the belt.
Harvest race (2026-11-28): Boomerang Fu-style hide-and-seek in tall rice, where cutting the stalks reveals the area (and your own cover). Built the calm mode first, **Harvest Race** (`_toys/harvest-race/`): 1 to 4 players, one button (tap = swing, 3-hit combo ending in a spin; hold = boomerang throw), walk over sheaves to collect, ducks eat what's left, sunset ends it. The toy is mainly a **feel test**: snappy like Overcooked with Mario-style weight, and the most satisfying sickle we can make. First real test: two Xbox controllers on the Mac in Chrome, mirrored to the Apple TV. It played well ("works amazing"; AirPlay mirroring caps the frame rate; pairing the controllers is fiddly). Charles loves the harvest mode, so it got a second field the same day: **Rice terraces** (now the default): four tiers held up by stone walls, hop down off an edge, climb back up only by the stairs. Kept generic (no specific real place), so the cultural-consultation note above doesn't apply yet.
Toy: `_toys/sushi-ladder/` (cozy one-button kaiten shift), see `_toys/README.md`.
Concept screens (solo + co-op): `_concept/concept-solo.png`, `_concept/concept-coop.png`; source `_concept/screens.html`, re-render with `node _concept/shot.cjs`.
Next: a grey-box prototype of one shift.

## The read (hypothesis — correct me)
"bed of rice" is a warm, everyday, comfort-food image with built-in cuteness (a little rice character *on* its bed of rice). The white space to own: the **overlap of kawaii character design and real cooking/food culture** — not generic cute food stickers, but rice with a point of view (rituals, dishes, diaspora, the humble staple that carries every cuisine). Stickers are the wedge product; the brand is the character world behind them.

## Open questions — reply by number

### 1. Audience — who's the core fan?
1. **Kawaii/stationery collectors** (Sanrio, Smiko, sticker-club crowd) — buy for cuteness + collectibility.
2. **Food-culture / cooking people** (home cooks, food-media followers, restaurant folks) — buy for the in-joke and the reverence for the dish.
3. **Diaspora / "rice is home" audience** — buy for identity and nostalgia (rice as the thread across Asian, Latin, African, Middle-Eastern tables).
4. Something else / a blend — which two lead?

### 2. Brand strategy — what does bedofrice *stand for*?
1. **Positioning**: is it "the cutest rice on the internet" (character-first) or "a love letter to the world's most-eaten food" (culture-first)? The art style follows this choice.
2. **Voice**: cozy & wholesome, or dry & funny (rice with opinions)?
3. **Character system**: one hero mascot (a single rice grain/ball), or a *cast* (short-grain, jasmine, arborio, a rice cooker, a spoon) — a cast is more merch SKUs and more world.
4. **Name architecture**: is "bed of rice" the brand and the mascot, or is the mascot named separately (e.g. the character is "Gohan"/"Congee") under the bedofrice label?

### 3. Art direction — pin the style
1. **Kawaii lineage to borrow from**: (a) Sanrio-flat pastel, (b) mochi/squishy 3D-render cute, (c) retro Showa/70s-diner kawaii, (d) hand-drawn crayon/marker naive style. Which feels most "us"?
2. **Cooking-culture adjacency, made visual**: rice in real contexts — a nigiri, a bibimbap stone bowl, a burrito, jollof, risotto, a rice cooker with a face. Stickers that are *dish-accurate but cute*.
3. **Palette**: rice-white + a warm accent (nori-black, salmon-pink, seaweed-green, soy-brown)? Lock 3–4.
4. Should the style be **consistent enough to be a system** (die-cut character + a "dish series" + a "type/pun series")?

### 4. Sticker ideas — first drop (I'll expand whichever directions you like)
1. **Hero mascot** die-cuts: sleepy rice grain, rice ball with seaweed belt, rice in a tiny bed (the literal "bed of rice").
2. **Dish series**: cute-but-accurate nigiri, onigiri, bibimbap, congee, arroz con pollo, jollof, risotto — "rice around the world."
3. **Pun / type series**: "rice to meet you," "no rice no life," "well-rounded" (rice ball), "grain of truth."
4. **Ritual series**: rice cooker with a face, the perfect scoop, the crispy bottom (tahdig/nurungji/socarrat) as a cult sticker for foodies.
5. **Holographic / special-finish** collector chase stickers (drives the collector audience in Q1).

### 5. GTM — how it reaches people
1. **Channel**: (a) own Shopify + sticker-pack drops, (b) Etsy for discovery, (c) marketplace/consignment in cafés & Asian grocers, (d) all three staged.
2. **Content engine**: short-form video of the mascot "cooking" + sticker reveals (TikTok/IG/Reels) — cooking-culture adjacency gives endless format (recipe + cute).
3. **Community wedge**: a monthly **sticker club / subscription** (kawaii audiences love the recurring drop + collectibility).
4. **Collabs**: local restaurants, ramen/rice shops, food creators — co-branded packs = built-in distribution + credibility.
5. **Wholesale**: card/gift shops and Asian grocers once the line proves out.

## Suggested first move
Lock **§1 (lead audience)** and **§2.1 (positioning)** first — those two decisions cascade into the art style, the sticker lineup, and the GTM channel. Tell me the numbers and I'll turn the winning direction into a concrete first-drop sticker sheet + a one-page brand brief, and we can mock the mascot in Figma.

## Not yet decided / needs Charles
- Domain/handle availability check (bedofrice.com + socials) — *needs Charles at the rig*.
- Whether this is a side art project or a real commerce line (sets how much GTM rigor to apply). See [[reference_project_modes]] — likely 🛒 Commerce.
