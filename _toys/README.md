# Bed of Rice toys

Rough playable sketches for trying game directions before the Godot build. They're plain HTML/JS with no build step. The `_` prefix keeps them off the public site, because GitHub Pages' Jekyll skips underscore folders.

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
