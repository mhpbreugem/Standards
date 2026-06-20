#!/usr/bin/env python3
"""Single-figure summary of the Agentic Research OS and how it lives in Standards."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib.backends.backend_pdf import PdfPages

# palette
RED   = (0.70, 0.11, 0.11)
BLUE  = (0.00, 0.20, 0.42)
GREEN = (0.11, 0.35, 0.02)
GREY  = (0.42, 0.42, 0.45)
INK   = (0.11, 0.11, 0.13)
LBLUE = (0.87, 0.92, 0.97)
LGREY = (0.94, 0.94, 0.95)
LGREEN= (0.88, 0.93, 0.84)
LRED  = (0.97, 0.88, 0.88)
PAPER = (0.985, 0.985, 0.99)
BANDS = (0.965, 0.97, 0.985)

def box(ax, x, y, w, h, text, fc=LGREY, ec=INK, fs=9, weight="normal", tc=INK, lw=1.2, rad=0.5, align="center"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.02,rounding_size={rad}",
                                fc=fc, ec=ec, lw=lw, zorder=3))
    if align == "center":
        ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=fs, color=tc, weight=weight, zorder=4)
    else:
        ax.text(x+1.2, y+h/2, text, ha="left", va="center", fontsize=fs, color=tc, weight=weight, zorder=4)
    return (x+w/2, y+h/2)

def arrow(ax, p0, p1, color=GREY, lw=1.6, style="-|>", ls="-", rad=0.0, ms=13):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, lw=lw,
                                 color=color, zorder=2, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}"))

def band(ax, x, y, w, h, label, fc=BANDS):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.8",
                                fc=fc, ec=(0.78,0.80,0.85), lw=1.3, zorder=1))
    ax.text(x+1.6, y+h-1.6, label, ha="left", va="top", fontsize=10.5, weight="bold", color=GREY, zorder=2)

pdf = PdfPages("agentic_research_os_summary.pdf")
fig, ax = plt.subplots(figsize=(16.2, 10.5))
ax.set_xlim(0, 162); ax.set_ylim(0, 105); ax.axis("off")
fig.patch.set_facecolor("white")

# ---- title ----
ax.text(4, 102.5, "Agentic Research OS", fontsize=23, weight="bold", color=INK)
ax.text(4, 99.0, "One git-backed ledger · a fleet of background agents · this chat is the dashboard",
        fontsize=11, color=GREY)

# autonomy legend (top-right)
lx = 138
ax.add_patch(Rectangle((lx, 99.6), 2.2, 2.2, fc=GREEN, ec=GREEN)); ax.text(lx+3, 100.7, "auto-merge on green CI", fontsize=8.5, va="center", color=INK)
ax.add_patch(Rectangle((lx, 96.4), 2.2, 2.2, fc=RED, ec=RED));     ax.text(lx+3, 97.5, "you approve (one click)", fontsize=8.5, va="center", color=INK)
ax.add_patch(Rectangle((lx+0.0, 93.2), 2.2, 2.2, fc=GREY, ec=GREY)); ax.text(lx+3, 94.3, "low-risk notes / shared", fontsize=8.5, va="center", color=INK)

# =====================================================================
# BAND A — STANDARDS (the hub)
# =====================================================================
band(ax, 4, 76, 154, 16.5, "STANDARDS  —  single source of truth   (work on a feature branch · owner merges main · back-port, don't fork)")
pillars = [
    ("writing/", "figures ✓\nproofs + references  (new gates)", LGREY, GREY),
    ("methods/", "solver core\nprecision  ‖F‖ < 1e-20", LGREY, GREY),
    ("runner/", "compute workers\nweb dashboard · git-race lock", LGREEN, GREEN),
    ("agents/   ← NEW", "ledger schema · fleet prompt-packs\nautonomy policy · cron workflow", LBLUE, BLUE),
]
px = 7
for name, sub, fc, ec in pillars:
    ax.add_patch(FancyBboxPatch((px, 78), 36, 11, boxstyle="round,pad=0.02,rounding_size=0.6", fc=fc, ec=ec, lw=1.4, zorder=3))
    ax.text(px+18, 86.4, name, ha="center", fontsize=11, weight="bold", color=ec, zorder=4)
    ax.text(px+18, 82.3, sub, ha="center", fontsize=8.6, color=INK, zorder=4)
    px += 38.5
# note: agents reuses runner machinery
arrow(ax, (122.5, 83.5), (118.5, 83.5), color=BLUE, lw=1.4, style="-|>", ms=11)
ax.text(110, 76.7, "agents/ = runner/ generalized:  same cron-matrix + claim/done/bail, now for typed research items",
        fontsize=8, color=BLUE, style="italic", ha="right")

# down arrow: vendored into project
arrow(ax, (81, 76), (81, 71.5), color=INK, lw=2.6, style="-|>", ms=16)
ax.text(81, 73.6, "vendored as  standards/  submodule    →    project copies templates + sets  todo/agents.config.json",
        fontsize=8.8, color=INK, ha="center")

# =====================================================================
# BAND B — THE PROJECT (MIWN)
# =====================================================================
band(ax, 4, 27, 154, 43, "MIWN  —  the consolidated project repo   (REZN · MIZN · fixed-point-factory all fold in here)")

# YOU + dashboard (left control plane)
box(ax, 8, 60, 26, 6.0, "YOU\na few prompts / day", fc=(1,0.97,0.86), ec=RED, fs=10, weight="bold", tc=RED)
dash = box(ax, 6.5, 46.5, 29, 9.5,
           "DASHBOARD  =  this chat\nreads the ledger + open PRs\n→ daily digest; asks you only\nwhen an item needs a decision",
           fc=(1,1,1), ec=INK, fs=8.8, weight="bold")
arrow(ax, (21, 60), (21, 56), color=RED, lw=2.0, style="<|-|>", ms=13)

# central ledger hub
lx0, ly0, lw0, lh0 = 52, 44, 36, 17
ax.add_patch(FancyBboxPatch((lx0, ly0), lw0, lh0, boxstyle="round,pad=0.02,rounding_size=0.7",
                            fc=LBLUE, ec=BLUE, lw=1.8, zorder=3))
ax.text(lx0+lw0/2, ly0+lh0-2.4, "research-ledger.json", ha="center", fontsize=12, weight="bold", color=BLUE, zorder=4)
ax.text(lx0+lw0/2, ly0+lh0-5.2, "one source of truth", ha="center", fontsize=8.6, color=GREY, style="italic", zorder=4)
ax.text(lx0+lw0/2, ly0+5.6, "items:  proof · compute · figure\nliterature · writing · decision",
        ha="center", fontsize=9, color=INK, zorder=4)
ax.text(lx0+lw0/2, ly0+1.8, "each: status · gate · depends_on · owner", ha="center", fontsize=7.8, color=GREY, zorder=4)
arrow(ax, (35.5, 51.2), (lx0, 52.5), color=INK, lw=1.8, style="-|>", ms=13)
ax.text(43.5, 53.4, "read /\nroute", fontsize=7.6, color=GREY, ha="center")

# config chip under ledger
box(ax, 50, 39.5, 40, 3.8, "agents.config.json  —  per-type cadence · model · autonomy", fc=PAPER, ec=GREY, fs=8, tc=GREY, rad=0.4)

# agents column (right)
agents = [
    ("Compute agent", "gate: precision + branch guard", LGREEN, GREEN),
    ("Figure agent",  "gate: writing/figures ✓",        LGREEN, GREEN),
    ("Literature agent","gate: writing/references",     LGREY,  GREY),
    ("Proof agent",   "gate: writing/proofs (new)",     LRED,   RED),
    ("Writing / QA agent","gate: make stale + checklists", LRED, RED),
]
ax_x, ax_w, ax_h = 110, 44, 5.6
ytop = 62.0; step = 7.0
ledger_anchor = (lx0+lw0, 52.5)
for i, (name, gate, fc, ec) in enumerate(agents):
    yy = ytop - i*step
    ax.add_patch(FancyBboxPatch((ax_x, yy), ax_w, ax_h, boxstyle="round,pad=0.02,rounding_size=0.5", fc=fc, ec=ec, lw=1.4, zorder=3))
    ax.text(ax_x+2, yy+ax_h-1.9, name, ha="left", fontsize=9.6, weight="bold", color=ec, zorder=4)
    ax.text(ax_x+2, yy+1.6, gate, ha="left", fontsize=7.8, color=INK, zorder=4)
    arrow(ax, (ax_x, yy+ax_h/2), ledger_anchor, color=ec, lw=1.5, style="<|-|>", ms=11, rad=0.04)

# PR / merge note between ledger and agents
ax.text(99, 64.5, "agents open PRs\n→ tiered merge", fontsize=8.2, color=INK, ha="center", weight="bold")

# =====================================================================
# BAND C — LIVENESS
# =====================================================================
band(ax, 4, 4, 154, 20.5, "LIVENESS  —  sessions are disposable, the ledger is permanent   (an agent that wakes up just reads the ledger and resumes)")

# heartbeat timeline
ax.text(8, 20.0, "1.  Cron heartbeat", fontsize=10.5, weight="bold", color=GREEN)
ax.text(8, 17.4, "GitHub Actions wakes each agent on a schedule — compute */5 min, literature weekly.",
        fontsize=8.4, color=INK)
ty = 13.0
for i in range(8):
    xx = 10 + i*9.5
    ax.add_patch(Circle((xx, ty), 0.85, fc=GREEN, ec=GREEN, zorder=4))
    ax.text(xx, ty-2.2, f"t{i}", fontsize=7, color=GREY, ha="center", zorder=4)
    if i < 7:
        arrow(ax, (xx+0.95, ty), (xx+8.55, ty), color=GREEN, lw=1.3, ms=10)
ax.text(10, ty+2.0, "wake → read ledger → claim (git-race) → work → commit/PR → die", fontsize=7.8, color=GREEN, style="italic")

# event + self check-in + resume (right)
box(ax, 92, 15.0, 30, 5.4, "2.  Event wake-ups\nPR · CI · push  → instant", fc=(1,1,1), ec=BLUE, fs=8.4, weight="bold", tc=BLUE)
box(ax, 124, 15.0, 30, 5.4, "3.  Self-check-in\nre-arm a timer before dying", fc=(1,1,1), ec=RED, fs=8.4, weight="bold", tc=RED)
box(ax, 92, 6.2, 62, 6.0,
    "Why nothing is lost:  ALL STATE LIVES IN THE LEDGER, NOT THE SESSION.\nstale claims (died mid-task) auto-release after 15 min  →  re-picked",
    fc=LBLUE, ec=BLUE, fs=8.6, weight="bold", tc=BLUE)

pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)
pdf.close()
print("wrote agentic_research_os_summary.pdf")
