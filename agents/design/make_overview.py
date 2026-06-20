#!/usr/bin/env python3
"""Render a multi-page graphical PDF design overview for the Agentic Research OS."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.backends.backend_pdf import PdfPages

# BC20/ECTA-ish palette
RED   = (0.70, 0.11, 0.11)
BLUE  = (0.00, 0.20, 0.42)
GREEN = (0.11, 0.35, 0.02)
GREY  = (0.45, 0.45, 0.45)
LBLUE = (0.86, 0.91, 0.97)
LGREY = (0.93, 0.93, 0.93)
LGREEN= (0.88, 0.93, 0.84)
LRED  = (0.97, 0.88, 0.88)
INK   = (0.12, 0.12, 0.14)

def box(ax, x, y, w, h, text, fc=LGREY, ec=INK, fs=10, weight="normal", tc=INK, lw=1.3, rad=0.04):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.01,rounding_size={rad}",
                       fc=fc, ec=ec, lw=lw, zorder=2)
    ax.add_patch(p)
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=fs,
            color=tc, weight=weight, zorder=3, wrap=True)
    return (x+w/2, y+h/2, x, y, w, h)

def arrow(ax, p0, p1, color=GREY, lw=1.6, style="-|>", ls="-", rad=0.0):
    a = FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=14,
                        lw=lw, color=color, zorder=1,
                        connectionstyle=f"arc3,rad={rad}", linestyle=ls)
    ax.add_patch(a)

def newpage(pdf, title, subtitle=None):
    fig, ax = plt.subplots(figsize=(11.69, 8.27))  # A4 landscape
    ax.set_xlim(0, 100); ax.set_ylim(0, 72); ax.axis("off")
    ax.text(4, 68.5, title, fontsize=20, weight="bold", color=INK)
    if subtitle:
        ax.text(4, 65.2, subtitle, fontsize=11, color=GREY)
    ax.plot([4, 96], [63.8, 63.8], color=INK, lw=1.0)
    return fig, ax

pdf = PdfPages("agentic_research_os.pdf")

# ----------------------------------------------------------------------------
# PAGE 1 — Hub-and-spoke: the fleet around the ledger, dashboard = this chat
# ----------------------------------------------------------------------------
fig, ax = newpage(pdf, "Agentic Research OS — what it ends up like",
                  "One git-backed ledger. A fleet of background agents. This chat is the dashboard.")

# central ledger
cx, cy = 50, 29
box(ax, cx-11, cy-6, 22, 12, "research-ledger.json\n(one source of truth)\nproof · compute · figure\nliterature · writing · decision",
    fc=LBLUE, ec=BLUE, fs=10, weight="bold", tc=BLUE)

# agents around it
agents = [
    ("Compute agent\nrequeue · extract · gate ‖F‖<1e-20", 10, 43, LGREEN, GREEN),
    ("Figure agent\nregen from pool · kill placeholders", 10, 28, LGREEN, GREEN),
    ("Literature agent\nfind · verify citations", 10, 13, LGREY, GREY),
    ("Proof agent\nstep-check · find gaps · draft fixes", 68, 43, LRED, RED),
    ("Writing/QA agent\nmake stale · checklists", 68, 13, LGREY, GREY),
]
for txt, x, y, fc, ec in agents:
    c = box(ax, x, y, 22, 9, txt, fc=fc, ec=ec, fs=9)
    # arrow to/from ledger center
    arrow(ax, (c[0], c[1]), (cx, cy), color=ec, lw=1.5, style="<|-|>", rad=0.05)

# dashboard / this chat on top
dash = box(ax, cx-13, 50.5, 26, 6.0, "DASHBOARD  =  this chat\nreads ledger + open PRs  →  daily digest",
           fc=(1,1,1), ec=INK, fs=10, weight="bold")
arrow(ax, (cx, 50.5), (cx, cy+6), color=INK, lw=2.0, style="<|-|>")

# researcher
you = box(ax, cx-10, 58.0, 20, 3.8, "YOU — a few prompts / day", fc=(1,0.97,0.86), ec=RED, fs=10, weight="bold", tc=RED)
arrow(ax, (cx, 58.0), (cx, 56.5), color=RED, lw=2.0, style="<|-|>")

# legend
ax.text(4, 7.5, "git is the message bus", fontsize=9, color=GREY, style="italic")
ax.text(4, 5.0, "■ auto-merge on green CI", fontsize=9, color=GREEN)
ax.text(34, 5.0, "■ human-gated (you approve)", fontsize=9, color=RED)
ax.text(70, 5.0, "■ notes / low-risk", fontsize=9, color=GREY)
pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

# ----------------------------------------------------------------------------
# PAGE 2 — Liveness: how agents don't fall asleep
# ----------------------------------------------------------------------------
fig, ax = newpage(pdf, "Liveness — how agents don't fall asleep",
                  "Containers are ephemeral. Agents are resumable + externally woken, never long-lived.")

# timeline bar
ax.text(6, 58, "1.  Cron heartbeat", fontsize=13, weight="bold", color=GREEN)
ax.text(6, 55, "GitHub Actions wakes each agent on a schedule (compute */5 min, literature weekly).", fontsize=10, color=INK)
ax.text(6, 52.5, "A dead container doesn't matter — the next tick spins up a fresh one.", fontsize=10, color=GREY)
# ticks
y=46
for i in range(9):
    x = 8 + i*10
    ax.add_patch(Circle((x, y), 0.7, fc=GREEN, ec=GREEN, zorder=3))
    if i < 8:
        arrow(ax, (x+0.8, y), (x+9.2, y), color=GREEN, lw=1.4)
    ax.text(x, y-2.4, f"t{i}", fontsize=8, color=GREY, ha="center")
ax.text(8, y+2.2, "wake → read ledger → claim → work → commit → die", fontsize=9, color=GREEN, style="italic")

ax.text(6, 38, "2.  Event wake-ups", fontsize=13, weight="bold", color=BLUE)
ax.text(6, 35, "PR comments, CI results, pushes wake the right agent instantly via webhooks —", fontsize=10, color=INK)
ax.text(6, 32.5, "bursts handled between heartbeats, not held until the next tick.", fontsize=10, color=GREY)

ax.text(6, 26, "3.  Self-scheduled check-ins", fontsize=13, weight="bold", color=RED)
ax.text(6, 23, "For 'come back in an hour and re-verify', an agent re-arms a timer before its container dies.", fontsize=10, color=INK)

# the why-it-works box
box(ax, 58, 12, 38, 14,
    "Why a fresh wake-up never loses work:\n\nALL STATE LIVES IN THE LEDGER,\nNOT IN THE SESSION.\n\nBoot → read ledger → see ready/claimed/stale → resume.\nStale claims (died mid-task) auto-release after 15 min.",
    fc=LBLUE, ec=BLUE, fs=10, weight="bold", tc=BLUE)
ax.text(6, 17, "state is durable", fontsize=11, weight="bold", color=INK)
ax.text(6, 12.5, "session = disposable\nledger = permanent", fontsize=10, color=GREY)
arrow(ax, (26, 14), (57, 18), color=INK, lw=1.6, style="-|>", rad=-0.1)
pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

# ----------------------------------------------------------------------------
# PAGE 3 — Where it lives + rollout
# ----------------------------------------------------------------------------
fig, ax = newpage(pdf, "Where it lives & the rollout",
                  "A 4th pillar in Standards, consumed by MIWN. Built generic from day one.")

# Standards pillars
box(ax, 6, 48, 88, 12, "", fc=(1,1,1), ec=INK, lw=1.4)
ax.text(8, 57.5, "Standards  (the hub — single source of truth, owner-merge only)", fontsize=11, weight="bold", color=INK)
pillars = [("writing/", "figures ✓  proofs+refs: NEW", LGREY, GREY),
           ("methods/", "solver · precision policy", LGREY, GREY),
           ("runner/", "compute jobs · dashboard ✓", LGREEN, GREEN),
           ("agents/  ← NEW", "ledger · fleet · autonomy", LBLUE, BLUE)]
for i,(t,s,fc,ec) in enumerate(pillars):
    x = 9 + i*21.5
    box(ax, x, 49.5, 19, 6, f"{t}\n{s}", fc=fc, ec=ec, fs=8.5,
        weight="bold" if "NEW" in t else "normal", tc=ec)

# consume arrow
box(ax, 35, 38, 30, 5.5, "MIWN  (canonical project — consolidate here)", fc=(1,0.97,0.86), ec=RED, fs=10, weight="bold", tc=RED)
arrow(ax, (50, 49.5), (50, 43.5), color=INK, lw=1.8, style="-|>")
ax.text(52, 46, "vendored as submodule", fontsize=8, color=GREY)

# rollout phases
phases = [
    ("1", "Scaffold the pillar (schema + autonomy + dashboard). No behavior yet.", GREEN),
    ("2", "Compute agent → absorbs the manual rerun scripts. Proves the loop.", GREEN),
    ("3", "Figure agent (gate already done).", GREEN),
    ("4", "Write proof + reference gates, then proof & literature agents.", GREY),
    ("5", "Writing/QA agent + scheduled morning digest.", GREY),
    ("6", "Migrate REZN proofs/manuscript into MIWN (consolidation).", GREY),
]
ax.text(6, 32, "Rollout — each phase small, ships value", fontsize=12, weight="bold", color=INK)
y = 28
for num, txt, col in phases:
    ax.add_patch(Circle((8, y+0.6), 1.2, fc=col, ec=col, zorder=3))
    ax.text(8, y+0.6, num, fontsize=9, color="white", weight="bold", ha="center", va="center", zorder=4)
    ax.text(11, y+0.6, txt, fontsize=10, color=INK, va="center")
    if num != "6":
        arrow(ax, (8, y-0.6), (8, y-3.4), color=GREY, lw=1.2)
    y -= 4

# autonomy mini-legend
box(ax, 70, 6, 26, 18,
    "Tiered autonomy\n\nAUTO-MERGE (green CI):\nfigures · requeues · lit notes · pins\n\nYOU APPROVE:\nproofs · prose · methods · Standards",
    fc=LGREY, ec=INK, fs=9, weight="normal")
pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)

pdf.close()
print("wrote agentic_research_os.pdf")
