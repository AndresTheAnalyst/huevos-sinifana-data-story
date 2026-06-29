# Data Dictionary — Huevos Sinifana SAS

> Bilingual data dictionary (ES/EN). All monetary values in **COP** (Colombian pesos).
> Diccionario de datos bilingüe. Valores monetarios en **pesos colombianos (COP)**.

Source / Fuente: real records of **Huevos Sinifana SAS** (Las Marías farm, Caldas–Antioquia,
Colombia), 6 layer lots (G1–G6), 2016–2023. My own poultry operation / Operación avícola propia.

---

## `production_weekly.csv`
Weekly operating record, one row per lot × week. / Registro operativo semanal, una fila por lote × semana.

| Column | ES | EN |
|---|---|---|
| `lot` | Lote (G1–G6) | Lot id |
| `line` | Línea genética | Genetic line |
| `week` | Semana de vida del lote | Lot age week |
| `date_start` / `date_end` | Inicio / fin de la semana | Week start / end |
| `hens` | Aves vivas | Live hens |
| `mortality` | Mortalidad de la semana | Weekly mortality |
| `lay_rate_real` | % postura real | Actual lay rate |
| `lay_rate_standard` | % postura estándar (tabla genética) | Breed-standard lay rate |
| `eggs` | Huevos de la semana | Eggs that week |
| `feed_kg` | Alimento consumido (kg) | Feed consumed (kg) |

## `lot_comparison.csv`
Cost-per-egg and margin by lot/era. Fixed cost (labor+services) shared across overlapping lots. /
Costo por huevo y margen por lote/época. El costo fijo se reparte entre lotes traslapados.

| Column | ES | EN |
|---|---|---|
| `lot` / `line` / `period` | Lote / línea / época | Lot / line / era |
| `hens` | Aves (flock productivo) | Productive flock size |
| `lay_rate` | % postura promedio en plena postura | Avg peak-lay rate |
| `cost_feed` | Costo alimento / huevo | Feed cost / egg |
| `cost_labor` | Costo mano de obra / huevo (fijo repartido) | Labor cost / egg (shared fixed) |
| `cost_other` | Otros (servicios, sanidad, empaque, calcio) / huevo | Other costs / egg |
| `cost_total` | Costo total / huevo | Total cost / egg |
| `sale_price` | Precio de venta del productor / huevo | Producer sale price / egg |
| `margin` | Margen neto / huevo | Net margin / egg |
| `status` | Semáforo (green/yellow/red) | Traffic light |

**Honesty note / Nota de honestidad:** G5/G6 feed cost = real invoices; G1–G4 = estimated
(calibrated concentrate model, R²=0.74). G1 sale price estimated (pre-SIPSA).

## `egg_market_price.csv`
Monthly wholesale red-egg price, Medellín market (SIPSA-DANE). /
Precio mayorista mensual del huevo rojo, plaza Medellín (SIPSA-DANE).

| Column | ES | EN |
|---|---|---|
| `month` | Mes (YYYY-MM) | Month |
| `price_avg` | Precio ponderado (mezcla de categorías) | Weighted price |
| `price_extra` / `price_aa` / `price_a` / `price_b` | Precio por categoría | Price by grade |

## `feed_price.csv`
Monthly layer-concentrate price per kg. / Precio mensual del concentrado ponedora por kg.

| Column | ES | EN |
|---|---|---|
| `month` | Mes (YYYY-MM) | Month |
| `price_per_kg` | Precio por kg (COP) | Price per kg (COP) |
| `source` | `invoice` (factura real) / `estimated` (modelo) | Source |

## `lot_monthly.csv`
Month-by-month economics per lot (cost-per-egg model at monthly resolution). /
Economía mes a mes por lote (modelo de costo por huevo a resolución mensual).

| Column | ES | EN |
|---|---|---|
| `lot` / `month` | Lote / mes (YYYY-MM) | Lot / month |
| `eggs` | Huevos del mes | Eggs that month |
| `feed_price_kg` | Precio del concentrado ese mes (COP/kg) | Feed price that month (COP/kg) |
| `feed_source` | `invoice` (factura real) / `estimated` (modelo maíz+soya) | Source of the feed price |
| `feed_cost_egg` | Costo de alimento / huevo | Feed cost / egg |
| `total_cost_egg` | Costo total de producción / huevo | Total production cost / egg |
| `producer_price` | Precio de venta del productor / huevo (mayorista × factor de finca) | Producer sale price / egg |
| `wholesale_dane` | Precio mayorista DANE-SIPSA / huevo (Medellín) | DANE-SIPSA wholesale price / egg |

**Nota / Note:** "precio DANE" y "plaza mayorista" son la misma fuente (SIPSA, publicada por el DANE).
El precio del productor es ese mayorista × factor de finca (~0,89). Meses sin SIPSA (G1, pre-2018) → vacío.
