"""
Entorno de simulación de PictoSecuencias basado en un Proceso de Decisión de Markov (MDP).
Desacoplado de la interfaz gráfica de Pygame para permitir entrenamiento acelerado,
experimentación estocástica y evaluación empírica de agentes inteligentes.

Formalización Matemática del MDP:
----------------------------------
El problema pedagógico de tutoría adaptativa se modela como una tupla M = (S, A, T, R, gamma):

1. Espacio de Estados (S):
   Tupla discreta s = (casilla_activa, intentos_fallidos_casilla, nivel_pista_actual, nivel_inactividad)
   - casilla_activa in {0, 1, 2}: Posición actual en la estructura sintáctica canónica
     (0: Sujeto, 1: Verbo, 2: Complemento). Terminal al alcanzar 3.
   - intentos_fallidos_casilla in {0, 1, 2, 3}: Contador discreto acotado de errores consecutivos
     en la casilla en evaluación.
   - nivel_pista_actual in {0, 1, 2, 3}: Nivel de asistencia visual/auditiva provisto recientemente
     en la casilla activa (0: ninguna intervención previa).
   - nivel_inactividad in {0, 1}: Indicador binario de temporizador de 25 segundos
     (0: usuario activo < 25s, 1: usuario inactivo >= 25s).
   Card(S) = 3 x 4 x 4 x 2 = 96 estados transitivos + estados terminales.

2. Espacio de Acciones del Agente (A):
   Intervenciones pedagógicas discretas a in {0, 1, 2, 3}:
   - a = 0 (No intervenir / Esperar): Fomenta la autonomía del usuario si se encuentra activo.
   - a = 1 (Pista Nivel 1 - Verbal suave): Pregunta orientadora en texto y locución TTS.
   - a = 2 (Pista Nivel 2 - Apoyo Visual CAA): Pregunta + TTS + Pictograma universal orientador.
   - a = 3 (Pista Nivel 3 - Reducción cognitiva): Pista bimodal completa + atenuación de distractores.

3. Función de Transición T(s' | s, a):
   Distribución estocástica condicionada por el perfil sintético de usuario de Kallpa
   (Autónomo, Dificultad Semántica Moderada o Alta Distracción/Inactividad) y la pertinencia
   de la acción ejecutada por el agente inteligente.

4. Función de Recompensa R(s, a, s'):
   Disenada para balancear la asimilación sintáctica independiente y la prevención de frustración:
   - +15.0: Acierto autónomo con mínima intervención (a = 0 en estado sin bloqueo).
   -  +8.0: Acierto asistido tras emitir una pista pedagógicamente adecuada.
   -  -3.0: Penalización por sobreasistencia prematura (pistas altas sin error previo) o repetición
            ineficaz del mismo nivel de pista tras un fallo persistente.
   - -10.0: Penalización severa por subasistencia (esperar a = 0 cuando el usuario acumula >= 2
            fallos o sufre inactividad >= 25s).

5. Factor de Descuento (gamma):
   gamma = 0.95: Equilibra la optimización del proceso de aprendizaje de la oración completa
   con la efectividad de la retroalimentación inmediata.
"""

from typing import Tuple, Dict, Any, Optional
import random

# Constantes del espacio de estados
TOTAL_CASILLAS: int = 3
LIMITE_FALLOS_DISCRETOS: int = 3
TOTAL_NIVELES_PISTA: int = 4
SEGUNDOS_UMBRAL_INACTIVIDAD: float = 25.0

# Acciones pedagógicas disponibles
ACCION_ESPERAR: int = 0
ACCION_PISTA_NIVEL_1: int = 1
ACCION_PISTA_NIVEL_2: int = 2
ACCION_PISTA_NIVEL_3: int = 3
TOTAL_ACCIONES: int = 4

# Recompensas y penalizaciones del MDP
RECOMPENSA_ACIERTO_AUTONOMO: float = 15.0
RECOMPENSA_ACIERTO_ASISTIDO: float = 8.0
PENALIZACION_SOBREASISTENCIA: float = -3.0
PENALIZACION_SUBASISTENCIA: float = -10.0
PENALIZACION_PASO_FALLIDO: float = -1.0

# Factor de descuento del MDP
GAMMA_DESCUENTO: float = 0.95

# Nombres canónicos de perfiles de usuario
PERFIL_AUTONOMO: str = "autonomo"
PERFIL_SEMANTICO_MODERADO: str = "semantico_moderado"
PERFIL_DISTRACCION_BLOQUEO: str = "distraccion_bloqueo"

TipoEstado = Tuple[int, int, int, int]


class PerfilJugador:
    """Modelo estocástico de respuesta para perfiles de beneficiarios de Kallpa."""

    def __init__(self, tipo_perfil: str) -> None:
        self.tipo_perfil: str = tipo_perfil
        self._configurar_probabilidades()

    def _configurar_probabilidades(self) -> None:
        # Asignación de matrices empíricas de acierto e inactividad según perfil clínico
        if self.tipo_perfil == PERFIL_AUTONOMO:
            self.probabilidad_inactividad_base: float = 0.05
            self.probabilidad_acierto_base: float = 0.75
            self.efectividad_pistas: Dict[int, float] = {
                ACCION_ESPERAR: 0.75,
                ACCION_PISTA_NIVEL_1: 0.95,
                ACCION_PISTA_NIVEL_2: 0.98,
                ACCION_PISTA_NIVEL_3: 0.99,
            }
        elif self.tipo_perfil == PERFIL_SEMANTICO_MODERADO:
            self.probabilidad_inactividad_base = 0.20
            self.probabilidad_acierto_base = 0.35
            self.efectividad_pistas = {
                ACCION_ESPERAR: 0.35,
                ACCION_PISTA_NIVEL_1: 0.65,
                ACCION_PISTA_NIVEL_2: 0.88,
                ACCION_PISTA_NIVEL_3: 0.96,
            }
        elif self.tipo_perfil == PERFIL_DISTRACCION_BLOQUEO:
            self.probabilidad_inactividad_base = 0.50
            self.probabilidad_acierto_base = 0.20
            self.efectividad_pistas = {
                ACCION_ESPERAR: 0.20,
                ACCION_PISTA_NIVEL_1: 0.40,
                ACCION_PISTA_NIVEL_2: 0.72,
                ACCION_PISTA_NIVEL_3: 0.94,
            }
        else:
            # Perfil equilibrado por defecto
            self.probabilidad_inactividad_base = 0.15
            self.probabilidad_acierto_base = 0.50
            self.efectividad_pistas = {
                ACCION_ESPERAR: 0.50,
                ACCION_PISTA_NIVEL_1: 0.70,
                ACCION_PISTA_NIVEL_2: 0.85,
                ACCION_PISTA_NIVEL_3: 0.95,
            }

    def simular_respuesta(self, accion_agente: int, estaba_inactivo: bool) -> Tuple[bool, bool]:
        """Determina estocásticamente si el usuario acierta la casilla y si experimenta inactividad."""
        # Las intervenciones activas (1, 2 o 3) rompen el estado de inactividad
        if accion_agente > ACCION_ESPERAR:
            queda_inactivo = random.random() < (self.probabilidad_inactividad_base * 0.25)
        else:
            queda_inactivo = random.random() < (0.60 if estaba_inactivo else self.probabilidad_inactividad_base)

        probabilidad_acierto = self.efectividad_pistas.get(accion_agente, self.probabilidad_acierto_base)
        acierta = random.random() < probabilidad_acierto
        return acierta, queda_inactivo


class EntornoPictoSecuencias:
    """Entorno de simulación formal MDP para tutoría pedagógica adaptativa."""

    def __init__(self, tipo_perfil: str = PERFIL_SEMANTICO_MODERADO) -> None:
        self.tipo_perfil: str = tipo_perfil
        self.simulador_jugador: PerfilJugador = PerfilJugador(tipo_perfil)
        self.casilla_activa: int = 0
        self.intentos_fallidos: int = 0
        self.nivel_pista_actual: int = 0
        self.nivel_inactividad: int = 0
        self.pasos_episodio: int = 0

    def cambiar_perfil(self, nuevo_perfil: str) -> None:
        """Modifica dinámicamente el perfil del usuario para pruebas cruzadas."""
        self.tipo_perfil = nuevo_perfil
        self.simulador_jugador = PerfilJugador(nuevo_perfil)

    def reiniciar(self) -> TipoEstado:
        """Restablece los contadores para iniciar un nuevo episodio oracional."""
        self.casilla_activa = 0
        self.intentos_fallidos = 0
        self.nivel_pista_actual = 0
        self.nivel_inactividad = 0
        self.pasos_episodio = 0
        return self.obtener_estado()

    def obtener_estado(self) -> TipoEstado:
        """Genera la representación discreta canónica del estado actual."""
        fallos_acotados = min(self.intentos_fallidos, LIMITE_FALLOS_DISCRETOS)
        return (
            self.casilla_activa,
            fallos_acotados,
            self.nivel_pista_actual,
            self.nivel_inactividad,
        )

    def calcular_recompensa(self, accion: int, acierto: bool) -> float:
        """Evalúa la pertinencia pedagógica de la acción respecto al estado del usuario."""
        # Penalización grave por desatención a usuarios bloqueados
        if accion == ACCION_ESPERAR and (self.intentos_fallidos >= 2 or self.nivel_inactividad == 1):
            return PENALIZACION_SUBASISTENCIA

        # Penalización por sobreasistencia sin necesidad
        if accion in (ACCION_PISTA_NIVEL_2, ACCION_PISTA_NIVEL_3) and self.intentos_fallidos == 0 and self.nivel_inactividad == 0:
            return PENALIZACION_SOBREASISTENCIA

        # Penalización por repetir la misma pista sin mejoría
        if accion > ACCION_ESPERAR and accion == self.nivel_pista_actual and self.intentos_fallidos > 0:
            return PENALIZACION_SOBREASISTENCIA

        if acierto:
            # Premia la autonomía cuando no hubo necesidad de pistas complejas
            if accion == ACCION_ESPERAR and self.intentos_fallidos == 0:
                return RECOMPENSA_ACIERTO_AUTONOMO
            return RECOMPENSA_ACIERTO_ASISTIDO

        return PENALIZACION_PASO_FALLIDO

    def ejecutar_paso(self, accion: int) -> Tuple[TipoEstado, float, bool, Dict[str, Any]]:
        """Aplica una intervención del agente y simula la transición del entorno."""
        self.pasos_episodio += 1
        estaba_inactivo = (self.nivel_inactividad == 1)

        acierto, queda_inactivo = self.simulador_jugador.simular_respuesta(accion, estaba_inactivo)
        recompensa = self.calcular_recompensa(accion, acierto)

        # Actualización de estados según el resultado de la interacción
        if acierto:
            self.casilla_activa += 1
            self.intentos_fallidos = 0
            self.nivel_pista_actual = 0
            self.nivel_inactividad = 0
        else:
            self.intentos_fallidos += 1
            if accion > ACCION_ESPERAR:
                self.nivel_pista_actual = accion
            self.nivel_inactividad = 1 if queda_inactivo else 0

        terminado = self.casilla_activa >= TOTAL_CASILLAS
        info: Dict[str, Any] = {
            "acierto": acierto,
            "pasos_totales": self.pasos_episodio,
            "perfil": self.tipo_perfil,
        }

        return self.obtener_estado(), recompensa, terminado, info


if __name__ == "__main__":
    print("=" * 70)
    print("PRUEBA RÁPIDA DE TRANSICIONES Y RECOMPENSAS: EntornoPictoSecuencias")
    print("=" * 70)

    entorno = EntornoPictoSecuencias(tipo_perfil=PERFIL_SEMANTICO_MODERADO)
    estado_inicial = entorno.reiniciar()
    print(f"Estado inicial s_0: {estado_inicial} (Casilla, Fallos, Pista, Inactividad)\n")

    acciones_nombres = {
        ACCION_ESPERAR: "0 (Esperar)",
        ACCION_PISTA_NIVEL_1: "1 (Pista Verbal)",
        ACCION_PISTA_NIVEL_2: "2 (Pista Visual CAA)",
        ACCION_PISTA_NIVEL_3: "3 (Reducción Cognitiva)",
    }

    for paso in range(1, 6):
        accion_aleatoria = random.choice([
            ACCION_ESPERAR,
            ACCION_PISTA_NIVEL_1,
            ACCION_PISTA_NIVEL_2,
            ACCION_PISTA_NIVEL_3,
        ])
        s_siguiente, recompensa, terminado, info = entorno.ejecutar_paso(accion_aleatoria)
        print(f"Paso {paso}:")
        print(f"  Acción del tutor : {acciones_nombres[accion_aleatoria]}")
        print(f"  Acierto usuario  : {info['acierto']}")
        print(f"  Recompensa R     : {recompensa:+.1f}")
        print(f"  Estado s'        : {s_siguiente}")
        print(f"  ¿Episodio final? : {terminado}")
        print("-" * 50)
        if terminado:
            print("¡Oración completada exitosamente!")
            break

    print("Verificación de transiciones completada con éxito.")
