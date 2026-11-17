"""
Evaluación empírica y comparativa entre el Baseline Heurístico y el Agente Q-Learning.
Ejecuta baterías de simulación sobre perfiles clínicos sintéticos de Kallpa,
calcula métricas de desempeño pedagógico y genera reportes tabulares y gráficos.
"""

from typing import Dict, List, Any, Tuple
import os
import sys
import csv

# Asegurar que la raíz del proyecto esté en el path de búsqueda de módulos
RAIZ_PROYECTO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if RAIZ_PROYECTO not in sys.path:
    sys.path.insert(0, RAIZ_PROYECTO)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ia_models.entorno_simulacion import (
    EntornoPictoSecuencias,
    TipoEstado,
    ACCION_ESPERAR,
    ACCION_PISTA_NIVEL_1,
    ACCION_PISTA_NIVEL_2,
    ACCION_PISTA_NIVEL_3,
    PERFIL_AUTONOMO,
    PERFIL_SEMANTICO_MODERADO,
    PERFIL_DISTRACCION_BLOQUEO,
    TOTAL_CASILLAS,
)
from ia_models.baseline_heuristico import BaselineHeuristico
from ia_models.agente_qlearning import AgenteQLearning

DIR_RESULTADOS: str = os.path.join(os.path.dirname(__file__), "resultados")
RUTA_MODELO_Q: str = os.path.join(os.path.dirname(__file__), "modelo_q_entrenado.json")
MAX_PASOS_TEST: int = 25


class EvaluadorComparativo:
    """Ejecutor de pruebas empíricas comparativas y generador de métricas pedagógicas."""

    def __init__(self, episodios_test_por_perfil: int = 1000) -> None:
        self.episodios_por_perfil: int = episodios_test_por_perfil
        self.perfiles: List[str] = [
            PERFIL_AUTONOMO,
            PERFIL_SEMANTICO_MODERADO,
            PERFIL_DISTRACCION_BLOQUEO,
        ]
        os.makedirs(DIR_RESULTADOS, exist_ok=True)

    def evaluar_agente_en_partida(
        self, agente: Any, entorno: EntornoPictoSecuencias
    ) -> Dict[str, Any]:
        """Evalúa un agente en una partida individual y registra métricas detalladas."""
        estado = entorno.reiniciar()
        terminado = False
        pasos = 0
        total_intervenciones = 0
        repeticiones_pista = 0
        fallos_post_primera_pista = 0
        hubo_intervencion_en_casilla = False
        ultima_pista_en_casilla = 0
        casilla_anterior = 0

        while not terminado and pasos < MAX_PASOS_TEST:
            pasos += 1
            accion = agente.seleccionar_accion(estado)

            # Monitoreo de cambio de casilla para reiniciar contadores locales
            if estado[0] != casilla_anterior:
                casilla_anterior = estado[0]
                hubo_intervencion_en_casilla = False
                ultima_pista_en_casilla = 0

            if accion > ACCION_ESPERAR:
                total_intervenciones += 1
                if hubo_intervencion_en_casilla and accion == ultima_pista_en_casilla:
                    repeticiones_pista += 1
                hubo_intervencion_en_casilla = True
                ultima_pista_en_casilla = accion

            estado_siguiente, _, terminado, info = entorno.ejecutar_paso(accion)

            # Si ya se emitió pista y el usuario continúa fallando
            if hubo_intervencion_en_casilla and not info["acierto"]:
                fallos_post_primera_pista += 1

            estado = estado_siguiente

        exito = (estado[0] >= TOTAL_CASILLAS)
        return {
            "exito": 1.0 if exito else 0.0,
            "pasos": pasos,
            "intervenciones": total_intervenciones,
            "repeticiones_pista": repeticiones_pista,
            "fallos_post_pista": fallos_post_primera_pista,
        }

    def evaluar_modelo(self, agente: Any) -> Dict[str, Dict[str, float]]:
        """Evalúa un agente sobre todos los perfiles de usuario y calcula promedios."""
        entorno = EntornoPictoSecuencias()
        metricas_por_perfil: Dict[str, Dict[str, float]] = {}

        for perfil in self.perfiles:
            entorno.cambiar_perfil(perfil)
            resultados_perfil: List[Dict[str, Any]] = []

            for _ in range(self.episodios_por_perfil):
                res = self.evaluar_agente_en_partida(agente, entorno)
                resultados_perfil.append(res)

            tasa_exito = np.mean([r["exito"] for r in resultados_perfil]) * 100.0
            prom_fallos_post_pista = float(np.mean([r["fallos_post_pista"] for r in resultados_perfil]))
            prom_intervenciones = float(np.mean([r["intervenciones"] for r in resultados_perfil]))
            total_interv = sum(r["intervenciones"] for r in resultados_perfil)
            total_repet = sum(r["repeticiones_pista"] for r in resultados_perfil)
            tasa_repeticion = (total_repet / total_interv * 100.0) if total_interv > 0 else 0.0

            metricas_por_perfil[perfil] = {
                "tasa_exito": tasa_exito,
                "fallos_post_pista": prom_fallos_post_pista,
                "intervenciones_promedio": prom_intervenciones,
                "tasa_repeticion": tasa_repeticion,
            }

        # Cálculo de promedio ponderado global
        metricas_por_perfil["GLOBAL"] = {
            "tasa_exito": float(np.mean([m["tasa_exito"] for m in metricas_por_perfil.values()])),
            "fallos_post_pista": float(np.mean([m["fallos_post_pista"] for m in metricas_por_perfil.values()])),
            "intervenciones_promedio": float(np.mean([m["intervenciones_promedio"] for m in metricas_por_perfil.values()])),
            "tasa_repeticion": float(np.mean([m["tasa_repeticion"] for m in metricas_por_perfil.values()])),
        }

        return metricas_por_perfil

    def guardar_metricas_csv(
        self,
        metricas_baseline: Dict[str, Dict[str, float]],
        metricas_qlearning: Dict[str, Dict[str, float]],
    ) -> str:
        """Exporta las métricas comparativas a un archivo CSV."""
        ruta_csv = os.path.join(DIR_RESULTADOS, "metricas_comparativas.csv")
        with open(ruta_csv, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([
                "Modelo",
                "Perfil_Usuario",
                "Tasa_Exito_Porcentaje",
                "Promedio_Fallos_Post_Pista",
                "Promedio_Intervenciones_Partida",
                "Tasa_Repeticion_Inefectiva_Porcentaje",
            ])
            for perfil, m in metricas_baseline.items():
                escritor.writerow([
                    "Baseline Heurístico",
                    perfil,
                    f"{m['tasa_exito']:.2f}",
                    f"{m['fallos_post_pista']:.2f}",
                    f"{m['intervenciones_promedio']:.2f}",
                    f"{m['tasa_repeticion']:.2f}",
                ])
            for perfil, m in metricas_qlearning.items():
                escritor.writerow([
                    "Q-Learning Adaptativo",
                    perfil,
                    f"{m['tasa_exito']:.2f}",
                    f"{m['fallos_post_pista']:.2f}",
                    f"{m['intervenciones_promedio']:.2f}",
                    f"{m['tasa_repeticion']:.2f}",
                ])
        return ruta_csv

    def generar_grafica_convergencia(self, historial_recompensas: List[float]) -> str:
        """Genera y guarda el gráfico de convergencia con media móvil de recompensas."""
        ruta_grafica = os.path.join(DIR_RESULTADOS, "curva_convergencia_qlearning.png")
        plt.figure(figsize=(10, 5), dpi=300)

        ventana = 100
        medias_moviles = np.convolve(historial_recompensas, np.ones(ventana) / ventana, mode="valid")

        plt.plot(historial_recompensas, color="#B0BEC5", alpha=0.35, label="Recompensa por Episodio")
        plt.plot(
            range(ventana - 1, len(historial_recompensas)),
            medias_moviles,
            color="#1E88E5",
            linewidth=2.2,
            label=f"Media Móvil ({ventana} episodios)",
        )

        plt.title("Curva de Aprendizaje y Convergencia: Agente Q-Learning", fontsize=14, pad=12)
        plt.xlabel("Episodios de Entrenamiento", fontsize=11)
        plt.ylabel("Recompensa Acumulada", fontsize=11)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend(loc="lower right", fontsize=10)
        plt.tight_layout()
        plt.savefig(ruta_grafica)
        plt.close()
        return ruta_grafica

    def generar_grafica_comparativa(
        self,
        metricas_baseline: Dict[str, Dict[str, float]],
        metricas_qlearning: Dict[str, Dict[str, float]],
    ) -> str:
        """Genera un gráfico comparativo de barras enfrentando los dos modelos."""
        ruta_grafica = os.path.join(DIR_RESULTADOS, "comparativa_baseline_vs_qlearning.png")
        fig, axes = plt.subplots(1, 3, figsize=(15, 5), dpi=300)

        categorias = ["Autónomo", "Semántico", "Distracción", "Global"]
        claves_perfil = [PERFIL_AUTONOMO, PERFIL_SEMANTICO_MODERADO, PERFIL_DISTRACCION_BLOQUEO, "GLOBAL"]

        x = np.arange(len(categorias))
        ancho = 0.35

        # 1. Tasa de Éxito (%)
        exito_base = [metricas_baseline[c]["tasa_exito"] for c in claves_perfil]
        exito_ql = [metricas_qlearning[c]["tasa_exito"] for c in claves_perfil]

        axes[0].bar(x - ancho / 2, exito_base, ancho, label="Baseline Heurístico", color="#78909C")
        axes[0].bar(x + ancho / 2, exito_ql, ancho, label="Q-Learning", color="#2E7D32")
        axes[0].axhline(80.0, color="#D32F2F", linestyle=":", linewidth=1.5, label="Meta Hito 2 (80%)")
        axes[0].set_title("Tasa de Éxito de Resolución (%)", fontsize=11, fontweight="bold")
        axes[0].set_xticks(x)
        axes[0].set_xticklabels(categorias, fontsize=9)
        axes[0].set_ylim(0, 105)
        axes[0].grid(True, linestyle="--", alpha=0.5, axis="y")
        axes[0].legend(loc="lower left", fontsize=8)

        # 2. Promedio de Fallos Post-Pista
        fallos_base = [metricas_baseline[c]["fallos_post_pista"] for c in claves_perfil]
        fallos_ql = [metricas_qlearning[c]["fallos_post_pista"] for c in claves_perfil]

        axes[1].bar(x - ancho / 2, fallos_base, ancho, label="Baseline Heurístico", color="#78909C")
        axes[1].bar(x + ancho / 2, fallos_ql, ancho, label="Q-Learning", color="#1565C0")
        axes[1].set_title("Fallos Posteriores a Pista", fontsize=11, fontweight="bold")
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(categorias, fontsize=9)
        axes[1].grid(True, linestyle="--", alpha=0.5, axis="y")
        axes[1].legend(loc="upper right", fontsize=8)

        # 3. Intervenciones por Partida (Autonomía)
        interv_base = [metricas_baseline[c]["intervenciones_promedio"] for c in claves_perfil]
        interv_ql = [metricas_qlearning[c]["intervenciones_promedio"] for c in claves_perfil]

        axes[2].bar(x - ancho / 2, interv_base, ancho, label="Baseline Heurístico", color="#78909C")
        axes[2].bar(x + ancho / 2, interv_ql, ancho, label="Q-Learning", color="#E65100")
        axes[2].set_title("Pistas Emitidas por Partida", fontsize=11, fontweight="bold")
        axes[2].set_xticks(x)
        axes[2].set_xticklabels(categorias, fontsize=9)
        axes[2].grid(True, linestyle="--", alpha=0.5, axis="y")
        axes[2].legend(loc="upper right", fontsize=8)

        plt.suptitle("Comparativa Empírica: Baseline Heurístico vs. Agente Q-Learning (Hito 2)", fontsize=13)
        plt.tight_layout()
        plt.savefig(ruta_grafica)
        plt.close()
        return ruta_grafica


def ejecutar_flujo_completo_hito2() -> None:
    """Orquesta el entrenamiento de 5,000 episodios y la evaluación de 6,000 partidas."""
    print("=" * 80)
    print("INICIO DEL HITO 2: ENTRENAMIENTO Y EVALUACIÓN COMPARATIVA")
    print("=" * 80)

    # 1. Entrenamiento de Q-Learning
    print("\n[1/3] Entrenando AgenteQLearning (5,000 episodios con balance de perfiles)...")
    entorno = EntornoPictoSecuencias()
    agente_ql = AgenteQLearning()
    historial = agente_ql.entrenar(entorno, total_episodios=5000)
    agente_ql.guardar_modelo(RUTA_MODELO_Q)
    print(f"      Entrenamiento finalizado. Modelo exportado a: {RUTA_MODELO_Q}")
    print(f"      Estados únicos explorados y valorizados: {len(agente_ql.tabla_q)}")

    # 2. Inicialización de modelos para evaluación
    print("\n[2/3] Ejecutando evaluación comparativa (1,000 partidas por perfil)...")
    agente_base = BaselineHeuristico()
    evaluador = EvaluadorComparativo(episodios_test_por_perfil=1000)

    print("      Evaluando Baseline Heurístico...")
    metricas_base = evaluador.evaluar_modelo(agente_base)

    print("      Evaluando Agente Q-Learning óptimo...")
    metricas_ql = evaluador.evaluar_modelo(agente_ql)

    # 3. Exportación y Generación de Gráficos
    print("\n[3/3] Generando reportes y visualizaciones...")
    ruta_csv = evaluador.guardar_metricas_csv(metricas_base, metricas_ql)
    ruta_convergencia = evaluador.generar_grafica_convergencia(historial)
    ruta_comparativa = evaluador.generar_grafica_comparativa(metricas_base, metricas_ql)

    print(f"      CSV guardado en: {ruta_csv}")
    print(f"      Gráfica de convergencia en: {ruta_convergencia}")
    print(f"      Gráfica comparativa en: {ruta_comparativa}")

    # Impresión de Tabla Resumen en Consola
    print("\n" + "=" * 80)
    print("TABLA COMPARATIVA DE DESEMPEÑO EMPÍRICO (HITO 2)")
    print("=" * 80)
    encabezado = f"{'Perfil Usuario':<22} | {'Modelo':<21} | {'Éxito (%)':<10} | {'Fallos Post':<12} | {'Interv.':<8} | {'Repetición':<10}"
    print(encabezado)
    print("-" * 95)

    nombres_perfil = {
        PERFIL_AUTONOMO: "Autónomo (Rápido)",
        PERFIL_SEMANTICO_MODERADO: "Semántico Moderado",
        PERFIL_DISTRACCION_BLOQUEO: "Distracción/Bloqueo",
        "GLOBAL": "PROMEDIO GLOBAL",
    }

    for clave in [PERFIL_AUTONOMO, PERFIL_SEMANTICO_MODERADO, PERFIL_DISTRACCION_BLOQUEO, "GLOBAL"]:
        mb = metricas_base[clave]
        mq = metricas_ql[clave]
        nombre_p = nombres_perfil[clave]

        linea_base = f"{nombre_p:<22} | {'Baseline Heurístico':<21} | {mb['tasa_exito']:>8.2f}% | {mb['fallos_post_pista']:>12.2f} | {mb['intervenciones_promedio']:>8.2f} | {mb['tasa_repeticion']:>9.2f}%"
        linea_ql = f"{'':<22} | {'Q-Learning Adaptativo':<21} | {mq['tasa_exito']:>8.2f}% | {mq['fallos_post_pista']:>12.2f} | {mq['intervenciones_promedio']:>8.2f} | {mq['tasa_repeticion']:>9.2f}%"

        print(linea_base)
        print(linea_ql)
        print("-" * 95)

    print("=" * 80)


if __name__ == "__main__":
    ejecutar_flujo_completo_hito2()
