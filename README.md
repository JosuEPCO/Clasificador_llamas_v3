# Clasificador de Dentición en Llamas — versión 3

Aplicación web que clasifica fotografías de los incisivos de llamas (*Lama glama*) en cinco
etapas dentarias y estima la edad aproximada del animal, usando un modelo de clasificación
YOLOv8 entrenado para este fin.

| Etapa | Clase del modelo | Edad aproximada |
|---|---|---|
| Diente de leche menor (Cría) | `DL_menor` | Menor a 1 año |
| Diente de leche mayor (Tui) | `DL_Mayor` | 1 a 2 años |
| 2 dientes | `2D` | 2.5 a 3 años |
| 4 dientes | `4D` | 3.5 a 4 años |
| Boca llena | `BLL` | 4 años y medio a más |

## Estructura

```
version_3/
├── app.py                 # Flujo principal de la aplicación
├── ui.py                  # Componentes visuales (encabezado, paneles, gráficos)
├── etapas.py              # Datos de las cinco etapas dentarias
├── estilos.css            # Estilos y paleta de colores
├── modelo/
│   └── best.pt            # Pesos del modelo YOLOv8 de clasificación
├── .streamlit/
│   └── config.toml        # Tema visual de la aplicación
├── requirements.txt       # Dependencias de Python
└── packages.txt           # Dependencias del sistema (solo para Streamlit Cloud)
```

## Ejecutar en una computadora

Requiere Python 3.10 o superior. Ejecuta los comandos **dentro de esta carpeta**, para que
Streamlit tome la configuración de `.streamlit/config.toml`.

```bash
cd version_3
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
streamlit run app.py
```

La aplicación se abrirá en el navegador en `http://localhost:8501`.

## Publicar en Streamlit Community Cloud

1. Sube el contenido de esta carpeta como raíz de un repositorio de GitHub
   (el modelo pesa ~3 MB, no requiere Git LFS).
2. En [share.streamlit.io](https://share.streamlit.io) elige **Create app**, selecciona el
   repositorio y el archivo principal `app.py`.
3. Streamlit instalará automáticamente `requirements.txt` y `packages.txt`.

## Personalizar colores

Los colores están definidos como variables al inicio de `estilos.css` (bloque `:root`).
Los colores de cada etapa están en `etapas.py` (campo `color`). Si cambias el color
principal (`--accent`), actualiza también `primaryColor` en `.streamlit/config.toml`.

## Créditos

Investigación y desarrollo: **Josue Pari** y **Zaid Alonso** — Producción Animal, Universidad
Nacional del Altiplano (UNA-Puno).
Contacto: jjosuepco@gmail.com

> Las edades estimadas son aproximadas y deben complementarse con la evaluación en campo.
