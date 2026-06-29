# -*- coding: utf-8 -*-
"""Genera las figuras estáticas (PNG) del notebook con la paleta de marca Huevos del Vecino.
Reproduce los mismos gráficos del dashboard pero en matplotlib, para que rendericen en GitHub."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

AQUI = Path(__file__).resolve().parent
DATA = AQUI.parent / "data"
FIG = AQUI / "figures"
FIG.mkdir(exist_ok=True)

BROWN, YOLK, RED, BLUE, KRAFT, OLIVE = "#41322F", "#E5B441", "#AE4920", "#9ECBE5", "#C9B79C", "#6E8B3F"
plt.rcParams.update({"font.size": 11, "axes.edgecolor": "#D8CCB6", "axes.linewidth": .8,
                     "axes.grid": True, "grid.color": "#EEE6D6", "figure.facecolor": "white",
                     "axes.facecolor": "white", "savefig.facecolor": "white", "axes.titlecolor": BROWN})

prod = pd.read_csv(DATA / "production_weekly.csv")
comp = pd.read_csv(DATA / "lot_comparison.csv")
mkt = pd.read_csv(DATA / "egg_market_price.csv")
feed = pd.read_csv(DATA / "feed_price.csv")

# 1) Curva de postura G5 (real vs estándar)
d = prod[(prod.lot == "G5") & (prod.eggs > 0)].sort_values("week")
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.plot(d.week, d.lay_rate_standard * 100, "--", color=KRAFT, label="Estándar genético / Breed standard")
ax.plot(d.week, d.lay_rate_real * 100, color=RED, lw=2.4, label="Postura real / Actual lay")
ax.set_title("G5 · Lohmann Brown — postura real vs. estándar")
ax.set_xlabel("Semana de vida / Lot age (week)"); ax.set_ylabel("% postura / lay rate")
ax.legend(frameon=False); fig.tight_layout(); fig.savefig(FIG / "01_lay_curve_g5.png", dpi=130); plt.close(fig)

# 2) Costo por huevo apilado por lote
fig, ax = plt.subplots(figsize=(8, 3.8))
lots = comp.lot.tolist()
ax.bar(lots, comp.cost_feed, color=YOLK, label="Alimento / Feed")
ax.bar(lots, comp.cost_labor, bottom=comp.cost_feed, color=RED, label="Mano de obra / Labor")
ax.bar(lots, comp.cost_other, bottom=comp.cost_feed + comp.cost_labor, color=KRAFT, label="Otros / Other")
for i, (l, tot) in enumerate(zip(lots, comp.cost_total)):
    ax.text(i, tot + 6, f"${tot:,.0f}", ha="center", color=BROWN, fontweight="bold", fontsize=10)
ax.set_title("Costo por huevo, por lote (COP)")
ax.set_ylabel("COP / huevo"); ax.legend(frameon=False, ncol=3, loc="upper left")
ax.set_ylim(0, comp.cost_total.max() * 1.2); fig.tight_layout()
fig.savefig(FIG / "02_cost_breakdown.png", dpi=130); plt.close(fig)

# 3) Precio del concentrado (real vs estimado) en el tiempo
fig, ax = plt.subplots(figsize=(8, 3.4))
ax.plot(pd.to_datetime(feed.month + "-01"), feed.price_per_kg, color=YOLK, lw=2)
inv = feed[feed.source == "invoice"]; est = feed[feed.source == "estimated"]
ax.scatter(pd.to_datetime(inv.month + "-01"), inv.price_per_kg, color=BROWN, s=14, zorder=3,
           label="Factura real / Real invoice")
ax.scatter(pd.to_datetime(est.month + "-01"), est.price_per_kg, color="#EBD9A6", s=14, zorder=3,
           label="Estimado / Estimated")
ax.set_title("Precio del concentrado ponedora (COP/kg) — +%d%% en 2016–2023" %
             round((feed.price_per_kg.iloc[-1] / feed.price_per_kg.iloc[0] - 1) * 100))
ax.set_ylabel("COP / kg"); ax.legend(frameon=False); fig.tight_layout()
fig.savefig(FIG / "03_feed_price.png", dpi=130); plt.close(fig)

# 4) Margen por lote (semáforo)
fig, ax = plt.subplots(figsize=(8, 3.4))
cmap = {"green": OLIVE, "yellow": YOLK, "red": RED}
ax.bar(comp.lot, comp.margin, color=[cmap[s] for s in comp.status])
for i, m in enumerate(comp.margin):
    ax.text(i, m + (2 if m >= 0 else -6), f"{m:+,.0f}", ha="center", color=BROWN, fontweight="bold")
ax.axhline(0, color="#7A6A5A", lw=.9)
ax.set_title("Margen neto por huevo, por lote (COP)"); ax.set_ylabel("COP / huevo")
fig.tight_layout(); fig.savefig(FIG / "04_margin_by_lot.png", dpi=130); plt.close(fig)

print("Figuras generadas en", FIG)
for p in sorted(FIG.glob("*.png")):
    print("  ", p.name, p.stat().st_size // 1024, "KB")
