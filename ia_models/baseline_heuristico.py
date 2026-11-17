"""
Modelo Baseline de razonamiento mediante búsqueda y reglas heurísticas en espacio de estados.
Determina la intervención pedagógica a partir de la distancia al objetivo y entropía de opciones.
Aplica una política determinista estándar sin capacidad adaptativa ante errores recurrentes.
"""

from typing import Tuple, Dict
from ia_models.entorno_simulacion import (
    TipoEstado,
    ACCION_ESPERAR,
    ACCION_PISTA_NIVEL_2,
    TOTAL_CASILLAS,
)

# Factores de ponderación de la función heurística h(s)
PESO_DISTANCIA_CASILLAS: float = 10.0
PESO_PENALIZACION_FALLOS: float = 3.5
PESO_PENALIZACION_INACTIVIDAD: float = 5.0


class BaselineHeuristico:
    """Agente baseline basado en búsqueda heurística y reglas estáticas de decisión."""

    def __init__(self) -> None:
        self.nombre: str = "Baseline Heurístico (Reglas Estáticas)"

    def calcular_heuristica(self, estado: TipoEstado) -> float:
        """
        Calcula la función de evaluación heurística h(s) hacia el estado objetivo.
        Estima el costo restante sumando la distancia de casillas y penalizaciones de bloqueo.
        """
        casilla_activa, intentos_fallidos, _, nivel_inactividad = estado
        distancia_casillas = float(max(0, TOTAL_CASILLAS - casilla_activa))
        penalizacion_fallos = float(intentos_fallidos) * PESO_PENALIZACION_FALLOS
        penalizacion_inactividad = float(nivel_inactividad) * PESO_PENALIZACION_INACTIVIDAD

        return (distancia_casillas * PESO_DISTANCIA_CASILLAS) + penalizacion_fallos + penalizacion_inactividad

    def seleccionar_accion(self, estado: TipoEstado) -> int:
        """
        Determina la acción según política fija determinista:
        - Si no hay fallos ni inactividad: no interviene (esperar).
        - Ante cualquier fallo o inactividad: emite siempre Pista Nivel 2 (Visual CAA fija),
          sin considerar escalamiento adaptativo ni reducción de distractores.
        """
        _, intentos_fallidos, _, nivel_inactividad = estado
        if intentos_fallidos > 0 or nivel_inactividad == 1:
            return ACCION_PISTA_NIVEL_2
        return ACCION_ESPERAR
