# Authority as Code — the Sandbox Kit Spec (40-min deck)

A 40-minute talk on the [Docker Sandbox Kit Specification v3](../README.md), in
the new Docker **/Next** theme. Full-bleed slides in the Labspace/Simspace
`kind: slides` format — the same shape as the *Securing the Agentic Stack*
workshop deck, so it sits native next to it.

Design language: navy `#0B1533` ink, one Docker-blue (`#1D63ED`) accent,
concept diagrams instead of bullet dumps — green = allowed/pass, red =
ungoverned/danger, amber = gate. Non-AI theme: whales and containers, no robots.

## What's here

| File | What it is |
|---|---|
| `theme.py` | Shared palette, primitives (cards, zones, arrows, the Docker mark) and the cover/section/content/statement frames. |
| `build.py` | One generator per slide → SVG → PNG → `.webp`. `SLIDES` is the running order. |
| `gen_deck.py` | Writes `deck.md`: full-bleed `<img>` per slide + `Note:` speaker notes. |
| `labspace.yaml` | The `kind: slides` descriptor Labspace/Simspace reads. |
| `deck.md` | Generated deck (do not hand-edit — regenerate from `gen_deck.py`). |
| `assets/slide-NN.webp` | Rendered slides (36). `assets/svg/` holds the intermediate SVG/PNG. |

## Rebuild

```sh
# needs rsvg-convert + cwebp on PATH (brew install librsvg webp)
cd presentation
python3 build.py       # re-render every slide to assets/*.webp
python3 gen_deck.py    # regenerate deck.md (alt text + speaker notes)
```

Edit a slide by editing its generator in `build.py` (e.g. `s17_permission_slip`),
then re-run `build.py`. Edit its narration in the `SLIDES` list in `gen_deck.py`,
then re-run `gen_deck.py`.

## Running order (36 slides, ~5 acts)

1. **The boundary** — container vs agent · the paradox · container → containment · four open questions
2. **From Dockerfile to Kit** — the Dockerfile gap · config as debt · one image, one digest · anatomy · two kinds · it just works
3. **Authority as code** — the permission slip · can/can't · asks not grants · proxy-managed creds · composition · strict · the diff is the review · gating
4. **A spec, not a feature** — vendor-neutral · additive types · beyond agents · **what v3 fixes** · **why migrate v2 → v3**
5. **Try it** — the road · the commands · recap · resources

The **what v3 fixes** and **why migrate** slides draw directly on the maintainer
walkthrough: v2's confusing metadata/template decoupling, mixins that couldn't
ship binaries (slow startup), and a closed capability schema — all addressed by
"a kit is one OCI image", mixins-as-layers, and an open, versioned capability
grammar with `provides`/`requires`.

## Present it

Any static host serves it via Labspace, or open the `.webp` files directly. In
Labspace/Simspace, drop this directory in as a `kind: slides` lab; press
<kbd>S</kbd> for the speaker view to see the `Note:` narration.
