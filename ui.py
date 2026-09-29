"""Componentes visuales de la aplicación (HTML renderizado con st.markdown)."""

import base64
from html import escape
from io import BytesIO

import streamlit as st

from etapas import ETAPAS, posicion

UMBRAL_ALTA = 80
UMBRAL_MODERADA = 50


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def cargar_estilos(ruta):
    st.markdown(f"<style>{ruta.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def mostrar(bloque, destino=st):
    """Renderiza HTML sin sangrías ni líneas vacías, para que Markdown no lo altere."""
    lineas = [linea.strip() for linea in bloque.splitlines() if linea.strip()]
    destino.markdown("\n".join(lineas), unsafe_allow_html=True)


def imagen_base64(imagen, lado_max=1400):
    vista = imagen.copy()
    vista.thumbnail((lado_max, lado_max))
    buffer = BytesIO()
    vista.save(buffer, format="JPEG", quality=88)
    return base64.b64encode(buffer.getvalue()).decode()


def porcentaje(valor):
    return f"{valor:.0f}%" if valor >= 99.95 else f"{valor:.1f}%"


def nivel_confianza(valor):
    if valor >= UMBRAL_ALTA:
        return ("alta", "Alta", ICONOS["ok"],
                "La predicción es consistente. Aun así, confirma en campo si el animal está en el límite entre dos etapas.")
    if valor >= UMBRAL_MODERADA:
        return ("moderada", "Moderada", ICONOS["alerta"],
                "Revisa la distribución de probabilidades: la etapa vecina podría ser también plausible.")
    return ("baja", "Baja", ICONOS["error"],
            "Se recomienda tomar otra fotografía más nítida y frontal de los incisivos antes de concluir.")


# ---------------------------------------------------------------------------
# Iconos y esquema dental
# ---------------------------------------------------------------------------

def _icono(trazos, tam=18):
    return (f'<svg class="icono" width="{tam}" height="{tam}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{trazos}</svg>')


ICONOS = {
    "ok": _icono('<circle cx="12" cy="12" r="9"/><path d="m8.5 12.5 2.5 2.5 4.5-5"/>'),
    "alerta": _icono('<path d="M12 4 2.8 19.5a1 1 0 0 0 .9 1.5h16.6a1 1 0 0 0 .9-1.5L12 4Z"/>'
                     '<path d="M12 10v4"/><path d="M12 17.5h.01"/>'),
    "error": _icono('<circle cx="12" cy="12" r="9"/><path d="M12 8v5"/><path d="M12 16.5h.01"/>'),
    "reloj": _icono('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>', tam=14),
}


def svg_incisivos(nivel, color="#B65329", desgaste=None):
    """Esquema frontal de los seis incisivos inferiores (nivel 0 = cría … 4 = boca llena)."""
    pares_permanentes = (0, 0, 1, 2, 3)[nivel]
    desgaste = nivel == 1 if desgaste is None else desgaste
    dientes = []
    for x, par in zip((15, 33, 51, 69, 87, 105), (3, 2, 1, 1, 2, 3)):
        base = 47 - 4 * (1 - ((x - 60) / 58) ** 2)
        if par <= pares_permanentes:
            ancho, alto, radio = 15, 31, 6.5
            relleno, borde = "#FFFDF7", color
        else:
            ancho = 12
            alto, radio = (13, 3) if desgaste else (19, 5.5)
            relleno, borde = "#F4E9D6", "#C9B28E"
        dientes.append(
            f'<rect x="{x - ancho / 2:.1f}" y="{base - alto:.1f}" width="{ancho}" '
            f'height="{alto + 10}" rx="{radio}" fill="{relleno}" stroke="{borde}" stroke-width="1.6"/>'
        )

    permanentes = pares_permanentes * 2
    descripcion = f"{permanentes} incisivos permanentes y {6 - permanentes} de leche"
    if desgaste:
        descripcion += " con desgaste"
    encia = '<path d="M2 48 Q60 38 118 48 L118 58 Q60 66 2 58 Z" fill="#E9B0A4" stroke="#D0897C" stroke-width="1.2"/>'
    return (f'<svg viewBox="0 0 120 64" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="Esquema de incisivos inferiores: {descripcion}">'
            + "".join(dientes) + encia + "</svg>")


def svg_etapa(etapa):
    nivel = (posicion(etapa) or 3) - 1
    return svg_incisivos(nivel, etapa.color, etapa.desgaste)


LEYENDA_DIENTES = """
<div class="leyenda">
    <span><i class="sw-perm"></i>Permanente</span>
    <span><i class="sw-leche"></i>De leche</span>
</div>
"""


# ---------------------------------------------------------------------------
# Estructura general
# ---------------------------------------------------------------------------

def barra_lateral():
    return """
    <div class="sb-brand">
        <div class="sb-logo" aria-hidden="true">🦙</div>
        <div><b>Dentición en Llamas</b><small>Visión computacional · YOLO</small></div>
    </div>
    <div class="sb-section">Sobre el proyecto</div>
    <div class="sb-text">
        Herramienta de visión computacional que automatiza la evaluación de la cronología
        dentaria en llamas, optimizando el diagnóstico de edad en campo.
    </div>
    <div class="sb-section">Cómo usarla</div>
    <ol class="sb-steps">
        <li><span>Toma una fotografía clara y frontal de los incisivos.</span></li>
        <li><span>Súbela en el panel principal.</span></li>
        <li><span>Presiona <b>Analizar dentición</b>.</span></li>
    </ol>
    <div class="sb-section">Investigación y desarrollo</div>
    <div class="sb-card">
        <div class="label">Investigadores</div>
        <div><b>Josue Pari</b> · <b>Zaid Alonso</b></div>
        <div class="label sb-gap">Contacto</div>
        <a href="mailto:jjosuepco@gmail.com">jjosuepco@gmail.com</a>
    </div>
    <div class="sb-foot">Desarrollado para la investigación en Producción Animal — UNA-Puno.</div>
    """


def hero():
    return f"""
    <header class="hero">
        <div class="hero-inner">
            <div>
                <div class="hero-eyebrow">Producción Animal · UNA-Puno</div>
                <div class="hero-title" role="heading" aria-level="1">Clasificador automatizado de <em>dentición en llamas</em></div>
                <p class="lead">Sube una fotografía de los incisivos y el modelo identificará la etapa
                zootécnica del animal junto con su edad aproximada.</p>
                <div class="hero-stats">
                    <span class="hero-stat"><b>5</b>etapas dentarias</span>
                    <span class="hero-stat"><b>YOLOv8</b>clasificación</span>
                    <span class="hero-stat"><b>Cría</b>a boca llena</span>
                </div>
            </div>
            <div class="hero-art" aria-hidden="true">
                {svg_incisivos(4, "#E9A37A")}
                <div class="cap">Incisivos inferiores · vista frontal</div>
            </div>
        </div>
        <div class="band" aria-hidden="true"></div>
    </header>
    """


def encabezado_seccion(numero, titulo, subtitulo=None):
    sub = f'<div class="sec-sub">{subtitulo}</div>' if subtitulo else ""
    return f"""
    <div class="sec-head">
        <span class="sec-num" aria-hidden="true">{numero}</span>
        <span class="sec-title" role="heading" aria-level="2">{titulo}</span>
    </div>
    {sub}
    """


def pie():
    return """
    <footer class="footer">
        <span>Clasificador de Dentición en Llamas · Producción Animal, UNA-Puno</span>
        <span>Las edades son aproximadas y deben complementarse con la evaluación en campo.</span>
    </footer>
    """


# ---------------------------------------------------------------------------
# Imagen y avisos
# ---------------------------------------------------------------------------

def vista_previa(b64, nombre, tamano):
    ancho, alto = tamano
    return f"""
    <figure class="photo">
        <img src="data:image/jpeg;base64,{b64}" alt="Fotografía ingresada: {escape(nombre)}">
        <figcaption class="photo-meta">
            <span>{escape(nombre)}</span>
            <span>{ancho} × {alto} px</span>
        </figcaption>
    </figure>
    """


def aviso(tipo, titulo, texto, icono):
    rol = "alert" if tipo == "baja" else "status"
    return f"""
    <div class="note is-{tipo}" role="{rol}">
        {icono}<div><b>{titulo}.</b> {texto}</div>
    </div>
    """


def aviso_imagen_invalida():
    return aviso("baja", "No se pudo leer la imagen",
                 "El archivo está dañado o no es una imagen válida. Prueba con otro JPG o PNG.", ICONOS["error"])


def error_modelo(ruta):
    texto = (f"No se encontró el archivo <code>{ruta}</code>. Colócalo en la carpeta "
             "<code>modelo</code> junto a <code>app.py</code> y recarga la página.")
    return f'<div class="card">{aviso("baja", "No se pudo cargar el modelo", texto, ICONOS["error"])}</div>'


# ---------------------------------------------------------------------------
# Panel de diagnóstico
# ---------------------------------------------------------------------------

def panel_vacio(con_imagen):
    if con_imagen:
        titulo = "Imagen lista para analizar"
        texto = "Presiona <b>Analizar dentición</b> para obtener la etapa y la edad estimada."
    else:
        titulo = "Esperando una fotografía"
        texto = "Sube una imagen de los incisivos de la llama para iniciar el análisis."
    return f"""
    <div class="card empty" role="status" aria-live="polite">
        {svg_incisivos(2)}
        <div class="card-title">{titulo}</div>
        <p>{texto}</p>
        <div class="tips">
            <div class="tip"><b>Encuadre</b>Incisivos inferiores de frente, labios retraídos.</div>
            <div class="tip"><b>Luz</b>Luz natural difusa, sin sombras fuertes.</div>
            <div class="tip"><b>Enfoque</b>Imagen nítida, sin movimiento.</div>
            <div class="tip"><b>Distancia</b>La boca debe ocupar gran parte de la foto.</div>
        </div>
    </div>
    """


def panel_cargando():
    return """
    <div class="card result" aria-busy="true">
        <div class="result-accent skeleton"></div>
        <div class="result-body">
            <div class="eyebrow">Analizando características morfológicas…</div>
            <div class="skeleton" style="width:65%;height:36px;margin-top:12px"></div>
            <div class="skeleton" style="width:45%;height:26px;margin-top:14px"></div>
            <div class="skeleton" style="width:100%;height:96px;margin-top:22px"></div>
            <div class="skeleton" style="width:100%;height:44px;margin-top:16px"></div>
        </div>
    </div>
    """


def _anillo(confianza, tipo, etiqueta):
    grados = confianza * 3.6
    return f"""
    <div class="ring is-{tipo}" role="meter" aria-label="Confianza del modelo"
         aria-valuemin="0" aria-valuemax="100" aria-valuenow="{confianza:.1f}"
         aria-valuetext="{porcentaje(confianza)}, confianza {etiqueta.lower()}"
         style="background:conic-gradient(var(--estado) 0 {grados:.1f}deg, var(--estado-track) {grados:.1f}deg 360deg)">
        <span class="ring-ticks" aria-hidden="true"></span>
        <div class="ring-inner"><b>{porcentaje(confianza)}</b><small>{etiqueta}</small></div>
    </div>
    """


def _distribucion(probabilidades, clave_top):
    claves = [e.clave for e in ETAPAS if e.clave in probabilidades]
    claves += [c for c in probabilidades if c not in claves]
    nombres = {e.clave: e.nombre for e in ETAPAS}
    filas = ""
    for clave in claves:
        valor = probabilidades[clave] * 100
        nombre = escape(nombres.get(clave, clave))
        es_top = clave == clave_top
        marca = '<span class="tag-pred">Predicción</span>' if es_top else ""
        filas += f"""
        <li class="prob-row{' top' if es_top else ''}" title="{nombre}: {valor:.1f}%">
            <div class="prob-head">
                <span class="prob-name">{nombre}{marca}</span>
                <span class="prob-val">{valor:.1f}%</span>
            </div>
            <div class="prob-track" aria-hidden="true"><div class="prob-fill" style="width:{valor:.1f}%"></div></div>
        </li>
        """
    return f"""
    <div class="card probs">
        <div class="card-title">Distribución de probabilidades</div>
        <div class="card-help">Probabilidad asignada por el modelo a cada etapa, en orden cronológico.</div>
        <ul class="prob-list">{filas}</ul>
    </div>
    """


def panel_resultado(etapa, resultado):
    confianza = resultado["confianza"]
    tipo, etiqueta, icono, consejo = nivel_confianza(confianza)
    numero = posicion(etapa)
    ubicacion = f"Etapa {numero} de {len(ETAPAS)}" if numero else "Etapa no reconocida"
    ancho, alto = resultado["tamano"]

    chips = ""
    if etapa.categoria:
        chips += f'<span class="chip chip-soft"><i style="background:{etapa.color}"></i>{etapa.categoria}</span>'
    chips += f'<span class="chip chip-dark">{ICONOS["reloj"]}{etapa.edad}</span>'

    return f"""
    <div class="card result" aria-live="polite">
        <div class="result-accent" style="background:{etapa.color}"></div>
        <div class="result-body">
            <div class="result-top">
                <div>
                    <div class="eyebrow">Etapa dentaria · {ubicacion}</div>
                    <div class="result-stage" role="heading" aria-level="3">{escape(etapa.nombre)}</div>
                    <div class="chips">{chips}</div>
                </div>
                {_anillo(confianza, tipo, etiqueta)}
            </div>
            <div class="teeth-box">
                {svg_etapa(etapa)}
                <div>
                    <div class="t-title">Edad estimada: {etapa.edad}</div>
                    <div class="t-text">{etapa.detalle}</div>
                    <div class="t-text">Incisivos permanentes: <b>{etapa.permanentes} de 6</b></div>
                    {LEYENDA_DIENTES}
                </div>
            </div>
            {aviso(tipo, f"Confianza {etiqueta.lower()}", consejo, icono)}
            <div class="result-meta">
                <span>Tiempo de análisis: {resultado["ms"]:.0f} ms</span>
                <span>Imagen: {ancho} × {alto} px</span>
            </div>
        </div>
    </div>
    {_distribucion(resultado["probabilidades"], etapa.clave)}
    """


# ---------------------------------------------------------------------------
# Guía de etapas
# ---------------------------------------------------------------------------

def guia_etapas(clave_activa=None):
    tarjetas = ""
    for i, etapa in enumerate(ETAPAS):
        activa = etapa.clave == clave_activa
        estilo = f' style="border-color:{etapa.color}"' if activa else ""
        insignia = '<span class="badge">Resultado</span>' if activa else ""
        categoria = f" · {etapa.categoria}" if etapa.categoria else ""
        tarjetas += f"""
        <li class="stage{' active' if activa else ''}"{' aria-current="step"' if activa else ''}>
            <div class="stage-track" aria-hidden="true"><span class="stage-dot" style="background:{etapa.color}"></span><span class="stage-line"></span></div>
            <div class="stage-card"{estilo}>
                {insignia}
                {svg_incisivos(i, etapa.color)}
                <div class="s-num">Etapa {i + 1}{categoria}</div>
                <div class="s-name">{etapa.nombre}</div>
                <div class="s-age">{etapa.edad}</div>
                <div class="s-detail">{etapa.detalle}</div>
            </div>
        </li>
        """
    return f"""
    <section class="guide-section">
        <div class="guide-head">
            <div>
                {encabezado_seccion("03", "Guía de etapas dentarias",
                                    "Cronología de erupción de los incisivos inferiores permanentes en llamas.")}
            </div>
            {LEYENDA_DIENTES}
        </div>
        <ol class="guide">{tarjetas}</ol>
    </section>
    """
