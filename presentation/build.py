#!/usr/bin/env python3
"""Build the "Sandbox Kits" deck — developer-first, plain language, block
diagrams, in the dark IBM Plex Mono Docker /Next theme.

    python3 build.py      # -> assets/slide-NN.webp  (+ assets/svg/*.png)
Needs: rsvg-convert, cwebp.
"""
import os
import subprocess
import theme as T
from theme import (t, rect, line, arrow, check, cross, pill, docker_mark,
                   card_hard, blue_card, block, bullets, chips,
                   cover, section, content, light, statement)

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
SVGDIR = os.path.join(ASSETS, "svg")
CHIP = ["1", "2", "3", "4", "5"]


def term(x, y, w, h, title, lines):
    """Dark terminal/editor card with a title bar + mono lines."""
    b = [rect(x+8, y+10, w, h, T.SHADOW, rx=14),
         rect(x, y, w, h, "#0A1222", rx=14, stroke="#243busted" if False else "#26355a", sw=1.6),
         rect(x, y, w, 42, "#16233d", rx=14),
         rect(x, y+22, w, 20, "#16233d")]
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        b.append(f'<circle cx="{x+24+i*22}" cy="{y+21}" r="6" fill="{c}"/>')
    b.append(t(x+w-18, y+27, title, 14, T.SKY, 600, anchor="end"))
    yy = y + 82
    for ln in lines:
        txt, col, wt = (ln + (400,))[:3] if isinstance(ln, tuple) else (ln, "#C7D5F2", 400)
        b.append(t(x+26, yy, txt, 19, col, wt))
        yy += 32
    return "".join(b)


# ============================================================================
def s01_cover():
    return cover("WEAREDEVELOPERS 2026   ·   DOCKER / NEXT",
                 ["Sandbox Kits"],
                 "Package your AI agent — and everything it's allowed to touch — as one image.",
                 foot_tag="sbx  ·  Kit spec v3")


def s02_speaker():
    b = T._dark_base(glow=False)
    b.append(t(70, 120, "Whale, hello there.", 18, T.SKY, 700))
    b.append(t(70, 170, "Meet your speaker", 46, T.WHITE, 700))
    # speaker card
    b.append(card_hard(90, 260, 720, 380))
    b.append(f'<circle cx="200" cy="380" r="66" fill="{T.BLUE}"/>')
    b.append(t(200, 398, "AR", 44, T.WHITE, 700, anchor="middle"))
    b.append(t(300, 360, "Ajeet Singh Raina", 34, T.INK, 700))
    b.append(t(300, 400, "Developer Advocate  ·  @ajeetsraina", 19, T.BLUE, 600))
    b.append(t(120, 500, "20+ years across testing, consulting & DevRel.", 20, T.INK, 500))
    b.append(t(120, 534, "Former Docker Captain; runs a 17,000-member", 20, T.INK, 500))
    b.append(t(120, 568, "Bengaluru meetup. Author of “Operational AI", 20, T.INK, 500))
    b.append(t(120, 602, "with Docker”.", 20, T.INK, 500))
    # takeaways
    b.append(t(880, 320, "You'll leave knowing", 22, T.WHITE, 700))
    b.append(bullets(880, 380, [
        "what a Kit is (it's just an image)",
        "the 5 things it does for you",
        "how v3 differs from v2",
        "how to run one in 5 minutes",
    ], gap=58))
    b.append(T.footer(dark=True))
    return T._svg("".join(b), T.COVER_DEFS)


def s03_setup():
    b = []
    b.append(bullets(70, 280, [
        ("It installs dependencies", "runs your build, edits your code"),
        ("It calls the GitHub API", "with your token, to open a PR"),
        ("It reads and writes files", "all over your working copy"),
    ], gap=104, size=24))
    # right: laptop block with agent reaching out
    b.append(block(900, 250, 560, 400, "", None, "solid"))
    b.append(t(1180, 296, "your laptop", 16, T.MUTE, 600, anchor="middle"))
    b.append(block(1080, 330, 200, 90, "AI agent", None, "blue", tsize=22))
    for lbl, tx, ty in [("files", 950, 470), ("network", 1180, 560), ("your token", 1330, 470)]:
        b.append(arrow(1180, 420, tx+ (0), ty-24, T.SKY, 2.4))
        b.append(block(tx-70, ty-24, 140, 48, lbl, None, "ghost", tsize=15))
    return content("The setup", "You want an AI coding agent to work on your repo.",
                   "".join(b), tag="Why kits")


def s04_problem():
    b = []
    b.append(bullets(70, 270, [
        ("It can do anything you can", "delete files, hit any URL, spend your cloud budget"),
        ("Access is scattered", "docker run flags, env vars, a wiki, your memory"),
        ("Your real token sits inside", "one prompt-injection away from leaking"),
    ], gap=100, size=23, marker=T.RED))
    # messy diagram
    b.append(block(900, 250, 560, 400, "", None, "bad"))
    b.append(t(1180, 296, "today: nothing says “no”", 16, "#ff9e94", 600, anchor="middle"))
    b.append(block(1080, 330, 200, 84, "agent", None, "blue", tsize=22))
    ring = [("rm -rf /", 940, 450), ("any URL", 1330, 450),
            ("$AWS_KEY", 940, 560), ("exfiltrate", 1330, 560)]
    for lbl, tx, ty in ring:
        b.append(arrow(1180, 414, tx, ty-22, T.RED, 2.2))
        b.append(block(tx-80, ty-22, 160, 46, lbl, None, "bad", tsize=15))
    return content("So what's the problem?", "Right now that agent runs with all of your authority.",
                   "".join(b), tag="Why kits")


def s05_sec_what():
    return section(1, ["What's a Kit?"], "The whole idea in one picture.")


def s06_oneliner():
    return statement("THE ONE-LINER",
                     ["A Kit is a normal Docker image", "that also declares what the",
                      "agent is allowed to do."],
                     foot="Build it, push it, pull it — like any other image.")


def s07_anatomy():
    b = []
    # one big image box
    b.append(block(120, 230, 900, 430, "", None, "solid"))
    b.append(t(160, 280, "ONE OCI IMAGE", 16, T.SKY, 700, spacing=2))
    # layers = content
    b.append(block(160, 310, 400, 300, "", None, "ghost"))
    b.append(t(360, 350, "layers", 20, "#c6d2ec", 700, anchor="middle"))
    b.append(t(360, 378, "= the content", 15, T.MUTE2, 400, anchor="middle"))
    for i, lab in enumerate(["agent runtime", "the CLIs / tools", "skills & config"]):
        ly = 400 + i*62
        b.append(rect(190, ly, 340, 46, "#15223d", rx=8, stroke="#31456e", sw=1.4))
        b.append(t(360, ly+29, lab, 16, "#cdd9f2", 500, anchor="middle"))
    # annotation = rules
    b.append(block(590, 310, 400, 300, "", None, "ghost"))
    b.append(t(790, 350, "annotation", 20, "#c6d2ec", 700, anchor="middle"))
    b.append(t(790, 378, "= the rules", 15, T.MUTE2, 400, anchor="middle"))
    for i, lab in enumerate(["network policy", "credentials", "volumes & ports"]):
        ly = 400 + i*62
        b.append(rect(620, ly, 340, 46, "#152a1d", rx=8, stroke=T.GREEN_D, sw=1.4))
        b.append(t(790, ly+29, lab, 16, "#a9e9ba", 500, anchor="middle"))
    # right note
    b.append(t(1080, 340, "content", 26, T.WHITE, 700))
    b.append(t(1080, 376, "+ the rules", 26, T.SKY, 700))
    b.append(t(1080, 420, "one digest.", 22, T.MUTE, 400))
    b.append(pill(1080, 470, 320, 44, "no sidecar, no new file", "#15223d", T.SKY, 15))
    b.append(t(1080, 560, "The rules travel WITH", 18, T.WHITE, 500))
    b.append(t(1080, 586, "the thing they describe.", 18, T.WHITE, 500))
    return content("Anatomy of a Kit", "Nothing new to learn — it's an OCI image.",
                   "".join(b), tag="What's a Kit")


def s08_two_pieces():
    b = []
    # workload
    b.append(block(90, 300, 300, 150, "workload", "shell · the base env", "blue", tsize=26))
    b.append(t(240, 480, "the thing that runs", 15, T.MUTE, 400, anchor="middle"))
    b.append(t(240, 502, "exactly one", 15, T.SKY, 600, anchor="middle"))
    # plus mixins
    b.append(t(430, 385, "+", 44, T.MUTE2, 700, anchor="middle"))
    for i, (nm, sub) in enumerate([("claude", "the agent"), ("gh", "a real CLI"), ("network", "a rule")]):
        mx = 480 + i*175
        b.append(block(mx, 315, 160, 120, nm, sub, "ghost", tsize=22))
    b.append(t=None) if False else b.append(t(740, 480, "mixins — zero or more, stack in any number", 15, T.MUTE, 400, anchor="middle"))
    # arrow to assembled
    b.append(arrow(1015, 500, 1015, 560, T.MUTE2, 3))
    b.append(block(760, 570, 520, 110, "one assembled image", "sbx run  →  a sandbox", "good", tsize=24))
    return content("Two pieces", "A workload runs; mixins add to it.",
                   "".join(b), tag="What's a Kit")


def s09_just_image():
    b = []
    cmds = [("docker build", "make a kit anywhere, even CI"),
            ("docker push", "share it on any registry"),
            ("docker pull", "grab someone else's kit"),
            ("FROM <kit>", "build on top of one")]
    for i, (c, sub) in enumerate(cmds):
        cx = 70 + (i % 2)*730
        cy = 250 + (i // 2)*170
        b.append(card_hard(cx, cy, 690, 130))
        b.append(check(cx+42, cy+65, 15, T.GREEN))
        b.append(t(cx+78, cy+58, c, 26, T.INK, 700))
        b.append(t(cx+78, cy+92, sub, 17, T.INKSUB, 400))
    b.append(t(70, 660, "A registry that has never heard of Kits stores one correctly — it's just an image.",
               20, T.MUTE, 400))
    return content("You already know the tools", "There's no special kit tooling to learn.",
                   "".join(b), tag="What's a Kit")


def s10_sec_five():
    return section(2, ["Five things a Kit", "does for you"],
                   "The parts developers actually feel.")


def _five_head(n, title):
    return t(70, 108, f"#{n}  {title}", 40, T.WHITE, 700)


def s11_cap_network():
    b = []
    b.append(block(120, 300, 220, 110, "agent", None, "blue", tsize=24))
    b.append(arrow(346, 355, 470, 355, T.GREEN, 3))
    b.append(block(490, 300, 300, 110, "github.com", "allowed ✓", "good", tsize=22))
    b.append(arrow(346, 355, 470, 520, T.RED, 3))
    b.append(block(490, 470, 300, 110, "everything else", "blocked ✗", "bad", tsize=22))
    b.append(term(870, 280, 590, 250, "gh.yaml", [
        ("type: network-policy@2", T.SKY, 600),
        ("allow:", "#9FB6E6", 400),
        ("  - github.com", "#8ff0a6", 600),
        ("  - hosts: [api.github.com]", "#8ff0a6", 600),
    ]))
    b.append(t(870, 590, "One list. If it's not allowed, it doesn't happen.", 19, T.MUTE, 400))
    return content("#1 · Locks the network",
                   "The agent talks to what you allow — and nothing else.",
                   "".join(b), tag="5 things", active_chip=0, chip_labels=CHIP)


def s12_cap_secrets():
    b = []
    b.append(block(90, 320, 330, 150, "sandbox", None, "solid"))
    b.append(rect(120, 380, 270, 60, "#2a2416", rx=8, stroke="#7a6320", sw=1.4))
    b.append(t(255, 418, 'GH_TOKEN = "fake"', 17, T.TAN, 600, anchor="middle"))
    b.append(t(255, 500, "the agent only sees a decoy", 15, T.MUTE, 400, anchor="middle"))
    b.append(arrow(424, 395, 520, 395, T.BLUE, 3))
    b.append(block(540, 320, 320, 150, "the boundary", "holds your real token", "blue", tsize=22))
    b.append(t(700, 500, "swaps the decoy for the real", 15, T.MUTE, 400, anchor="middle"))
    b.append(t(700, 522, "token on the way out", 15, T.MUTE, 400, anchor="middle"))
    b.append(arrow(864, 395, 960, 395, T.GREEN, 3))
    b.append(block(980, 320, 320, 150, "api.github.com", "sees a real request", "good", tsize=22))
    b.append(pill(90, 600, 640, 46, "Leaked logs, prompt-injection, a rogue tool — all get the decoy.",
                  "#15223d", T.SKY, 16))
    return content("#2 · Hides your secrets",
                   "The agent never sees your real token.",
                   "".join(b), tag="5 things", active_chip=1, chip_labels=CHIP)


def s13_cap_layers():
    b = []
    b.append(block(120, 300, 260, 110, "workload", None, "blue", tsize=22))
    b.append(t(250, 470, "base image", 15, T.MUTE, 400, anchor="middle"))
    b.append(t(400, 355, "+", 40, T.MUTE2, 700, anchor="middle"))
    b.append(block(450, 300, 300, 110, "gh binary", "shipped as a layer", "good", tsize=22))
    b.append(arrow(766, 355, 860, 355, T.GREEN, 3))
    b.append(block(880, 300, 300, 110, "tool ready", "instantly", "good", tsize=24))
    b.append(card_hard(120, 500, 700, 150))
    b.append(t(150, 552, "v2 way", 18, T.RED, 700))
    b.append(t(150, 590, "ran  apt-get install  on every start", 20, T.INK, 500))
    b.append(t(150, 622, "— slow sandbox startup, every time.", 18, T.INKSUB, 400))
    b.append(t(900, 560, "v3 way", 18, T.GREEN, 700))
    b.append(t(900, 598, "binary content is a", 20, T.WHITE, 500))
    b.append(t(900, 628, "cached layer. Fast.", 20, T.WHITE, 500))
    return content("#3 · Ships tools as fast layers",
                   "Drop in a CLI as a layer — no slow install script.",
                   "".join(b), tag="5 things", active_chip=2, chip_labels=CHIP)


def s14_cap_compose():
    b = []
    for i, (nm, sub) in enumerate([("shell", "provides shell"), ("claude", "requires shell"), ("gh", "provides gh")]):
        b.append(block(120, 260 + i*115, 300, 90, nm, sub, "solid", tsize=22))
    b.append(arrow(440, 400, 560, 400, T.MUTE2, 3))
    b.append(block(580, 320, 300, 160, "sbx resolves", "the dependency order", "blue", tsize=22))
    b.append(arrow(900, 400, 1020, 400, T.GREEN, 3))
    b.append(block(1040, 320, 380, 160, "one image", "same set → same image", "good", tsize=26))
    b.append(t(120, 640, "You never order the flags by hand — provides / requires do it. Lockable & cacheable.",
               19, T.MUTE, 400))
    return content("#4 · Composes cleanly",
                   "Stack kits; sbx works out the order.",
                   "".join(b), tag="5 things", active_chip=3, chip_labels=CHIP)


def s15_cap_review():
    b = []
    b.append(term(90, 270, 720, 330, "gh-kit  v2 → v3   (a pull request)", [
        ("  network-policy@2:", "#C7D5F2", 400),
        ("      allow:", "#9FB6E6", 400),
        ("        - github.com", "#C7D5F2", 400),
        ("+       - hosts: [pypi.org]", "#8ff0a6", 700),
        ("+         methods: [GET]", "#8ff0a6", 700),
        ("+   credential: npm", "#8ff0a6", 700),
    ]))
    b.append(t(870, 330, "A new host.", 30, T.WHITE, 700))
    b.append(t(870, 372, "A new credential.", 30, T.WHITE, 700))
    b.append(t(870, 428, "Not a code change —", 22, T.MUTE, 400))
    b.append(t(870, 460, "a change in access.", 22, T.TAN, 700))
    b.append(bullets(870, 522, ["shows up as added lines",
                                "can stop for approval",
                                "travels with the kit"], gap=48, size=19))
    return content("#5 · Reviews itself in a PR",
                   "When the agent asks for more, it shows up as a diff.",
                   "".join(b), tag="5 things", active_chip=4, chip_labels=CHIP)


def s16_the_file():
    b = []
    b.append(term(70, 210, 760, 560, "gh.yaml  ·  a mixin", [
        ("kind: mixin", T.SKY, 600),
        ("provides: [\"gh@2.72.0\"]", "#C7D5F2", 400),
        ("", "#fff", 400),
        ("capabilities:", T.SKY, 600),
        ("  - type: network-policy@2", "#C7D5F2", 400),
        ("      allow: [github.com,", "#8ff0a6", 600),
        ("             api.github.com]", "#8ff0a6", 600),
        ("      deny:  DELETE /repos/**", "#ff9e94", 600),
        ("", "#fff", 400),
        ("  - type: credential@1", "#C7D5F2", 400),
        ("      apiKey: GH_TOKEN", "#C7D5F2", 400),
        ("      proxyManaged: true", "#8ff0a6", 600),
    ]))
    notes = [(T.GREEN, "reaches GitHub", "and nowhere else"),
             (T.RED, "can't delete repos", "deny always wins"),
             (T.BLUE, "token stays hidden", "proxy injects the real one"),
             (T.SKY, "declares  gh@2.72.0", "so others can require it")]
    for i, (col, a, bb) in enumerate(notes):
        ny = 250 + i*128
        b.append(card_hard(880, ny, 580, 100, dx=6, dy=8))
        b.append(rect(880, ny, 9, 100, col, rx=4))
        b.append(t(912, ny+44, a, 22, T.INK, 700))
        b.append(t(912, ny+76, bb, 16, T.INKSUB, 400))
    return content("Show me the file", "The gh mixin — read it like a permission slip.",
                   "".join(b), tag="5 things")


def s17_sec_v2v3():
    return section(3, ["How is v3", "different from v2?"],
                   "If you've written a kit before, read this.")


def s18_v2_v3():
    b = []
    # v2 side
    b.append(card_hard(70, 230, 640, 470, fill="#F4F5F8"))
    b.append(t(102, 284, "v2", 22, T.RED, 700))
    b.append(t(150, 284, "spec.yaml  +  a separate image", 18, T.INK, 600))
    b.append(rect(102, 310, 250, 60, "#fff", rx=8, stroke="#d9b3ad", sw=1.5, dash="5 5"))
    b.append(t(227, 348, "spec.yaml", 16, T.INK, 700, anchor="middle"))
    b.append(rect(452, 310, 226, 60, "#fff", rx=8, stroke="#d9b3ad", sw=1.5, dash="5 5"))
    b.append(t(565, 340, "named image", 15, T.INK, 700, anchor="middle"))
    b.append(t(565, 360, "sync by hand", 12, T.RED, 500, anchor="middle"))
    b.append(line(352, 340, 452, 340, "#d6a79f", 1.6, dash="3 5"))
    b.append(t(102, 410, "a patchwork of bespoke blocks:", 14, T.INKSUB, 600))
    for i, bl in enumerate(["permissions", "credentials", "volumes", "ports", "setup hooks", "environment"]):
        bx = 102 + (i % 2)*290
        by = 432 + (i//2)*54
        b.append(rect(bx, by, 278, 42, "#fff", rx=7, stroke="#e0e0e6", sw=1.3))
        b.append(t(bx+14, by+27, bl, 15, T.INK, 500))
    b.append(t(102, 682, "identity = a mutable name:", 14, T.RED, 600))
    # arrow
    b.append(arrow(724, 460, 806, 460, T.SKY, 4))
    b.append(t(765, 438, "collapse", 14, T.SKY, 700, anchor="middle"))
    # v3 side
    b.append(block(820, 230, 640, 470, "", None, "good"))
    b.append(t(852, 284, "v3", 22, T.GREEN, 700))
    b.append(t(900, 284, "one OCI image", 18, T.WHITE, 700))
    b.append(rect(852, 312, 576, 64, "#0A1222", rx=8, stroke="#2b6b3a", sw=1.4))
    b.append(t(870, 342, "content (layers)", 16, "#a9e9ba", 500))
    b.append(t(870, 364, "+ rules (annotation) · one digest", 15, "#8aa596", 400))
    b.append(t(852, 412, "one typed, versioned list:", 14, "#8ff0a6", 600))
    for i, c in enumerate(["network-policy@1", "credential@1", "volume@1", "port@1", "lifecycle@1", "agent-context@1"]):
        bx = 852 + (i % 2)*290
        by = 432 + (i//2)*54
        b.append(rect(bx, by, 278, 42, "#0A1222", rx=7, stroke="#2b6b3a", sw=1.3))
        b.append(check(bx+22, by+21, 9, T.GREEN))
        b.append(t(bx+42, by+27, c, 15, "#cdeed6", 500))
    b.append(t(852, 682, "identity = the digest-pinned reference", 14, "#8ff0a6", 600))
    return content("v2 → v3, side by side", "Same asks — now in one place.",
                   "".join(b), tag="v2 → v3")


def s19_why_better():
    cards = [("ONE IMAGE",
              ["v2 split a kit's metadata", "from a separate “template”", "image. Confusing."],
              "v3: it's all one image."),
             ("FAST MIXINS",
              ["v2 mixins ran apt-get in a", "hook — slow startup, every", "single time."],
              "v3: tools are cached layers."),
             ("OPEN CAPABILITIES",
              ["v2 hard-coded network,", "creds & context into the", "grammar."],
              "v3: new features plug in.")]
    b = []
    for i, (k, probl, fix) in enumerate(cards):
        cx = 70 + i*480
        b.append(card_hard(cx, 240, 450, 380))
        b.append(t(cx+30, 296, "v2 · " + k, 15, T.RED, 700, spacing=1))
        for j, ln in enumerate(probl):
            b.append(t(cx+30, 340 + j*30, ln, 18, T.INKSUB, 500))
        b.append(rect(cx+30, 452, 390, 2, "#e6e9f0"))
        b.append(f'<circle cx="{cx+50}" cy="452" r="16" fill="{T.GREEN}"/>')
        b.append(t(cx+50, 458, "v3", 13, T.WHITE, 700, anchor="middle"))
        b.append(t(cx+30, 520, fix, 21, T.INK, 700))
    b.append(rect(70, 654, 1390, 56, "#15223d", rx=12))
    b.append(t(96, 690, "+ provides / requires — sbx verifies the whole set is satisfied before it runs.",
               19, T.WHITE, 500))
    return content("Why v3 is better", "Three problems it fixes — from the maintainer.",
                   "".join(b), tag="v2 → v3")


def s20_migrate():
    b = []
    maps = [("kind: sandbox", "kind: workload", "+ a Dockerfile recipe"),
            ("setup: hooks", "lifecycle@1", "install / startup as a capability"),
            ("permissions / creds / volumes", "capabilities: [ … ]", "one typed, versioned list")]
    for i, (a, bb, sub) in enumerate(maps):
        cy = 270 + i*120
        b.append(block(90, cy, 470, 90, a, None, "bad", tsize=20))
        b.append(arrow(575, cy+45, 675, cy+45, T.SKY, 3))
        b.append(block(690, cy, 470, 90, bb, sub, "good", tsize=20))
    b.append(rect(90, 640, 1070, 60, "#2a1518", rx=12, stroke="#7d2b2b", sw=1.6))
    b.append(cross(126, 670, 13, T.RED))
    b.append(t(158, 677, "Don't mix — v3 kits can't compose with v1 or v2 kits.", 20, "#ff9e94", 600))
    b.append(t(90, 240, "A rename and a reshape, not a rewrite.", 20, T.MUTE, 400))
    return content("Migrating a kit", "The claude example is a real v2 kit, ported.",
                   "".join(b), tag="v2 → v3")


def s21_sec_start():
    return section(4, ["Get started"], "Five minutes, start to finish.")


def s22_install():
    b = []
    b.append(term(70, 230, 820, 300, "terminal", [
        ("# 1 · install (macOS)", "#6E86B8", 400),
        ("brew install docker/tap/sbx", "#C7D5F2", 600),
        ("", "#fff", 400),
        ("# 2 · run a published kit — no build", "#6E86B8", 400),
        ("sbx run docker/sbx-kit-shell:1.0.0 \\", "#8ff0a6", 700),
        ("    --kit docker/sbx-kit-claude-mixin .", "#8ff0a6", 700),
    ]))
    b.append(block(930, 250, 250, 90, "shell", "workload", "blue", tsize=20))
    b.append(t(1195, 300, "+", 34, T.MUTE2, 700, anchor="middle"))
    b.append(block(1210, 250, 250, 90, "claude", "mixin", "ghost", tsize=20))
    b.append(arrow(1195, 360, 1195, 420, T.GREEN, 3))
    b.append(block(930, 430, 530, 100, "a running sandbox", "Claude Code, boxed & scoped", "good", tsize=24))
    b.append(t(70, 600, "Nothing to build. The kit references pull like any image — locally or in the cloud.",
               19, T.MUTE, 400))
    b.append(t(70, 636, "sbx --cloud run …   runs the exact same references on elastic capacity.", 18, T.SKY, 500))
    return content("Install & run", "Run a published kit — no build needed.",
                   "".join(b), tag="Get started")


def s23_local_loop():
    b = []
    b.append(term(70, 230, 760, 300, "terminal", [
        ("cd examples", "#C7D5F2", 600),
        ("sbx run ./hello --kit ./gh .", "#8ff0a6", 700),
        ("", "#fff", 400),
        ("# edit hello.yaml, then re-run:", "#6E86B8", 400),
        ("# only hello rebuilds — the rest", "#6E86B8", 400),
        ("# is reused from cache.", "#6E86B8", 400),
    ]))
    b.append(block(880, 250, 230, 80, "kit folders", "./hello ./gh", "ghost", tsize=18))
    b.append(arrow(1113, 290, 1180, 290, T.MUTE2, 2.6))
    b.append(block(1200, 250, 200, 80, "docker build", None, "solid", tsize=17))
    b.append(arrow(1300, 335, 1300, 385, T.MUTE2, 2.6))
    b.append(block(1200, 390, 200, 80, "image", "cached", "good", tsize=18))
    b.append(arrow(1200, 430, 1113, 430, T.GREEN, 2.6))
    b.append(block(880, 390, 230, 80, "sandbox", "sbx", "blue", tsize=18))
    b.append(t(70, 600, "No registry. No push. Point sbx at a directory and it builds on demand,", 19, T.MUTE, 400))
    b.append(t(70, 632, "keyed by source hash — the tightest edit loop you can get.", 19, T.WHITE, 500))
    return content("The local loop", "Point sbx at a folder — no registry, no push.",
                   "".join(b), tag="Get started")


def s24_demo():
    b = [t(90, 400, "Demo", 96, "#101A2E", 700)]
    b.append(t(94, 470, "sbx run docker/sbx-kit-shell:1.0.0 --kit docker/sbx-kit-claude-mixin .",
              22, "#1D63ED", 600))
    b.append(t(94, 300, "LIVE", 16, "#1D63ED", 700, spacing=3))
    b.append(rect(90, 320, 60, 5, "#1D63ED"))
    return light("Demo", "".join(b), tag="Get started")


def s25_recap():
    return statement("IN ONE LINE",
                     ["Your agent's environment", "+ its permissions, in one image",
                      "you can build, share, and review."],
                     foot="Dockerfiles ship your app. Kits ship what it's allowed to do.")


def s26_resources():
    b = []
    res = [("THE SPEC", "github.com/docker/", "sandbox-kit-spec", "grammar · schema · examples"),
           ("INSTALL sbx", "docs.docker.com/ai/", "sandboxes/install", "local + cloud, stable line"),
           ("BROWSE KITS", "hub.docker.com", "type=sbx_kit", "Verified Publisher v3 kits"),
           ("MIGRATE", "sandbox-kit-spec /", "migrate-kit-to-v3", "the field-by-field mapping")]
    for i, (k, a, bb, sub) in enumerate(res):
        cx = 70 + (i % 2)*730
        cy = 240 + (i//2)*180
        b.append(card_hard(cx, cy, 690, 150))
        b.append(t(cx+30, cy+50, k, 15, T.BLUE, 700, spacing=1))
        b.append(t(cx+30, cy+90, a, 19, T.INK, 600))
        b.append(t(cx+30, cy+118, bb, 19, T.BLUE, 700))
        b.append(t(cx+400, cy+90, sub, 15, T.INKSUB, 400))
    return content("Take it home", "Everything is open, under Apache-2.0. Experimental — final v3 targeted Q4 2026.",
                   "".join(b), tag="Resources")


def s27_thanks():
    b = T._dark_base()
    b.append(docker_mark(700, 250, 200, T.WHITE, 0.14))
    b.append(t(120, 430, "Thank you.", 72, T.WHITE, 700))
    b.append(line(124, 470, 360, 470, T.BLUE, sw=6))
    b.append(t(124, 528, "Ship agents like you ship software —", 25, T.MUTE, 400))
    b.append(t(124, 564, "with the permissions in the artifact.", 25, T.SKY, 600))
    b.append(t(124, 660, "github.com/docker/sandbox-kit-spec", 20, T.MUTE, 500))
    b.append(T.footer(dark=True))
    return T._svg("".join(b), T.COVER_DEFS)


SLIDES = [
    s01_cover, s02_speaker, s03_setup, s04_problem,
    s05_sec_what, s06_oneliner, s07_anatomy, s08_two_pieces, s09_just_image,
    s10_sec_five, s11_cap_network, s12_cap_secrets, s13_cap_layers, s14_cap_compose, s15_cap_review, s16_the_file,
    s17_sec_v2v3, s18_v2_v3, s19_why_better, s20_migrate,
    s21_sec_start, s22_install, s23_local_loop, s24_demo, s25_recap, s26_resources, s27_thanks,
]


def main():
    os.makedirs(SVGDIR, exist_ok=True)
    for i, fn in enumerate(SLIDES, 1):
        svg = fn()
        base = f"slide-{i:02d}"
        svgp = os.path.join(SVGDIR, base + ".svg")
        pngp = os.path.join(SVGDIR, base + ".png")
        webp = os.path.join(ASSETS, base + ".webp")
        with open(svgp, "w") as f:
            f.write(svg)
        subprocess.run(["rsvg-convert", "-w", "1600", "-h", "900", svgp, "-o", pngp], check=True)
        subprocess.run(["cwebp", "-quiet", "-q", "92", pngp, "-o", webp], check=True)
        print(f"{base}  {fn.__name__}")
    print(f"\n{len(SLIDES)} slides -> {ASSETS}")


if __name__ == "__main__":
    main()
