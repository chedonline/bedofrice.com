# Bed of Rice toys

Rough playable sketches for trying game directions before the Godot build. They're plain HTML/JS with no build step. The `_` prefix keeps them off the public site, because GitHub Pages' Jekyll skips underscore folders.

## harvest-race/: cut the paddy, grab the sheaves (1 to 4 players, one button)

A paddy of tall ripe rice seen from above. Cut it, then walk over the sheaves to collect them. Whoever has the most rice by sunset (90 s) wins, or when the field is bare. This is the calm "harvest race" mode of the Boomerang Fu-style hide-and-seek idea: inside tall rice you're hidden (only the rustle and your P-marker show). Plain 2D canvas, one file, no internet needed. Open `http://localhost:5181/harvest-race/` (or the rig IPs below).

- **The button:** tap swings the sickle. Three quick taps = left, right, then a bigger spin. Hold, then let go, throws the sickle like a boomerang: it mows a lane out and back. Hold until the *ding* for a full-power throw (longer, wider). Tap while it's out calls it back. A thrown sickle that hits another player makes them dizzy for a moment.
- **Moving:** tall rice is slow to wade through and stubble is fast, so cutting paths is part of the plan. Three ducks wander the paddy and eat sheaves left on the ground.
- **Feel (the point of this toy):** snappy like Overcooked (instant facing, quick acceleration, buffered taps so a press is never eaten) with Mario-style weight (momentum, a short slide when you stop, a skid with dust when you reverse, a lean into speed changes, squash on footsteps). The sickle gets hit-stop and screen shake scaled to how much it cut, toppling stalks, rumble while the boomerang mows, and a twirl on the catch.
- **Fields:** *Rice terraces* (the default) and *Rice paddy*. Switch in the lobby with LB / RB (T on the keyboard, or click the Field line); the browser remembers the last one.
- **Terraces:** four tiers stepped down the hill, held up by stone walls. Push the stick down off an edge to hop down a tier (with a little hop, a thud and dust); walking along the lip doesn't drop you. The only way back up is the stairs (two or three per wall, staggered so you zigzag). Your swing only cuts your own tier, but a thrown sickle flies over the walls. Sheaves flung over an edge tumble down to the tier below, and you can only pick up sheaves on your own tier. Each duck keeps to its tier. CPUs hop down toward lower targets and walk to the nearest stairs for higher ones.
- **Modes:** *Race* (most rice wins) and *Co-op* (one shared basket). Switch in the lobby with LT / RT (O on the keyboard, or click the Mode line); the browser remembers it.
- **Co-op days:** co-op is a ladder of 8 days, each adding one new thing (LB / RB or T picks the day; the browser remembers each day's best stars, and the lobby shows the total out of 24):
  1. *First harvest* (paddy): the rope and the basket.
  2. *The terraces*: boost up walls, and the midday storm.
  3. *Sparrows* (paddy): flocks swoop onto the rice and eat it until a swing, a throw, the rope or a ping (Y) scares them off.
  4. *The thresher* (paddy): carry day. Drop sheaves in the hopper; stand on the pedal and tap on the drum beat (the ring closes on the beat). Perfect = double rice, Good = normal, off the beat = clunk. With nobody on the pedal it threshes slowly by itself; what's in the hopper at sunset still counts.
  5. *Buffalo cart* (paddy): carry day. Press at the buffalo's head to lead it, press again to let go; load it at the back (40 max); it unloads itself next to the barn. The rope partner can't tug the driver.
  6. *The pulley* (terraces): carry day. The barn is on the top tier. Load the basket at the bottom of the pulley (right side); it rises by itself after 1.5 s (or when full), faster if someone taps the crank up top.
  7. *Duck pen* (paddy): six ducks run from you. Herd them into the pen in the bottom-right corner (+10 each). A lone herder gets dodged sideways; two can pinch them in.
  8. *Planting season*: the mirror mode. A flooded paddy with planting strings; tap to plant a seedling (12 in hand, refill at the tray on the left). On the drum beat = Perfect (3), Good (2), off = wobbly (1); next to your last one along the row 3+ times = +1. At sunset the field grows into ripe rice.
- **Carry days:** what you pick up rides on your back (12 max, slower the more you carry) and only counts once you drop it at a station. Walk into a friend while carrying to hand your load over: it's worth 25% more.
- **Co-op dopamine:** sheaves fly up into the basket bar (a tick that climbs in pitch as it fills); each star reached mid-round gets a chord, rumble and confetti; *Harvest Fever*: picking up fast (and Perfects, double spins, hand-offs, shoos, pens) fills the meter under the bar, and a full meter gives 6 s of double rice with a golden glow and music (10 s cool-down); 3 stars or a cleared field rains confetti.
- **Co-op targets:** the HUD bar shows the basket against three star targets, as a share of the field's rice (with fever you can pass 100%): days 1, 2, 3, 7 use 60 / 85 / 105% for two players, 40 / 60 / 80% alone, 65 / 90 / 110% for three or four. The carry days and planting set their own (lower) bars in `DAYS`.
  - *Two-handled scythe:* partners (P1 + P2, P3 + P4) share a rope. Spread out past arm's length and walk, and it cuts everything between you; it drags a little while it cuts. Too far apart and it tugs you together. It only cuts when you're both on the same tier.
  - *Double spin:* two players swing within 0.2 s of each other while close: one big spin between them ("Together!"). Humans only, so a CPU can't trigger it by accident.
  - *Boost:* on the terraces, push up against a wall with a friend beside you at the bottom (they're the step) or standing on the lip above (they pull you up). A CPU partner walks over to help when you're stuck at a wall.
  - *Storm:* at 40 s (sooner for 3 or 4 players) a storm warns, then a band of rain sweeps across and soaks any sheaf left lying in it.
  - *Help:* a swing next to a dizzy friend wakes them. Players can drop in mid-round. Extra ducks for each player past two.
  - CPU partners walk beside you so the rope sweeps; if you stand still for 2 s they go off and harvest on their own. CPUs also take the day's jobs: pedal on the beat, lead the cart out and back, crank the pulley, chase sparrows, herd ducks (odd-numbered CPUs), plant along the rows.
- **Ping:** Y (E or / on the keyboard) pops a "!" over your head, in both modes.
- **Hats:** 11 hats unlocked by your total co-op stars (Headscarf, then Straw hat at 1, Hibiscus 3, Chef hat 5, Party hat 7, Bucket hat 9, Harvest wreath 12, Rice cooker lid 15, Salmon nigiri 18, Duck friend 21, Golden crown 24). In the lobby Y changes your hat (in a round it pings); the pick is saved per controller or key set. A new unlock gets a big card under the end screen with fanfare and confetti, and the human players put it straight on; otherwise the card shows how far it is to the next hat. CPUs wear a random unlocked hat. Hats show in both modes.
- **Awards:** every round ends with up to four funny awards, one per player first (Bonk Magnet, Gravity Fan, Duck Whisperer, Menace, In Sync, Helping Hand, Chatterbox, Golden Touch, Stair Master, Lawn Mower, Top Picker, Marathon, Scarecrow, Duck Herder, Pack Mule, Team Player, Rhythm Master, Green Thumb, Buffalo Whisperer, Muscles).
- **Lobby = practice field:** joined players can run around and cut before starting; the rice grows back. The co-op rope, boost and double spin work here too (the storm doesn't).
- **Controls:** controller: stick + A, B or X, Y pings, Start begins and pauses, View adds a CPU (or removes them when full), LB/RB switch the field (the day in co-op), LT/RT the mode. At a station the button works it (pedal, crank, reins, planting). Keyboard: WASD + Space (E pings), arrows + Enter (/ pings); G starts, C adds a CPU, T switches the field, O the mode, P pauses, F full screen, M sound.
- **Pause menu:** Resume, Restart, Back to lobby. Stick or d-pad to move, A to choose, B (or Start) closes it. Keyboard: arrows, Space/Enter to choose, Backspace/P/Esc closes. You can also click an item.
- **Two Xbox controllers on the Mac, mirrored to the Apple TV:** pair both controllers with the Mac over Bluetooth, open `http://10.0.0.130:5181/harvest-race/` in Chrome (or `http://100.84.97.111:5181/harvest-race/` on Tailscale), click *Full screen* (that click also turns the sound on), then mirror the display to the Apple TV from Control Centre → Screen Mirroring. Press A on each controller to join. Chrome only lists a controller after a button press; the lobby shows which controllers it can see. If none show up, open the file straight from Dropbox on the Mac (`~/Dropbox/claude/projects/bedofrice.com/_toys/harvest-race/index.html`): it's a single file.
- **Tuning knobs:** the constants at the top of the script (`SPEED_OPEN`/`SPEED_RICE`, `ACCEL`/`FRICTION`/`SKID`/`LEAN`, `SLASH_R`/`SLASH_CD`, `HOLD_MIN`/`CHARGE_T`/`THROW_MIN`/`THROW_MAX`/`BOOM_SPEED`, `ROUND`, `DUCKS`). Terraces: `WALL_H`, `DIKE`, `STAIR_W`, `STAIR_SLOW`, `DROP_HOP`, and the wall curves and stair positions in `LEVELS`. Co-op: `ROPE_MIN`/`ROPE_MAX`/`ROPE_R`/`ROPE_DRAG`, `SYNC_WIN`/`SYNC_D`, `STORM_AT`/`STORM_W`/`STORM_SPEED`/`SOAK`, `STARS_SOLO`/`STARS_DUO`/`STARS_CREW`, `CREW_DUCKS`. Days: `DAYS` (features and star bars per day), `CARRY_MAX`/`CARRY_SLOW`/`HANDOFF_BONUS`, `BEAT`/`PERFECT_W`/`GOOD_W`, `THRESH_AUTO`, `CART_MAX`/`CART_SPEED`, `PULLEY_MAX`/`PULLEY_AUTO`/`PULLEY_CRANK`, `PEN_BONUS`, `FLOCK_EVERY`/`FLOCK_EAT`/`FLOCK_STAY`, `SEEDS`, `FEVER_FILL`/`FEVER_DRAIN`/`FEVER_T`/`FEVER_CD`.
- **Testing:** `__harvest.manual(true)` stops the clock, then `__harvest.step(frames)`. `__harvest.addBot()` adds a CPU, `__harvest.start()` begins a round, `__harvest.switchLevel(1)` changes the field and `__harvest.switchMode()` the mode (lobby only). `__harvest.setDay(i)` jumps to a co-op day (0 to 7). CPU balance check, 2026-11-28 (two CPUs): day 1 and Sparrows 3 stars (CPUs are much better with the rope than people), thresher about 1, cart 1 to 2, pulley 1, duck pen 1 (one CPU herding alone pens about 1 duck), planting 2 to 3.

## nigiri-drop/: the super simple one (one button)

Rice beds with faces roll by on a sushi belt, and a topping hangs from chopsticks. Tap to drop it so it lands square on the rice. Open `http://localhost:5181/nigiri-drop/` (or the rig IPs below). Plain 2D canvas, no internet needed.

- **Landing:** Perfect (centre), Good, Sloppy (the topping sits crooked) or Splat (it misses and rides off on the belt). Three splats end the shift. Every 25 nigiri wins a life back.
- **Score:** Perfect 3, Good 2, Sloppy 1, times a streak multiplier (up to x5) built from Perfects. Sloppy or Splat resets it. Best score is saved on the device.
- **It gets harder:** the belt speeds up, the rice beds shrink, and after 15 nigiri the chopsticks start to sway.
- **Controls:** tap, click, Space/Enter/J, or any face button on a controller (rumble on a Splat). P/Esc/Start pauses; it also pauses when the tab is hidden.
- **Tuning knobs:** the constants at the top of the script (`GRAV`, `PERFECT`/`GOOD`/`SLOPPY`, `SPEED0`/`SPEED_UP`/`SPEED_MAX`, `SWAY_FROM`, `LIVES`, `BONUS_EVERY`).
- **Testing:** `window.__drop.step(frames)`. `__drop.bot(true)` turns on the auto-chef (the same one that plays the title screen).

## look-test/: one rice cook in 3D (art direction)

A Three.js sketch (loaded from the jsdelivr CDN, so it needs internet) of the hero as a soft 3D onigiri, to judge the look before any Godot work. Open `http://localhost:5181/look-test/` (or the rig IPs below).

- **Two finishes:** Look button / T / Start toggles *soft clay* (matte + warm rim) and *cel shaded + ink outlines* (Street Fighter route).
- **Moves, all procedural:** walk (hop, lean, wobble, footfall squash), Dash (stretch, dust, squash on stop), Carry (lift a nigiri overhead, wobble), Yay (anticipation squash, spin jump, confetti, camera push-in), Bonk (knock-back, X eyes, stars, freeze frame + shake + rumble).
- **Also:** Camera (game view / close-up, the cook turns to face you when idle), Skin (classic, brown rice, sakura + sesame).
- **Controls:** stick or WASD to move; A/Space dash, X/E carry, Y/1 yay, B/2 bonk, RB/C camera, LB/V skin. On touch, drag on the left and use the buttons.
- **Frames:** `../_concept/look-test/`. Test hook: `window.__look.step(frames)`.

## sushi-ladder/: cozy kitchen toy (kaiten shift)

One-button simplified Overcooked: one 4-minute "day" (11 AM to 9 PM) at a conveyor-belt sushi bar for 1 to 4 cooks.

- **Run:** the rig serves this folder all the time. A Task Scheduler task, "Bed of Rice toys server", starts it at logon and checks every 5 minutes, starting it again if it has stopped. It runs hidden (`conhost --headless python -m http.server 5181 --bind 0.0.0.0`), so no window appears. Open `http://localhost:5181/sushi-ladder/`. The `bedofrice-toys` entry in `.claude/launch.json` only attaches to it. To stop or start it by hand, use `Stop-ScheduledTask` or `Start-ScheduledTask -TaskName 'Bed of Rice toys server'`. Elsewhere: `python -m http.server 5181 --bind 0.0.0.0 --directory projects/bedofrice.com/_toys`.
- **Other devices on the network:** `http://10.0.0.130:5181/sushi-ladder/` (home Wi-Fi) or `http://100.84.97.111:5181/sushi-ladder/` (Tailscale). Windows may ask once to let Python through the firewall.
- **Join:** each player presses their button. Controller: stick + A (any face button). Keyboard: WASD + Space, or arrows + Enter. Touch: left thumb moves, right thumb is the button.
- **Open the shop:** walk to the sign (top right) and press. The Start button on a controller does it too.
- **The button:** tap picks up, puts down or serves. Hold slices on the board. A tap with nothing in reach dashes (empty-handed) or throws what you carry, and a teammate can catch it.
- **Loop:** raw rice goes in the cooker (6 s, crispy okoge after 12 s more, +8 tip). Fish goes on the board (hold 1.4 s to slice). A plate needs rice plus a topping. Put the plate on the belt and the guest who ordered it takes it.
- **Tips:** 20 + speed bonus. Hand-off ×1.5 when two cooks contributed to the plate. Stars at 150 / 300 / 450, scaled up for more players.
- **Tuning knobs:** the constants near the top of the script (`SPEED`, `DAY`, `COOK`, `OKOGE`, `SLICE`, `STEP`, `PATIENCE`).
- **Testing:** `window.__toy.step(frames)` advances the sim by hand, which is handy when the tab is in the background.
