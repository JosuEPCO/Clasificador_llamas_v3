"""Etapas de la cronología dentaria en llamas, en orden cronológico."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Etapa:
    clave: str              # Nombre de la clase en el modelo YOLO
    nombre: str
    categoria: str | None
    edad: str
    detalle: str
    permanentes: int        # Incisivos inferiores permanentes (de 6)
    color: str              # Paso de la rampa ordinal terracota (claro → oscuro)
    desgaste: bool = False  # Dientes de leche con desgaste visible


# Rampa ordinal de un solo tono, validada: luminosidad monótona, ΔL ≥ 0.06
# entre pasos y el paso más claro a 2.34:1 sobre la superficie.
ETAPAS = (
    Etapa("DL_menor", "Diente de leche menor", "Cría", "Menor a 1 año",
          "Dientes de leche sin desgaste", 0, "#E69373"),
    Etapa("DL_Mayor", "Diente de leche mayor", "Tui", "1 a 2 años",
          "Dientes de leche con desgaste", 0, "#D0724C", desgaste=True),
    Etapa("2D", "2 dientes", None, "2.5 a 3 años",
          "Primer par de incisivos permanentes", 2, "#B65329"),
    Etapa("4D", "4 dientes", None, "3.5 a 4 años",
          "Segundo par de incisivos permanentes", 4, "#903F1C"),
    Etapa("BLL", "Boca llena", None, "4 años y medio a más",
          "Todos los incisivos permanentes", 6, "#692F17"),
)

POR_CLAVE = {etapa.clave: etapa for etapa in ETAPAS}


def buscar(clave):
    """Devuelve la etapa de una clase del modelo, o una genérica si no se reconoce."""
    return POR_CLAVE.get(clave) or Etapa(clave, clave, None, "Edad no determinada", "", 0, "#75685C")


def posicion(etapa):
    """Número de etapa (1-5) o None si no pertenece a la cronología."""
    return next((i for i, e in enumerate(ETAPAS, 1) if e.clave == etapa.clave), None)
