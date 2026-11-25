# Bed of Rice toys

Rough playable sketches for trying game directions before the Godot build. They're plain HTML/JS with no build step. The `_` prefix keeps them off the public site, because GitHub Pages' Jekyll skips underscore folders.

## sushi-ladder/: cozy kitchen toy (kaiten shift)

One-button simplified Overcooked: one 4-minute "day" (11 AM to 9 PM) at a conveyor-belt sushi bar for 1 to 4 cooks.

- **Run:** from the claude repo root, `python -m http.server 5181 --bind 0.0.0.0 --directory projects/bedofrice.com/_toys` (or the `bedofrice-toys` entry in `.claude/launch.json`). Then open `http://localhost:5181/sushi-ladder/`.
- **Other devices on the network:** `http://10.0.0.130:5181/sushi-ladder/` (home Wi-Fi) or `http://100.84.97.111:5181/sushi-ladder/` (Tailscale). Windows may ask once to let Python through the firewall.
- **Join:** each player presses their button. Controller: stick + A (any face button). Keyboard: WASD + Space, or arrows + Enter. Touch: left thumb moves, right thumb is the button.
- **Open the shop:** walk to the sign (top right) and press. The Start button on a controller does it too.
- **The button:** tap picks up, puts down or serves. Hold slices on the board. A tap with nothing in reach dashes (empty-handed) or throws what you carry, and a teammate can catch it.
- **Loop:** raw rice goes in the cooker (6 s, crispy okoge after 12 s more, +8 tip). Fish goes on the board (hold 1.4 s to slice). A plate needs rice plus a topping. Put the plate on the belt and the guest who ordered it takes it.
- **Tips:** 20 + speed bonus. Hand-off ×1.5 when two cooks contributed to the plate. Stars at 150 / 300 / 450, scaled up for more players.
- **Tuning knobs:** the constants near the top of the script (`SPEED`, `DAY`, `COOK`, `OKOGE`, `SLICE`, `STEP`, `PATIENCE`).
- **Testing:** `window.__toy.step(frames)` advances the sim by hand, which is handy when the tab is in the background.
