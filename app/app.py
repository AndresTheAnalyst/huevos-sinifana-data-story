# -*- coding: utf-8 -*-
"""
Huevos Sinifana — Interactive data story (bilingual ES/EN).
Streamlit dashboard.  Run:  streamlit run app/app.py

6 layer lots, ~6 years, one farm: what happened to the egg margin.
6 lotes, ~6 años, una sola granja: qué le pasó al margen del huevo.
"""
from pathlib import Path
import base64
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# ----- author / config (edítalo a tu gusto) -----
AUTHOR = "Andrés Estrada"
GITHUB = "AndresTheAnalyst"
CONTACT = "estrada0788@gmail.com"

DATA = Path(__file__).resolve().parent.parent / "data"
ASSETS = Path(__file__).resolve().parent / "assets"
FONTS = ASSETS / "fonts"
# Paleta real de la marca "Huevos del Vecino": marrón, yema, terracota, azul cielo
PALETTE = {"feed": "#E5B441", "labor": "#AE4920", "other": "#C9B79C",
           "real": "#AE4920", "standard": "#C9B79C"}
STATUS_COLOR = {"green": "#6E8B3F", "yellow": "#E5B441", "red": "#AE4920"}
STATUS_EMOJI = {"green": "🟢", "yellow": "🟡", "red": "🔴"}

st.set_page_config(page_title="Huevos Sinifana — Data Story", page_icon="🥚", layout="wide")

# ---------------- identidad de marca: "Huevos del Vecino" (fuentes y colores reales) ----------------
@st.cache_data
def _font_faces():
    faces = [("Foco", "Foco-Regular.otf", "opentype", 400),
             ("Foco", "Foco-Bold.otf", "opentype", 700),
             ("Gotham Book", "Gotham-Book.otf", "opentype", 400),
             ("Cream Cake", "CreamCake.ttf", "truetype", 400)]
    out = []
    for fam, fn, fmt, wt in faces:
        b = base64.b64encode((FONTS / fn).read_bytes()).decode()
        mime = "otf" if fmt == "opentype" else "ttf"
        out.append(f"@font-face{{font-family:'{fam}';src:url(data:font/{mime};base64,{b}) "
                   f"format('{fmt}');font-weight:{wt};font-display:swap;}}")
    return "\n".join(out)


@st.cache_data
def _img_b64(name):
    return base64.b64encode((ASSETS / name).read_bytes()).decode()


st.markdown(f"""
<style>
{_font_faces()}
:root{{--brown:#41322F;--yolk:#E5B441;--red:#AE4920;--blue:#9ECBE5;--paper:#FBF8F2;}}
html, body, [class*="css"], .stApp, p, span, label, div{{font-family:'Gotham Book','Inter',system-ui,sans-serif;}}
.stApp{{background:var(--paper);}}
h1,h2,h3,h4,h5,h6{{font-family:'Foco','Gotham Book',sans-serif !important;color:var(--brown) !important;
    font-weight:700;letter-spacing:-0.005em;}}
[data-testid="stMetric"]{{background:#FFFFFF;border:1px solid #EADFCB;border-top:3px solid var(--yolk);
    border-radius:9px;padding:.55rem .95rem;}}
[data-testid="stMetricValue"]{{font-family:'Foco',sans-serif !important;color:var(--brown) !important;font-weight:700;}}
[data-testid="stMetricLabel"] p{{text-transform:uppercase;letter-spacing:.07em;font-size:.72rem !important;
    color:var(--red) !important;font-weight:700;}}
hr{{border-color:#EADFCB !important;}}
[data-testid="stCaptionContainer"] p{{color:#7A6A5A !important;}}
div[role="radiogroup"]{{gap:.4rem;}}
div[role="radiogroup"] label{{background:#FFFFFF;border:1.5px solid #EADFCB;border-radius:999px;padding:.2rem .95rem;}}
.hero{{background:#FFFFFF;border:1px solid #EADFCB;border-left:7px solid var(--yolk);border-radius:16px;
    padding:1.4rem 2rem;display:flex;align-items:center;gap:1.9rem;flex-wrap:wrap;
    box-shadow:0 1px 3px rgba(65,50,47,.06);}}
.hero img{{height:134px;}}
.hero-eyebrow{{font-family:'Gotham Book',sans-serif;font-size:.74rem;letter-spacing:.16em;
    text-transform:uppercase;color:var(--red);font-weight:700;}}
.hero-title{{font-family:'Foco',sans-serif;font-size:2.4rem;font-weight:700;color:var(--brown);line-height:1.05;margin:.12rem 0;}}
.hero-tag{{font-family:'Cream Cake',cursive;font-size:2.05rem;color:var(--red);line-height:1;}}
.hero-sub{{color:var(--brown);font-family:'Gotham Book',sans-serif;font-size:.93rem;max-width:62rem;
    line-height:1.55;margin:.9rem 0 .2rem;}}
.hero-sub i{{color:var(--red);font-style:italic;}}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load():
    return (pd.read_csv(DATA / "production_weekly.csv"),
            pd.read_csv(DATA / "lot_comparison.csv"),
            pd.read_csv(DATA / "egg_market_price.csv"),
            pd.read_csv(DATA / "feed_price.csv"),
            pd.read_csv(DATA / "lot_monthly.csv"))


prod, comp, mkt, feed, lmon = load()


def cop(x):
    return f"${x:,.0f}"


def signed(x):
    return f"+${x:,.0f}" if x >= 0 else f"-${abs(x):,.0f}"


# ---------------- language ----------------
lang = st.sidebar.radio("🌐 Idioma / Language", ["Español", "English"], index=0)
ES = lang == "Español"


def t(es, en):
    return es if ES else en


MES = (["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"] if ES
       else ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])


def periodo(iso_start, iso_end):
    """'2021-02-11','2022-09-30' -> 'feb 2021 → sep 2022'"""
    def f(iso):
        return f"{MES[int(iso[5:7]) - 1]} {iso[:4]}"
    return f"{f(iso_start)} → {f(iso_end)}"


def years_span(period):
    """'2016-11→2018-02' -> '2016–18'  ·  '2022-03→2022-10' -> '2022'"""
    a, b = period.split("→")
    y0, y1 = a[:4], b[:4]
    return y0 if y0 == y1 else f"{y0}–{y1[2:]}"


st.sidebar.markdown("---")
st.sidebar.markdown(t(
    "**Cómo leerlo:** cada número es por **un huevo**, en pesos colombianos (COP). "
    "Si el precio de venta le gana al costo, hay margen.",
    "**How to read it:** every figure is **per egg**, in Colombian pesos (COP). "
    "If the sale price beats the cost, there's a margin."))

# ---------------- hero (marca Huevos del Vecino + Huevos Sinifana SAS) ----------------
st.markdown(f"""
<div class="hero">
  <img src="data:image/png;base64,{_img_b64('logo-full.png')}" alt="Huevos del Vecino"/>
  <div>
    <div class="hero-eyebrow">{t("Caso real · datos de producción 2016–2022", "Real case · production data 2016–2022")}</div>
    <div class="hero-title">Huevos Sinifana SAS</div>
    <div class="hero-tag">Sabor de campo cerca</div>
  </div>
</div>
<div class="hero-sub">{t("6 lotes de gallina ponedora · ~6 años · una granja en Caldas–Antioquia, Colombia. Mismo dueño, mismo manejo — pero el negocio cambió. <i>La gallina pone bien; el que no ves trabajar es tu margen.</i> Datos reales, usados con permiso del propietario.", "6 layer lots · ~6 years · one farm in Caldas–Antioquia, Colombia. Same owner, same management — yet the business changed. <i>The hen lays fine; the one you never watch working is your margin.</i> Real data, used with the owner's permission.")}</div>
""", unsafe_allow_html=True)
st.write("")

# ---------------- KPIs ----------------
total_eggs = int(prod["eggs"].sum())
yr_min = prod["date_start"].dropna().min()[:4]
yr_max = prod["date_end"].dropna().max()[:4]
feed_first, feed_last = feed.iloc[0]["price_per_kg"], feed.iloc[-1]["price_per_kg"]
feed_infl = (feed_last / feed_first - 1) * 100
best = comp.loc[comp["margin"].idxmax()]
worst = comp.loc[comp["margin"].idxmin()]

k1, k2, k3, k4 = st.columns(4)
k1.metric(t("Lotes analizados", "Lots analyzed"), comp["lot"].nunique())
k2.metric(t("Huevos producidos", "Eggs produced"), f"{total_eggs/1e6:.1f} M")
k3.metric(t("Concentrado por kg", "Feed price per kg"), f"+{feed_infl:.0f}%",
          help=t(f"Subió de {cop(feed_first)} a {cop(feed_last)} por kg entre {yr_min} y {yr_max}.",
                 f"Rose from {cop(feed_first)} to {cop(feed_last)} per kg between {yr_min} and {yr_max}."))
k4.metric(t("Margen por huevo", "Margin per egg"),
          f"{signed(worst['margin'])} … {signed(best['margin'])}",
          help=t(f"Del peor lote ({worst['lot']}) al mejor ({best['lot']}).",
                 f"From the worst lot ({worst['lot']}) to the best ({best['lot']})."))

st.divider()

S_PROD = "🐔 " + t("Producción", "Production")
S_COST = "💵 " + t("Costos", "Costs")
S_MKT = "📈 " + t("Mercado", "Market")
S_CMP = "🚦 " + t("Comparativo", "Comparison")
# Navegación por radio (conserva la sección activa entre re-ejecuciones; st.tabs se reiniciaba a la 1ra)
seccion = st.radio(t("Sección", "Section"), [S_PROD, S_COST, S_MKT, S_CMP],
                   horizontal=True, label_visibility="collapsed")
st.write("")

# ============ TAB 1 — PRODUCTION ============
if seccion == S_PROD:
    st.subheader(t("¿Cómo puso cada lote? Real vs. el estándar de su genética",
                   "How did each lot lay? Actual vs. its breed standard"))
    lots = sorted(prod["lot"].unique())
    sel = st.selectbox(t("Elegí un lote", "Pick a lot"), lots,
                       index=lots.index("G5") if "G5" in lots else 0)
    d = prod[(prod["lot"] == sel) & (prod["eggs"] > 0)].copy().sort_values("week")
    line_name = d["line"].iloc[0] if len(d) else ""
    plena = d[(d["week"] >= 22) & (d["week"] <= 60)]

    m1, m2, m3 = st.columns(3)
    m1.metric(t("Pico de postura", "Peak lay rate"), f"{d['lay_rate_real'].max()*100:.0f}%")
    m2.metric(t("Semanas en postura", "Weeks in lay"), len(d))
    m3.metric(t("Postura media (plena)", "Avg lay (peak phase)"),
              f"{plena['lay_rate_real'].mean()*100:.0f}%" if len(plena) else "—")

    d["real_%"] = d["lay_rate_real"] * 100
    d["std_%"] = d["lay_rate_standard"] * 100

    # línea de tiempo de MESES reales (un tick cada 2 meses desde el inicio) -> fila ABAJO, junto a la semana de vida
    ym = [(int(x[:4]), int(x[5:7]), int(w)) for x, w in zip(d["date_start"], d["week"])]
    first_week = {}
    for yy, mm, w in ym:
        first_week.setdefault((yy, mm), w)
    month_ticks = []   # (semana, etiqueta de mes)
    yy, mm = ym[0][0], ym[0][1]
    yN, mN = ym[-1][0], ym[-1][1]
    while (yy, mm) <= (yN, mN):
        if (yy, mm) in first_week:
            month_ticks.append((first_week[(yy, mm)], f"{MES[mm - 1]} '{str(yy)[2:]}"))
        mm += 2
        if mm > 12:
            mm -= 12
            yy += 1

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d["week"], y=d["std_%"], name=t("Estándar genético", "Breed standard"),
                             line=dict(color=PALETTE["standard"], dash="dash")))
    fig.add_trace(go.Scatter(x=d["week"], y=d["real_%"], name=t("Postura real", "Actual lay"),
                             line=dict(color=PALETTE["real"], width=3)))
    # mes real como SEGUNDA FILA de etiquetas debajo del eje de semanas
    for wk, lbl in month_ticks:
        fig.add_annotation(x=wk, y=-0.27, xref="x", yref="paper", text=lbl, showarrow=False,
                           font=dict(size=10, color="#475569"))
    # rótulos de fila a la IZQUIERDA: identifican cada fila del eje
    fig.add_annotation(text=t("Semana de vida →", "Lot age (week) →"), xref="paper", yref="paper",
                       x=-0.012, y=-0.06, xanchor="right", showarrow=False,
                       font=dict(size=11, color="#334155"))
    fig.add_annotation(text=t("Mes real →", "Real month →"), xref="paper", yref="paper",
                       x=-0.012, y=-0.27, xanchor="right", showarrow=False,
                       font=dict(size=11, color="#334155"))
    fig.update_layout(height=470, hovermode="x unified",
                      legend=dict(orientation="h", y=1.12), margin=dict(t=30, b=96, l=128),
                      xaxis=dict(title=None,
                                 range=[int(d["week"].min()) - 3, int(d["week"].max()) + 2]),
                      yaxis=dict(title=t("% de postura", "Lay rate %")))
    st.plotly_chart(fig, use_container_width=True)
    per_real = periodo(d["date_start"].min(), d["date_end"].max())
    st.markdown(t(f"📅 **Periodo real de producción:** {per_real}",
                  f"📅 **Actual production period:** {per_real}"))
    st.caption(t(
        f"**{sel} · {line_name}.** Cada fila del eje tiene su rótulo a la izquierda: **Semana de vida** (edad del lote) "
        "y, debajo, **Mes real** (cada 2 meses). La línea punteada es lo que promete la genética; la sólida, lo que de "
        "verdad puso. Cuando la real va pegada o por encima del estándar, el manejo está fino.",
        f"**{sel} · {line_name}.** Each axis row is labeled on the left: **Lot age (week)** and, below it, **Real month** "
        "(every 2 months). The dashed line is what the genetics promise; the solid one is what really happened. "
        "When the actual sits on or above the standard, husbandry is on point."))

# ============ TAB 2 — COSTS ============
elif seccion == S_COST:
    st.subheader(t("¿En qué se va el costo de cada huevo?", "Where does each egg's cost go?"))
    names = {"cost_feed": t("Alimento", "Feed"), "cost_labor": t("Mano de obra", "Labor"),
             "cost_other": t("Otros", "Other")}
    order = list(comp["lot"])
    # precio mayorista DANE-SIPSA (Medellín) promedio del periodo de cada lote
    mkt_idx = dict(zip(mkt["month"], mkt["price_avg"]))

    def months_between(p):
        a, b = p.split("→")
        y, m, ey, em = int(a[:4]), int(a[5:7]), int(b[:4]), int(b[5:7])
        out = []
        while (y, m) <= (ey, em):
            out.append(f"{y}-{m:02d}")
            m += 1
            if m > 12:
                m = 1
                y += 1
        return out

    dane = {}
    for lot_, p in zip(comp["lot"], comp["period"]):
        ml = months_between(p)
        vals = [mkt_idx[mm] for mm in ml if mm in mkt_idx]
        dane[lot_] = round(sum(vals) / len(vals)) if len(vals) >= max(2, len(ml) // 2) else None

    long = comp.melt(id_vars=["lot"], value_vars=["cost_feed", "cost_labor", "cost_other"],
                     var_name="rubro", value_name="cop_val")
    long["rubro"] = long["rubro"].map(names)
    fig = px.bar(long, x="lot", y="cop_val", color="rubro", category_orders={"lot": order},
                 color_discrete_map={names["cost_feed"]: PALETTE["feed"],
                                     names["cost_labor"]: PALETTE["labor"],
                                     names["cost_other"]: PALETTE["other"]},
                 labels={"lot": t("Lote", "Lot"), "cop_val": t("COP por huevo", "COP per egg"),
                         "rubro": t("Rubro", "Cost item")})
    # línea de precio de venta del productor por lote (para ver la tijera costo vs. precio)
    fig.add_trace(go.Scatter(x=comp["lot"], y=comp["sale_price"], mode="lines+markers",
                             name=t("Precio de venta (productor)", "Sale price (producer)"),
                             line=dict(color="#AE4920", width=2.5), marker=dict(size=8, color="#AE4920")))
    fig.add_trace(go.Scatter(x=order, y=[dane[l] for l in order], mode="lines+markers",
                             name=t("Precio mayorista DANE-SIPSA", "DANE-SIPSA wholesale price"),
                             line=dict(color="#5B9BBE", width=2, dash="dot"),
                             marker=dict(size=7, color="#5B9BBE"), connectgaps=False))
    for _, row in comp.iterrows():       # total encima de cada barra
        fig.add_annotation(x=row["lot"], y=row["cost_total"], text=f"<b>{cop(row['cost_total'])}</b>",
                           showarrow=False, yshift=11, font=dict(size=11, color="#0F172A"))
    per = comp.set_index("lot")["period"]
    ticktext = [f"{l}<br><span style='font-size:11px;color:#64748B'>{years_span(per[l])}</span>" for l in order]
    fig.update_xaxes(tickmode="array", tickvals=order, ticktext=ticktext)
    dane_vals = [v for v in dane.values() if v]
    ymax = max(comp["cost_total"].max(), comp["sale_price"].max(), max(dane_vals) if dane_vals else 0)
    fig.update_layout(height=480, legend=dict(orientation="h", y=1.14), margin=dict(t=48),
                      yaxis=dict(range=[0, ymax * 1.18], title=t("COP por huevo", "COP per egg")))
    st.plotly_chart(fig, use_container_width=True)
    st.caption(t(
        "Las barras son el **costo** por huevo (apilado por rubro) y, bajo cada lote, **el año en que produjo**. "
        "🔴 **Línea roja** = **precio de venta del productor** (lo que de verdad recibe la finca). "
        "🔵 **Línea azul punteada** = **precio mayorista que reporta el DANE-SIPSA** (Medellín) en ese mismo periodo. "
        "El espacio entre la azul y la roja es el *descuento de plaza*; el espacio entre la roja y la barra es el *margen*. "
        "⚠️ G1 no tiene línea DANE: su época (2016-17) es anterior a la serie SIPSA (arranca en 2018).",
        "Bars are the **cost** per egg (stacked by item) and, under each lot, **the year it produced**. "
        "🔴 **Red line** = **producer's sale price** (what the farm actually receives). "
        "🔵 **Dotted blue line** = **DANE-SIPSA wholesale price** (Medellín) for that same period. "
        "The gap between blue and red is the *market discount*; the gap between red and the bar is the *margin*. "
        "⚠️ G1 has no DANE line: its era (2016-17) predates the SIPSA series (starts in 2018)."))
    c1, c2 = st.columns(2)
    c1.info(t(
        "**El alimento manda:** es ~3 de cada 4 pesos del costo de un huevo. Por eso el precio del "
        "concentrado decide casi todo (ver pestaña Mercado).",
        "**Feed rules:** it's about 3 of every 4 pesos in an egg's cost. That's why the concentrate price "
        "decides almost everything (see the Market tab)."))
    c2.warning(t(
        "**El tamaño del lote pesa:** G6 fue un lote chico (~1.500 aves) → la nómina se reparte entre menos "
        "huevos → mano de obra más cara por huevo. La escala importa.",
        "**Lot size matters:** G6 was a small flock (~1,500 hens) → payroll spreads over fewer eggs → pricier "
        "labor per egg. Scale matters."))

    # ----- evolución MES A MES por lote (estilo Mercado) -----
    st.markdown("---")
    lots_c = list(comp["lot"])
    selc = st.selectbox(t("Elegí un lote para ver su evolución mensual",
                          "Pick a lot to see its monthly evolution"),
                        lots_c, index=lots_c.index("G5") if "G5" in lots_c else 0, key="lote_costos")
    dm = lmon[lmon["lot"] == selc].sort_values("month")
    line_c = comp.set_index("lot").loc[selc, "line"]
    # rangos Y ajustados a los datos reales de cada eje (para que ambos se lean bien)
    _left = pd.concat([dm["total_cost_egg"], dm["producer_price"], dm["wholesale_dane"]]).dropna()
    _conc = dm["feed_price_kg"].dropna()
    yrange = [_left.min() - 25, _left.max() + 25] if len(_left) else None
    y2range = [_conc.min() - 30, _conc.max() + 30] if len(_conc) else None
    figm = go.Figure()
    # eje izquierdo (COP/huevo): costo de producción + precio del productor + precio mayorista
    figm.add_trace(go.Scatter(x=dm["month"], y=dm["total_cost_egg"], mode="lines",
                              name=t("Costo de producción (COP/huevo)", "Production cost (COP/egg)"),
                              line=dict(color="#41322F", width=3)))
    figm.add_trace(go.Scatter(x=dm["month"], y=dm["producer_price"], mode="lines+markers",
                              name=t("Precio venta productor (COP/huevo)", "Producer sale price (COP/egg)"),
                              line=dict(color="#AE4920", width=2.5), marker=dict(size=5), connectgaps=False))
    figm.add_trace(go.Scatter(x=dm["month"], y=dm["wholesale_dane"], mode="lines+markers",
                              name=t("Precio mayorista DANE-SIPSA (COP/huevo)", "DANE-SIPSA wholesale (COP/egg)"),
                              line=dict(color="#5B9BBE", width=2, dash="dot"), marker=dict(size=5), connectgaps=False))
    # eje derecho (COP/kg): precio del concentrado — marcador marrón = factura real, claro = estimado
    fcol = ["#41322F" if s == "invoice" else "#EBD9A6" for s in dm["feed_source"].fillna("estimated")]
    figm.add_trace(go.Scatter(x=dm["month"], y=dm["feed_price_kg"], mode="lines+markers",
                              name=t("Precio concentrado (COP/kg) →", "Feed price (COP/kg) →"),
                              line=dict(color="#E5B441", width=2.5),
                              marker=dict(size=6, color=fcol),
                              yaxis="y2", connectgaps=False))
    figm.update_layout(height=460, margin=dict(t=46, b=40),
                       legend=dict(orientation="h", yanchor="top", y=-0.14, x=0),
                       title=dict(text=t(f"{selc} · {line_c} — costo, precios y concentrado, mes a mes",
                                         f"{selc} · {line_c} — cost, prices and feed, month by month"),
                                  y=0.97, yanchor="top"),
                       xaxis=dict(title=None),
                       yaxis=dict(title=t("COP / huevo", "COP / egg"), range=yrange),
                       yaxis2=dict(title=t("COP / kg (concentrado)", "COP / kg (feed)"),
                                   overlaying="y", side="right", showgrid=False, range=y2range))
    st.plotly_chart(figm, use_container_width=True)
    st.caption(t(
        f"**{selc} · {line_c}** — mes a mes durante su producción (eje izq. COP/huevo · eje der. COP/kg). "
        "⚫ **costo de producción** · 🔴 **precio de venta del productor** (lo que recibe la finca) · 🔵 **precio mayorista "
        "DANE-SIPSA** · 🟠 **precio del concentrado** (eje derecho). Donde la 🔴 va por encima de la ⚫, ese mes **dejó margen**. "
        "⚠️ 'DANE' y 'plaza mayorista' son la misma fuente (SIPSA); el productor recibe ese mayorista × factor (~0,89). "
        "En la 🟠 del concentrado, los puntos **marrones** son meses con **factura real** (Contegral, 2020–2023) y los **claros** "
        "son **estimados** (modelo maíz+soya). G1 no muestra precio de mercado (su época es anterior a SIPSA 2018).",
        f"**{selc} · {line_c}** — month by month during production (left axis COP/egg · right axis COP/kg). "
        "⚫ **production cost** · 🔴 **producer sale price** (what the farm gets) · 🔵 **DANE-SIPSA wholesale** · "
        "🟠 **feed price** (right axis). Where 🔴 sits above ⚫, that month **made margin**. "
        "⚠️ 'DANE' and 'wholesale plaza' are the same source (SIPSA); the producer gets that wholesale × factor (~0.89). "
        "On the 🟠 feed line, **brown** dots are months with **real invoices** (Contegral, 2020–2023) and **light** dots are "
        "**estimated** (maize+soy model). G1 shows no market price (its era predates SIPSA 2018)."))

# ============ TAB 3 — MARKET ============
elif seccion == S_MKT:
    st.subheader(t("El insumo subió y el mercado manda", "Input prices rose, and the market rules"))
    ca, cb = st.columns(2)
    with ca:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=feed["month"], y=feed["price_per_kg"], mode="lines",
                                 name=t("Serie de precio", "Price series"),
                                 line=dict(color=PALETTE["feed"], width=2.5)))
        inv = feed[feed["source"] == "invoice"]
        fig.add_trace(go.Scatter(x=inv["month"], y=inv["price_per_kg"], mode="markers",
                                 name=t("Mes con factura real", "Real-invoice month"),
                                 marker=dict(color="#0F766E", size=7)))
        fig.update_layout(height=390, margin=dict(t=44, b=8),
                          legend=dict(orientation="h", yanchor="top", y=-0.18, x=0),
                          title=dict(text=t("Precio del concentrado ponedora (COP/kg)", "Layer-feed price (COP/kg)"),
                                     y=0.97, yanchor="top"))
        st.plotly_chart(fig, use_container_width=True)
        n_inv = int((feed["source"] == "invoice").sum())
        st.caption(t(
            f"+{feed_infl:.0f}% en {yr_min}–{yr_max}. Solo {n_inv} de {len(feed)} meses vienen de **factura real** "
            "(puntos verdes, 2020–2022); el resto es un **modelo de concentrado calibrado** (R²=0,74). Honestidad ante todo.",
            f"+{feed_infl:.0f}% over {yr_min}–{yr_max}. Only {n_inv} of {len(feed)} months come from **real invoices** "
            "(green dots, 2020–2022); the rest is a **calibrated feed model** (R²=0.74). Full transparency."))
    with cb:
        mg = mkt.dropna(subset=["price_avg"]).copy()
        fig = px.line(mg, x="month", y="price_avg",
                      labels={"month": t("Mes", "Month"), "price_avg": t("COP / huevo", "COP / egg")})
        fig.update_traces(line=dict(color=PALETTE["real"], width=2))
        fig.update_layout(height=340, margin=dict(t=34),
                          title=t("Precio mayorista del huevo rojo · Medellín (COP/huevo)",
                                  "Wholesale red-egg price · Medellín (COP/egg)"))
        st.plotly_chart(fig, use_container_width=True)
        st.caption(t("El precio sube y baja con el mercado: la gallina pone igual, pero el margen cambia. Fuente: SIPSA-DANE.",
                     "The price swings with the market: the hen lays the same, but the margin moves. Source: SIPSA-DANE."))
    st.markdown("##### " + t("La tijera: costo vs. precio de venta, por lote",
                             "The scissors: cost vs. sale price, per lot"))
    fig = go.Figure()
    fig.add_trace(go.Bar(x=comp["lot"], y=comp["cost_total"], name=t("Costo total/huevo", "Total cost/egg"),
                         marker_color=PALETTE["other"]))
    fig.add_trace(go.Bar(x=comp["lot"], y=comp["sale_price"], name=t("Precio de venta/huevo", "Sale price/egg"),
                         marker_color=PALETTE["real"]))
    fig.update_layout(height=360, barmode="group", legend=dict(orientation="h", y=1.14),
                      yaxis_title=t("COP por huevo", "COP per egg"), margin=dict(t=30))
    st.plotly_chart(fig, use_container_width=True)

# ============ TAB 4 — COMPARISON ============
elif seccion == S_CMP:
    st.subheader(t("El veredicto: ¿qué lote dejó plata?", "The verdict: which lot made money?"))
    cc = comp.copy()
    cc["color"] = cc["status"].map(STATUS_COLOR)
    fig = go.Figure(go.Bar(x=cc["lot"], y=cc["margin"], marker_color=cc["color"],
                           text=cc["margin"].map(signed), textposition="outside"))
    fig.update_layout(height=400, yaxis_title=t("Margen neto / huevo (COP)", "Net margin / egg (COP)"),
                      margin=dict(t=20), yaxis=dict(range=[cc["margin"].min() - 20, cc["margin"].max() + 25]))
    fig.add_hline(y=0, line_color="#64748B")
    st.plotly_chart(fig, use_container_width=True)

    show = cc.copy()
    show[" "] = show["status"].map(STATUS_EMOJI)
    show["lay_rate"] = (show["lay_rate"] * 100).round(0).astype(int).astype(str) + "%"
    for col in ["cost_total", "sale_price"]:
        show[col] = show[col].map(cop)
    show["margin"] = show["margin"].map(signed)
    show = show[[" ", "lot", "line", "period", "lay_rate", "cost_total", "sale_price", "margin"]]
    show.columns = [" ", t("Lote", "Lot"), t("Línea", "Line"), t("Época", "Era"), t("Postura", "Lay rate"),
                    t("Costo/huevo", "Cost/egg"), t("Venta/huevo", "Sale/egg"), t("Margen", "Margin")]
    st.dataframe(show, use_container_width=True, hide_index=True)
    st.caption(t(
        "🟢 verde = margen > $30 · 🟡 amarillo = $0 a $30 · 🔴 rojo = pérdida. "
        "El costo fijo (nómina + servicios) se reparte entre los lotes que corrieron al tiempo (G3 y G4 se traslaparon en 2019–2020).",
        "🟢 green = margin > $30 · 🟡 yellow = $0–30 · 🔴 red = loss. "
        "Fixed cost (labor + services) is shared across overlapping lots (G3 and G4 ran simultaneously in 2019–2020)."))

# ---------------- footer ----------------
st.divider()
st.caption(t(
    f"**{AUTHOR}** · Análisis de datos · GitHub: {GITHUB} · {CONTACT}  \n"
    "Datos reales de Huevos Sinifana SAS (Las Marías, Caldas–Antioquia), usados con permiso del propietario. "
    "Concentrado: factura real Contegral donde existe (2020–2023); antes, estimado con modelo maíz+soya (R²=0,74). Valores en COP.",
    f"**{AUTHOR}** · Data analytics · GitHub: {GITHUB} · {CONTACT}  \n"
    "Real data from Huevos Sinifana SAS (Las Marías, Caldas–Antioquia), used with the owner's permission. "
    "Feed: real Contegral invoices where available (2020–2023); earlier, estimated via a maize+soy model (R²=0.74). All values in COP."))
