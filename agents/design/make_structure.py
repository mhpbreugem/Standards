#!/usr/bin/env python3
"""Clean structure diagram: consolidation onto MIWN + the agentic loop."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib.backends.backend_pdf import PdfPages

INK   = (0.11, 0.11, 0.14)
BLUE  = (0.09, 0.22, 0.37)
GREEN = (0.12, 0.40, 0.20)
RED   = (0.55, 0.13, 0.13)
GREY  = (0.46, 0.46, 0.52)
LINE  = (0.80, 0.82, 0.86)
ZONE  = (0.972, 0.976, 0.984)
LBLUE = (0.89, 0.93, 0.97)
LGREEN= (0.89, 0.94, 0.88)
LRED  = (0.97, 0.90, 0.90)
LGREY = (0.935, 0.94, 0.95)
WHITE = (1, 1, 1)

def rbox(ax, x, y, w, h, fc, ec, lw=1.3, rad=0.7, z=3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.02,rounding_size={rad}",
                                fc=fc, ec=ec, lw=lw, zorder=z))

def txt(ax, x, y, s, fs=9, c=INK, w="normal", ha="center", va="center", z=5):
    ax.text(x, y, s, fontsize=fs, color=c, weight=w, ha=ha, va=va, zorder=z)

def arrow(ax, p0, p1, c=GREY, lw=1.7, style="-|>", rad=0.0, ms=14, ls="-", z=2):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, lw=lw,
                                 color=c, zorder=z, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}"))

def chip(ax, x, y, w, h, title, sub, fc, ec, tfs=9.4, sfs=7.6):
    rbox(ax, x, y, w, h, fc, ec, lw=1.4, rad=0.45)
    txt(ax, x+2.2, y+h-1.8, title, fs=tfs, c=ec, w="bold", ha="left")
    txt(ax, x+2.2, y+1.7, sub, fs=sfs, c=INK, ha="left")

pdf = PdfPages("miwn_structure.pdf")
fig, ax = plt.subplots(figsize=(16.0, 9.6))
ax.set_xlim(0, 160); ax.set_ylim(0, 96); ax.axis("off")
fig.patch.set_facecolor("white")

# ---------- title ----------
txt(ax, 5, 92.5, "Market Inefficiency Without Noise — the research stack", fs=21, c=INK, w="bold", ha="left")
txt(ax, 5, 88.7, "One project repo (MIWN)   ·   one reusable hub (Standards)   ·   a background agent fleet you steer from this chat",
    fs=11, c=GREY, ha="left")

# tier legend (horizontal row, below subtitle, clear of the title)
leg = [(GREEN,"auto-merge"),(RED,"you approve"),(GREY,"low-risk notes")]
lxs = [104, 124, 144]
for (col,lab),lxp in zip(leg, lxs):
    ax.add_patch(Rectangle((lxp, 84.6), 2.0, 2.0, fc=col, ec=col, zorder=5))
    txt(ax, lxp+2.8, 85.6, lab, fs=8.2, c=INK, ha="left")

# =====================================================================
# ZONE 1 — repositories
# =====================================================================
rbox(ax, 4, 49, 152, 34, ZONE, LINE, lw=1.4, rad=1.0, z=1)
txt(ax, 7, 80.6, "1   Repositories — everything consolidates onto MIWN", fs=12.5, c=BLUE, w="bold", ha="left")

# archived sources (left)
txt(ax, 7, 75.6, "ARCHIVED  ·  frozen, read-only history", fs=8.2, c=GREY, w="bold", ha="left")
arch = [
    ("REZN", "theory · proofs · manuscript"),
    ("MIZN", "solver rebuild (strict h = 0)"),
    ("FIXED-POINT-FACTORY", "compute farm → folds into runner"),
]
ay = 67.5
for name, sub in arch:
    rbox(ax, 7, ay, 38, 6.0, LGREY, GREY, lw=1.2, rad=0.4)
    txt(ax, 9, ay+3.9, name, fs=9.2, c=GREY, w="bold", ha="left")
    txt(ax, 9, ay+1.7, sub, fs=7.8, c=GREY, ha="left")
    ay -= 7.2
# fold-in arrow
arrow(ax, (45.5, 60.0), (58.5, 64.0), c=INK, lw=2.0, ms=15, rad=0.05)
txt(ax, 51, 63.3, "fold in", fs=8.2, c=INK, w="bold")

# MIWN (center, prominent)
rbox(ax, 59, 57, 39, 17, LBLUE, BLUE, lw=2.4, rad=0.9)
txt(ax, 78.5, 69.6, "MIWN", fs=19, c=BLUE, w="bold")
txt(ax, 78.5, 65.4, "the one canonical project repo", fs=9.6, c=INK)
txt(ax, 78.5, 61.6, "REZN · MIZN · fixed-point-factory  all live here now", fs=8.2, c=GREY)

# Standards (right)
rbox(ax, 110, 53, 44, 25, WHITE, BLUE, lw=1.8, rad=0.8)
txt(ax, 132, 75.3, "STANDARDS — reusable hub", fs=11.2, c=BLUE, w="bold")
txt(ax, 132, 72.2, "owner · direct-to-main · no side branches", fs=8.0, c=GREY)
pill = [
    ("writing/", "figures ✓ · proofs+refs", LGREY, GREY),
    ("methods/", "solver · ‖F‖ < 1e-20", LGREY, GREY),
    ("runner/", "compute · dashboard", LGREEN, GREEN),
    ("agents/  ★", "ledger · fleet · autonomy", LBLUE, BLUE),
]
pxs = [112.5, 133.0]; pys = [62.5, 55.5]
for i,(t,s,fc,ec) in enumerate(pill):
    px = pxs[i % 2]; py = pys[i // 2]
    chip(ax, px, py, 19.5, 6.0, t, s, fc, ec, tfs=8.8, sfs=7.0)
# submodule arrow Standards -> MIWN
arrow(ax, (110, 65.5), (98, 65.5), c=BLUE, lw=2.0, ms=15)
txt(ax, 104, 67.4, "vendored as", fs=7.6, c=BLUE, ha="center")
txt(ax, 104, 63.6, "submodule", fs=7.6, c=BLUE, ha="center")

# =====================================================================
# ZONE 2 — the agentic loop inside MIWN
# =====================================================================
rbox(ax, 4, 4, 152, 42, ZONE, LINE, lw=1.4, rad=1.0, z=1)
txt(ax, 7, 43.0, "2   Inside MIWN — the loop the agent fleet runs in the background", fs=12.5, c=BLUE, w="bold", ha="left")

# YOU + dashboard
rbox(ax, 7, 33.5, 24, 5.6, (1,0.97,0.86), RED, lw=1.6, rad=0.5)
txt(ax, 19, 36.3, "YOU", fs=11, c=RED, w="bold")
txt(ax, 19, 34.4, "a few prompts / day", fs=8.0, c=RED)
rbox(ax, 6, 22.5, 26, 8.2, WHITE, INK, lw=1.5, rad=0.6)
txt(ax, 19, 28.6, "DASHBOARD = this chat", fs=9.4, c=INK, w="bold")
txt(ax, 19, 25.7, "reads ledger + open PRs\n→ daily digest; asks only on decisions", fs=7.7, c=INK)
arrow(ax, (19, 33.5), (19, 30.7), c=RED, lw=2.0, style="<|-|>", ms=13)

# ledger (center)
rbox(ax, 45, 19, 31, 17, LBLUE, BLUE, lw=2.0, rad=0.8)
txt(ax, 60.5, 33.0, "research-ledger.json", fs=12, c=BLUE, w="bold")
txt(ax, 60.5, 30.0, "one source of truth", fs=8.2, c=GREY)
txt(ax, 60.5, 25.6, "typed items:\nproof · compute · figure\nliterature · writing · decision", fs=8.3, c=INK)
txt(ax, 60.5, 20.6, "status · gate · depends_on", fs=7.4, c=GREY)
arrow(ax, (32, 26.5), (45, 27.5), c=INK, lw=1.8, ms=13)
txt(ax, 38.5, 28.8, "route", fs=7.4, c=GREY)

# fleet (right)
fleet = [
    ("Compute agent", "gate  ‖F‖ < 1e-20", LGREEN, GREEN),
    ("Figure agent", "gate  writing/figures ✓", LGREEN, GREEN),
    ("Literature agent", "gate  writing/references", LGREY, GREY),
    ("Proof agent", "gate  writing/proofs (new)", LRED, RED),
    ("Writing / QA agent", "gate  make stale + checklists", LRED, RED),
]
fy = 34.0; fx = 92; fw = 42; fh = 5.0; step = 6.05
anchor = (76, 27.5)
for name, gate, fc, ec in fleet:
    chip(ax, fx, fy, fw, fh, name, gate, fc, ec, tfs=9.0, sfs=7.3)
    arrow(ax, (fx, fy+fh/2), anchor, c=ec, lw=1.5, style="<|-|>", ms=11, rad=0.04)
    fy -= step
txt(ax, 113, 41.0, "agents open PRs  →  tiered merge", fs=8.4, c=INK, w="bold")

# liveness caption
rbox(ax, 7, 5.0, 79, 3.4, WHITE, LINE, lw=1.0, rad=0.4)
txt(ax, 8.5, 6.7, "Liveness:  cron heartbeat (*/5) + event wake-ups · all state is in the ledger, so any agent that wakes up resumes · stale claims auto-release in 15 min",
    fs=7.6, c=GREY, ha="left")

pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)
pdf.close()
print("wrote miwn_structure.pdf")
