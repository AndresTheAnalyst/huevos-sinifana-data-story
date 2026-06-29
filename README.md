<div align="center">

<img src="app/assets/logo-full.png" alt="Huevos del Vecino" height="180"/>

# Huevos Sinifana SAS — Data Story

**6 lotes de gallina ponedora · ~6 años · una granja en Caldas–Antioquia, Colombia**

*La gallina pone bien. El que no ves trabajar es tu margen.*
*The hen lays just fine. The one you never watch working is your margin.*

</div>

---

🇪🇸 **Español** · [🇬🇧 English below](#-english)

## De qué se trata

Caso real de análisis de datos sobre **6 lotes de gallina ponedora** (G1–G6) de **Huevos Sinifana SAS**, ~2016–2022. A partir de registros de producción reales, facturas de alimento, salarios y precios de mercado, reconstruí el **costo y el margen por huevo** de cada lote y lo convertí en un **dashboard interactivo** que cualquiera —sepa o no de avicultura— puede entender.

> 🔗 **Dashboard en vivo:** _(pega aquí tu link de Streamlit Cloud al desplegar)_
> ▶️ **Correr local:** `streamlit run app/app.py`

## Lo que cuentan los datos (hallazgos)

| # | Hallazgo | El dato |
|---|---|---|
| 1 | **El alimento manda** | El concentrado es **~76%** del costo de cada huevo. |
| 2 | **El insumo se encareció** | El concentrado subió de **~$1.200 a ~$2.150/kg** (2016→2023). |
| 3 | **El tamaño del lote pesa** | G6 (lote chico, ~1.500 aves) concentra la nómina → el huevo más caro (**$408/huevo**). |
| 4 | **El mercado decide el margen** | La gallina pone igual (90–94%), pero el margen lo mueve el precio del huevo (🔴 en unos meses, 🟢 en otros). |
| 5 | **No todos los lotes dejaron plata** | Margen por huevo: de **−$37 (G1, pérdida)** a **+$65 (G6)**. |

### Comparativo de lotes (costo vs. margen, COP por huevo)

| Lote | Línea | Época | Costo/huevo | Venta/huevo | Margen | |
|---|---|---|---:|---:|---:|:--:|
| G1 | Hy-Line Brown | 2016–18 | $224 | $187 | −$37 | 🔴 |
| G2 | Hy-Line Brown | 2018–19 | $233 | $242 | +$9 | 🟡 |
| G3 | Babcock Brown | 2019–20 | $232 | $278 | +$46 | 🟢 |
| G4 | Babcock Brown | 2019–20 | $234 | $278 | +$44 | 🟢 |
| G5 | Lohmann Brown | 2021–22 | $323 | $361 | +$38 | 🟢 |
| G6 | Isa Brown | 2022 | $408 | $473 | +$65 | 🟢 |

## El dashboard

Cuatro vistas interactivas, bilingües (ES/EN):
- **🐔 Producción** — curva de postura real vs. el estándar de cada genética, semana a semana.
- **💵 Costos** — desglose por huevo + evolución mensual (costo, precio del productor, mayorista y concentrado).
- **📈 Mercado** — inflación del concentrado, precio del huevo y "la tijera" costo vs. precio.
- **🚦 Comparativo** — veredicto por lote con semáforo de margen.

## Datos y método (honestidad ante todo)

- **Producción:** registros semanales reales por lote (postura, mortalidad, huevos, alimento).
- **Costo por huevo:** modelo de 7 rubros. La **nómina y servicios** (costo fijo de la granja) se reparten entre la producción real de cada día → los lotes que corrieron al tiempo (G3/G4) **comparten** ese costo.
- **Alimento:** **factura real de Contegral** donde existe (2020–2023); antes, **estimado** con un modelo de concentrado ≈ f(maíz, soya) calibrado contra facturas (**R²=0,74**). Cada punto está marcado real/estimado.
- **Mercado:** precio mayorista del huevo rojo en Medellín (**SIPSA-DANE**). El precio del productor = mayorista × factor de finca (~0,89).
- **Límites declarados:** G1 (pre-2018) no tiene precio de mercado SIPSA; parte del alimento es estimado; SIPSA es mayorista, no minorista de plaza.

## Estructura del repo

```
portafolio-huevos-sinifana/
├── app/app.py            # Dashboard Streamlit (bilingüe, marca Huevos del Vecino)
├── app/assets/           # Logo y fuentes de marca
├── data/                 # Tablas limpias (CSV) + diccionario de datos
├── scripts/construir_datos.py  # Reproduce las tablas desde la fuente
├── notebooks/analisis.ipynb    # Análisis paso a paso
└── requirements.txt
```

## Correr local

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

## Stack

Python · pandas · Plotly · Streamlit · openpyxl

---

## 🇬🇧 English

### What this is

A real data-analysis case on **6 layer-hen lots** (G1–G6) of **Huevos Sinifana SAS**, Colombia, ~2016–2022. From real production records, feed invoices, wages and market prices, I rebuilt each lot's **cost and margin per egg** and turned it into an **interactive dashboard** anyone can understand — poultry background or not.

> 🔗 **Live dashboard:** _(paste your Streamlit Cloud link after deploying)_
> ▶️ **Run locally:** `streamlit run app/app.py`

### What the data shows

1. **Feed rules** — it's **~76%** of each egg's cost.
2. **Input prices rose** — feed went from **~$1,200 to ~$2,150/kg** (2016→2023).
3. **Lot size matters** — G6 (small flock) concentrates payroll → priciest egg (**$408**).
4. **The market sets the margin** — hens lay the same (90–94%), but the egg price decides profit.
5. **Not every lot made money** — margin per egg ranged from **−$37 (G1, loss)** to **+$65 (G6)**.

### Data & method (full transparency)

- **Production:** real weekly per-lot records.
- **Cost/egg:** 7-item model; fixed cost (labor + services) shared across overlapping lots by daily egg production.
- **Feed:** real **Contegral invoices** where available (2020–2023); otherwise **estimated** via a maize+soy model (**R²=0.74**). Each point is flagged real/estimated.
- **Market:** SIPSA-DANE wholesale red-egg price (Medellín); producer price = wholesale × farm factor (~0.89).
- **Stated limits:** G1 predates SIPSA; some feed is estimated; SIPSA is wholesale, not retail.

### Run locally

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

---

<div align="center">

**Andrés Estrada** · Análisis de datos / Data Analytics
GitHub: [AndresTheAnalyst](https://github.com/AndresTheAnalyst) · estrada0788@gmail.com

*Datos reales de Huevos Sinifana SAS, usados con permiso del propietario.
Real data from Huevos Sinifana SAS, used with the owner's permission.*

</div>
