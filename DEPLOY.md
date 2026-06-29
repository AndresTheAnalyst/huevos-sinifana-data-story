# Publicar el portafolio — paso a paso

Dos pasos: **(A)** subir la carpeta a un repo público de GitHub y **(B)** desplegar el dashboard en Streamlit Community Cloud (gratis). Al final tenés un **link en vivo** para pegar en LinkedIn.

> Esta carpeta es **autocontenida**: es la raíz del repo público. Las rutas del app (`app/app.py`) ya apuntan a `data/` y `app/assets/` relativo a la raíz, así que funciona tal cual en la nube.

---

## A · Repo público en GitHub

> ⚠️ El repo será **público** e incluye los datos reales de Huevos Sinifana (con permiso del propietario). Confirmá que estás de acuerdo antes de publicar.

**Opción guiada (la hace El Salo con tu OK):** decime el nombre del repo y yo corro los comandos.

**Opción manual:**
1. En GitHub → **New repository** → nombre (ej. `huevos-sinifana-data-story`) → **Public** → *Create*.
2. En una terminal, desde esta carpeta:
   ```bash
   cd portafolio-huevos-sinifana
   git init -b main
   git add .
   git commit -m "Huevos Sinifana — data story (dashboard + notebook)"
   git remote add origin https://github.com/AndresTheAnalyst/<nombre-del-repo>.git
   git push -u origin main
   ```
3. (Recordá que los push grandes a veces fallan; los assets acá son chicos, debería ir liviano.)

---

## B · Deploy en Streamlit Community Cloud (gratis)

1. Entrá a **https://share.streamlit.io** e iniciá sesión con tu cuenta de **GitHub**.
2. Botón **"Create app"** → **"Deploy a public app from GitHub"**.
3. Completá:
   - **Repository:** `AndresTheAnalyst/<nombre-del-repo>`
   - **Branch:** `main`
   - **Main file path:** `app/app.py`
4. **Deploy**. Tarda 1–2 min en instalar `requirements.txt` y arrancar.
5. Te queda un link tipo `https://<algo>.streamlit.app` — **ese es el que pegás en LinkedIn**.
6. Copiá ese link y pegámelo: lo pongo en el README (donde dice *"pega aquí tu link de Streamlit Cloud"*).

---

## Mantenimiento

- Cada vez que hagas `git push` a `main`, Streamlit Cloud **redespliega solo**.
- Para refrescar los datos: corré `python scripts/construir_datos.py`, commiteá y pusheá.
- El tablero corre en modo **solo lectura** (no escribe nada).
