"""
Agente principal de razonamiento adaptativo mediante Aprendizaje por Refuerzo (Q-Learning).
Aprende la política óptima de emisión de pistas pedagógicas para minimizar la frustración
y maximizar la autonomía del usuario mediante actualización de diferencias temporales (TD).
"""

from typing import Dict, List, Tuple, Any, Optional
import json
import os
import random
from ia_models.entorno_simulacion import (
    EntornoPictoSecuencias,
    TipoEstado,
    TOTAL_ACCIONES,
    ACCION_ESPERAR,
    ACCION_PISTA_NIVEL_1,
    ACCION_PISTA_NIVEL_2,
    ACCION_PISTA_NIVEL_3,
    GAMMA_DESCUENTO,
    PERFIL_AUTONOMO,
    PERFIL_SEMANTICO_MODERADO,
    PERFIL_DISTRACCION_BLOQUEO,
)

# Parámetros hiperparamétricos de entrenamiento
TASA_APRENDIZAJE_ALFA: float = 0.10
EPSILON_INICIAL: float = 1.0
EPSILON_MINIMO: float = 0.05
DECAIMIENTO_EPSILON: float = 0.995
MAX_PASOS_POR_EPISODIO: int = 30


class AgenteQLearning:
    """Implementación de Q-Learning tabular para tutoría adaptativa en PictoSecuencias."""

    def __init__(
        self,
        tasa_aprendizaje: float = TASA_APRENDIZAJE_ALFA,
        factor_descuento: float = GAMMA_DESCUENTO,
        epsilon_inicial: float = EPSILON_INICIAL,
        epsilon_minimo: float = EPSILON_MINIMO,
        decaimiento_epsilon: float = DECAIMIENTO_EPSILON,
    ) -> None:
        self.nombre: str = "Agente Adaptativo (Q-Learning Tabular)"
        self.alfa: float = tasa_aprendizaje
        self.gamma: float = factor_descuento
        self.epsilon: float = epsilon_inicial
        self.epsilon_min: float = epsilon_minimo
        self.decaimiento: float = decaimiento_epsilon
        self.tabla_q: Dict[str, Dict[int, float]] = {}
        self.historial_recompensas: List[float] = []

    def serializar_estado(self, estado: TipoEstado) -> str:
        """Convierte una tupla de estado discreto en clave única para la tabla Q."""
        return f"{estado[0]}_{estado[1]}_{estado[2]}_{estado[3]}"

    def obtener_valores_q(self, estado: TipoEstado) -> Dict[int, float]:
        """Obtiene o inicializa las estimaciones Q para todas las acciones en un estado."""
        clave = self.serializar_estado(estado)
        if clave not in self.tabla_q:
            self.tabla_q[clave] = {accion: 0.0 for accion in range(TOTAL_ACCIONES)}
        return self.tabla_q[clave]

    def seleccionar_accion(self, estado: TipoEstado, en_entrenamiento: bool = False) -> int:
        """
        Selecciona la acción pedagógica utilizando la política epsilon-greedy.
        En inferencia/evaluación (en_entrenamiento=False), actúa de forma completamente explotadora.
        """
        if en_entrenamiento and random.random() < self.epsilon:
            return random.randint(0, TOTAL_ACCIONES - 1)

        valores_q = self.obtener_valores_q(estado)
        max_valor = max(valores_q.values())
        mejores_acciones = [acc for acc, val in valores_q.items() if val == max_valor]
        return random.choice(mejores_acciones)

    def actualizar(
        self,
        estado: TipoEstado,
        accion: int,
        recompensa: float,
        estado_siguiente: TipoEstado,
        terminado: bool,
    ) -> float:
        """
        Aplica la regla de actualización de Bellman para Q-Learning:
        Q(s, a) <- Q(s, a) + alfa * [ R + gamma * max_a' Q(s', a') - Q(s, a) ]
        """
        clave_estado = self.serializar_estado(estado)
        q_actual = self.obtener_valores_q(estado)[accion]

        if terminado:
            objetivo = recompensa
        else:
            q_siguiente = self.obtener_valores_q(estado_siguiente)
            max_q_siguiente = max(q_siguiente.values())
            objetivo = recompensa + (self.gamma * max_q_siguiente)

        nuevo_q = q_actual + self.alfa * (objetivo - q_actual)
        self.tabla_q[clave_estado][accion] = nuevo_q
        return nuevo_q

    def decaer_exploracion(self) -> None:
        """Reduce progresivamente la tasa de exploración epsilon."""
        if self.epsilon > self.epsilon_min:
            self.epsilon = max(self.epsilon_min, self.epsilon * self.decaimiento)

    def entrenar(self, entorno: EntornoPictoSecuencias, total_episodios: int = 5000) -> List[float]:
        """
        Ejecuta el ciclo de entrenamiento a lo largo de un número fijado de episodios,
        muestreando perfiles balanceados de Kallpa para generalización robusta.
        """
        perfiles = [PERFIL_AUTONOMO, PERFIL_SEMANTICO_MODERADO, PERFIL_DISTRACCION_BLOQUEO]
        self.historial_recompensas = []

        for episodio in range(total_episodios):
            perfil_actual = perfiles[episodio % len(perfiles)]
            entorno.cambiar_perfil(perfil_actual)
            estado = entorno.reiniciar()
            recompensa_acumulada = 0.0
            terminado = False
            pasos = 0

            while not terminado and pasos < MAX_PASOS_POR_EPISODIO:
                pasos += 1
                accion = self.seleccionar_accion(estado, en_entrenamiento=True)
                estado_siguiente, recompensa, terminado, _ = entorno.ejecutar_paso(accion)

                self.actualizar(estado, accion, recompensa, estado_siguiente, terminado)
                recompensa_acumulada += recompensa
                estado = estado_siguiente

            self.decaer_exploracion()
            self.historial_recompensas.append(recompensa_acumulada)

        return self.historial_recompensas

    def guardar_modelo(self, ruta_archivo: str) -> None:
        """Persiste la matriz Q aprendida y el historial de entrenamiento en formato JSON."""
        directorio = os.path.dirname(ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

        datos = {
            "hiperparametros": {
                "alfa": self.alfa,
                "gamma": self.gamma,
                "epsilon_final": self.epsilon,
            },
            "estados_aprendidos": len(self.tabla_q),
            "tabla_q": self.tabla_q,
            "historial_recompensas": self.historial_recompensas,
        }

        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=2)

    def cargar_modelo(self, ruta_archivo: str) -> None:
        """Recupera la política óptima desde el archivo JSON serializado."""
        if not os.path.exists(ruta_archivo):
            return

        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            if "tabla_q" in datos:
                self.tabla_q = {
                    clave: {int(acc): float(val) for acc, val in acciones.items()}
                    for clave, acciones in datos["tabla_q"].items()
                }
                self.historial_recompensas = datos.get("historial_recompensas", [])
