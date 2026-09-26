#!/usr/bin/env python3
"""Generate deck.md — full-bleed <img> slides + speaker notes — in the
Labspace/Simspace `kind: slides` format. Slide N maps to assets/slide-NN.webp,
in build.py's SLIDES order.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

SLIDES = [
    ("Sandbox Kits — package your AI agent as one image",
     "Welcome. For the next 40 minutes: one simple idea. You can package an AI agent — and everything it's allowed to touch — as a single Docker image. That's a Sandbox Kit."),
    ("Meet your speaker",
     "Quick hello — I'm Ajeet, a Developer Advocate. By the end you'll know what a Kit is, the five things it does for you, how v3 differs from v2, and how to run one in five minutes."),
    ("The setup — you want an agent to work on your repo",
     "Picture the thing we all want right now: an AI coding agent working on your repo. It installs dependencies and runs your build, it calls the GitHub API with your token to open a PR, and it reads and writes files all over your working copy. Useful — and that's the point."),
    ("So what's the problem?",
     "Here's the catch. That agent runs with all of your authority — it can delete files, hit any URL, spend your cloud budget. The access it needs is scattered across docker run flags, env vars, a wiki, and your memory. And your real token is sitting right inside the container, one prompt-injection away from leaking. Nothing says what it should NOT do."),
    ("What's a Kit?",
     "So let's fix that. What's a Kit? The whole idea fits in one picture."),
    ("A Kit is a normal Docker image that declares what the agent may do",
     "This is the one-liner to remember. A Kit is a normal Docker image that also declares what the agent is allowed to do. You build it, push it, and pull it like any other image."),
    ("Anatomy of a Kit — content plus the rules, one digest",
     "There's nothing new to learn, because it's just an OCI image. The layers carry the content — the agent, the tools, the config. A manifest annotation carries the rules — network policy, credentials, volumes. Content plus rules, one digest, and the rules travel with the thing they describe. No sidecar, no second file."),
    ("Two pieces — a workload runs; mixins add to it",
     "A Kit comes in two flavours. A workload is the thing that runs — the base environment, like a shell — and you get exactly one. Mixins add to it: the Claude agent, a real CLI like gh, a network rule. Zero or more, stacked in any number. Together they assemble into one image that sbx runs as a sandbox."),
    ("You already know the tools — it's just an image",
     "And because it's just an image, you already know the tools. docker build makes a kit anywhere, even in CI. docker push shares it on any registry. docker pull grabs someone else's. You can even FROM one. A registry that's never heard of Kits stores it correctly."),
    ("Five things a Kit does for you",
     "Now the part developers actually feel — five concrete things a Kit does for you."),
    ("#1 Locks the network — talks to what you allow, nothing else",
     "Number one: it locks the network. The agent talks to what you allow — github.com — and everything else is simply blocked. It's one list in the descriptor. If it isn't allowed, it doesn't happen."),
    ("#2 Hides your secrets — the agent never sees your real token",
     "Number two, and my favourite: it hides your secrets. Inside the sandbox the agent only ever sees a decoy token. The real token lives at the boundary, which swaps the decoy for the real value on the way out — so api.github.com sees a real request, but leaked logs, prompt-injection, or a rogue tool all get the fake."),
    ("#3 Ships tools as fast layers — no slow install script",
     "Number three: it ships tools as fast layers. Want the GitHub CLI? It's dropped in as a cached layer — instantly ready. In v2, mixins ran apt-get on every start, which made startup slow every single time. In v3 it's just a layer."),
    ("#4 Composes cleanly — stack kits, sbx works out the order",
     "Number four: it composes cleanly. Stack a shell, Claude, and gh; each declares what it provides and requires, and sbx works out the order. You never order flags by hand, and the same set always produces the same image — lockable and cacheable."),
    ("#5 Reviews itself in a PR — more access shows up as a diff",
     "Number five: it reviews itself. When the next version wants a new host or a new credential, that shows up as added lines in a pull request. It's not a code change — it's a change in access — so it can stop for approval, and it travels with the kit."),
    ("Show me the file — the gh mixin as a permission slip",
     "Here's a real one — the gh mixin, read like a permission slip. It reaches GitHub and nowhere else, it can't delete repos because deny always wins, the token stays hidden behind the proxy, and it declares gh@2.72.0 so other kits can require it. That's the whole contract, in one readable file."),
    ("How is v3 different from v2?",
     "If you've written a kit before, this next part is for you — how v3 differs from v2."),
    ("v2 to v3, side by side",
     "Side by side. A v2 kit was a spec.yaml plus a separately-built image you kept in sync by hand, with a patchwork of bespoke blocks — permissions, credentials, volumes, ports, setup hooks, environment — and identity was a mutable name. v3 collapses all of it into one OCI image and one typed, versioned capabilities list, with identity as the digest-pinned reference. Same asks, now in one place."),
    ("Why v3 is better — three fixes from the maintainer",
     "Why is that better? Three problems, straight from the maintainer. One: v2 split a kit's metadata from a separate 'template' image — confusing; v3 is all one image. Two: v2 mixins ran apt-get in a hook — slow; v3 tools are cached layers. Three: v2 hard-coded network, creds and context into the grammar; v3 lets new capabilities plug in. Plus provides/requires, so sbx verifies the whole set before it runs."),
    ("Migrating a kit — a rename and a reshape",
     "Migrating is a rename and a reshape, not a rewrite. kind: sandbox becomes kind: workload with a Dockerfile recipe. setup hooks become the lifecycle capability. permissions, credentials and volumes become one capabilities list. One caveat: don't mix — v3 kits can't compose with v1 or v2. The claude example in the repo is a real v2 kit, ported."),
    ("Get started",
     "Let's actually run one. Five minutes, start to finish."),
    ("Install and run — a published kit, no build needed",
     "Install sbx with brew. Then run a published kit — no build needed: a shell workload with the Claude mixin overlaid, and you've got Claude Code, boxed and scoped. The exact same references run in the cloud with sbx --cloud."),
    ("The local loop — point sbx at a folder",
     "For authoring, there's the local loop. Point sbx at the kit folders — no registry, no push — and it builds on demand, keyed by source hash. Edit hello.yaml, re-run, and only hello rebuilds; the rest is reused from cache. It's the tightest edit loop you can get."),
    ("Demo",
     "Let's see it live. [Run: sbx run docker/sbx-kit-shell:1.0.0 --kit docker/sbx-kit-claude-mixin . — show the sandbox come up, the agent working, and the network/credential boundary in action.]"),
    ("In one line — build, share, and review",
     "To wrap: your agent's environment plus its permissions, in one image you can build, share, and review. Dockerfiles ship your app; Kits ship what it's allowed to do."),
    ("Take it home — everything is open",
     "Everything's open under Apache-2.0: the spec and examples in docker/sandbox-kit-spec, install docs on Docker Docs, Verified Publisher kits on Docker Hub, and a field-by-field v2 to v3 mapping. It's experimental, with a final v3 targeted for Q4 2026 — so try it and open issues."),
    ("Thank you",
     "Thank you. Ship agents like you ship software — with the permissions in the artifact. Happy to take questions."),
]

IMG = ('<img src="assets/slide-{n:02d}.webp" alt="{alt}" width="1600" height="900" '
       '{load}decoding="async" style="position:absolute;inset:0;width:100%;height:100%;'
       'max-width:none;max-height:none;object-fit:fill" />')


def esc(s):
    return s.replace('"', '&quot;')


def main():
    out = []
    for i, (alt, note) in enumerate(SLIDES, 1):
        load = ('loading="eager" fetchpriority="high" ' if i == 1 else 'loading="lazy" ')
        block = ["<!-- chrome: false -->", "",
                 IMG.format(n=i, alt=esc(alt), load=load)]
        if note:
            block += ["", f"Note: {note}"]
        out.append("\n".join(block))
    deck = "\n\n---\n\n".join(out) + "\n"
    with open(os.path.join(HERE, "deck.md"), "w") as f:
        f.write(deck)
    print(f"deck.md — {len(SLIDES)} slides")


if __name__ == "__main__":
    main()
