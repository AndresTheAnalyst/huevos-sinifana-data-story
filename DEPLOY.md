# Publicación y mantenimiento

Este proyecto **ya está publicado**:

- **Repo público:** https://github.com/AndresTheAnalyst/huevos-sinifana-data-story
- **Dashboard en vivo:** https://huevos-sinifana-data-story.streamlit.app/ (Streamlit Community Cloud, main file `app/app.py`)

> La carpeta es **autocontenida**: es la raíz del repo. Las rutas del app (`app/app.py`) apuntan a `data/` y `app/assets/` relativo a la raíz, así que funciona igual local y en la nube.

---

## Mantenimiento (el ciclo normal)

1. Editar lo que sea (app, datos, README).
2. Si cambió la **fuente de datos**: correr `python scripts/construir_datos.py` (regenera los CSV de `data/`) y, si aplica, `python notebooks/_make_figures.py` (regenera las figuras del notebook).
3. Probar local: `streamlit run app/app.py`.
4. `git add . && git commit -m "..." && git push` → Streamlit Cloud **redespliega solo** en 1–2 min.

El tablero corre en modo **solo lectura** (no escribe nada).

## Visibilidad (importante)

La app debe estar **pública** para que cualquiera la vea sin iniciar sesión. Para verificarlo:
abrir el link en una **ventana de incógnito** — debe cargar el dashboard directo, sin pedir login.
Si pide login: en https://share.streamlit.io → menú de la app (⋮) → **Settings** → **Sharing** →
activar que cualquiera con el link pueda verla (público).

## Si hay que re-desplegar desde cero

1. https://share.streamlit.io → **Create app** → *Deploy a public app from GitHub*.
2. Repository `AndresTheAnalyst/huevos-sinifana-data-story` · Branch `main` · Main file `app/app.py`.
3. Deploy (instala `requirements.txt` y arranca en 1–2 min).
