"""Generate ablation figures for the ReGuide website from the paper's appendix tables."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "static/images"
plt.rcParams.update({
    "font.size": 13,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": ":",
    "figure.dpi": 200,
})

C_BASE = "#7f8c8d"   # gray  - base / unguided
C_OURS = "#e8822a"   # orange - guided / ours
C_BLUE = "#2a6f9e"   # blue


def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png", bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


# ---- Fig A: number of phase targets M (Transport) ----
M = ["1", "10", "50", "100", "150"]
y = [0.4663, 0.4653, 0.5358, 0.5126, 0.4758]
e = [0.0148, 0.0164, 0.0169, 0.0131, 0.0156]
fig, ax = plt.subplots(figsize=(5.2, 3.6))
colors = [C_OURS if v == max(y) else C_BLUE for v in y]
ax.bar(M, y, yerr=e, capsize=4, color=colors, edgecolor="black", linewidth=0.6)
ax.axhline(0.4664, ls="--", color=C_BASE, lw=1.5, label="Base policy (0.47)")
ax.set_xlabel("# Phase targets per phase ($M$)")
ax.set_ylabel("Success rate")
ax.set_ylim(0.40, 0.58)
ax.legend(frameon=False, loc="upper right")
ax.set_title("Phase targets — Transport", fontsize=13)
save(fig, "ablation_phase_targets")


# ---- Fig B: gating strategy (Transport) ----
cats = ["No\nguidance", "Lower\nonly", "Upper\nonly", "Both\n(ours)"]
y = [0.4664, 0.4800, 0.4947, 0.5105]
e = [0.0140, 0.0170, 0.0138, 0.0131]
fig, ax = plt.subplots(figsize=(5.2, 3.6))
colors = [C_BASE, C_BLUE, C_BLUE, C_OURS]
ax.bar(cats, y, yerr=e, capsize=4, color=colors, edgecolor="black", linewidth=0.6)
ax.set_ylabel("Success rate")
ax.set_ylim(0.44, 0.53)
ax.set_title("Two-threshold gate — Transport", fontsize=13)
save(fig, "ablation_gating")


# ---- Fig C: clean action vs noisy iterate (Transport) ----
cats = ["Noisy iterate\n$A_t^k$ (prior)", "Clean action\n$\\hat{A}_t^0$ (ours)"]
y = [0.4890, 0.5135]
e = [0.0118, 0.0115]
fig, ax = plt.subplots(figsize=(4.4, 3.6))
ax.bar(cats, y, yerr=e, capsize=4, color=[C_BLUE, C_OURS], edgecolor="black", linewidth=0.6)
ax.set_ylabel("Success rate")
ax.set_ylim(0.46, 0.53)
ax.set_title("Guidance target — Transport", fontsize=13)
save(fig, "ablation_clean_vs_noisy")


# ---- Fig D: guided vs base at matched data (2x2) ----
panels = [
    ("Can (ReGuide-FS)", [0, 8, 15, 23],
     [0.4924, 0.5086, 0.5756, 0.5528], [0.0101, 0.0107, 0.0094, 0.0093],
     [np.nan, 0.5324, 0.6764, 0.6264], [np.nan, 0.0100, 0.0089, 0.0094]),
    ("Square (ReGuide-FS)", [0, 15, 30, 45],
     [0.5632, 0.5628, 0.6488, 0.6476], [0.0091, 0.0101, 0.0083, 0.0094],
     [np.nan, 0.6908, 0.7144, 0.6888], [np.nan, 0.0096, 0.0101, 0.0075]),
    ("Transport (ReGuide-FS)", [0, 5, 10, 15],
     [0.4664, 0.5436, 0.5924, 0.6080], [0.0086, 0.0114, 0.0092, 0.0096],
     [np.nan, 0.6324, 0.6820, 0.6544], [np.nan, 0.0104, 0.0114, 0.0096]),
    ("Can (ReGuide-FT)", [0, 8, 15, 23],
     [0.4924, 0.5256, 0.5664, 0.5376], [0.0101, 0.0111, 0.0093, 0.0101],
     [np.nan, 0.5436, 0.5932, 0.5852], [np.nan, 0.0096, 0.0098, 0.0095]),
]
fig, axes = plt.subplots(2, 2, figsize=(9.5, 7))
for ax, (title, x, by, be, gy, ge) in zip(axes.ravel(), panels):
    x = np.array(x, float)
    ax.errorbar(x, by, yerr=be, marker="o", color=C_BASE, capsize=3,
                lw=2, label="Unguided rollouts")
    ax.errorbar(x, gy, yerr=ge, marker="s", color=C_OURS, capsize=3,
                lw=2, label="Guided rollouts (ours)")
    ax.set_title(title, fontsize=12.5)
    ax.set_xlabel("# Added rollouts")
    ax.set_ylabel("Success rate")
    ax.set_xticks(x)
fig.legend(*axes[0, 0].get_legend_handles_labels(), loc="upper center",
           ncol=2, frameon=False, bbox_to_anchor=(0.5, 1.04))
save(fig, "ablation_guided_vs_base")


# ---- Fig E: buffer-share ratio rho (Can) ----
x = [0.6, 0.7, 0.8, 0.9, 1.0]
y = [0.5800, 0.6008, 0.5932, 0.5680, 0.5608]
e = [0.0177, 0.0159, 0.0159, 0.0146, 0.0178]
fig, ax = plt.subplots(figsize=(5.2, 3.6))
ax.errorbar(x, y, yerr=e, marker="o", color=C_OURS, capsize=4, lw=2)
ax.scatter([0.7], [0.6008], s=140, facecolors="none", edgecolors=C_BLUE, lw=2, zorder=5)
ax.set_xlabel("Buffer-share ratio $\\rho$")
ax.set_ylabel("Success rate")
ax.set_title("Buffer-share ratio — Can (ReGuide-FT)", fontsize=13)
ax.set_xticks(x)
save(fig, "ablation_rho")


# ---- Fig F: ReGuide-FT vs ReGuide-FS at composition step (Can) ----
x = np.array([0, 8, 15], float)
ft = [0.6764, 0.7208, 0.6916]
fte = [0.0089, 0.0086, 0.0081]
fs = [np.nan, 0.6878, 0.7088]
fse = [np.nan, 0.0078, 0.0087]
fig, ax = plt.subplots(figsize=(5.2, 3.6))
ax.errorbar(x, ft, yerr=fte, marker="o", color=C_OURS, capsize=4, lw=2, label="ReGuide-FT")
ax.errorbar(x, fs, yerr=fse, marker="s", color=C_BLUE, capsize=4, lw=2, label="ReGuide-FS")
ax.set_xlabel("# Added rollouts (from shared FS checkpoint)")
ax.set_ylabel("Success rate")
ax.set_title("FT vs FS at the composition step — Can", fontsize=13)
ax.set_xticks(x)
ax.legend(frameon=False, loc="lower right")
save(fig, "ablation_ft_vs_fs")

print("done")
