import os
import sys
import time
import pygame

from configuracion import (
    estado_inicio,
    estado_seleccion_tematica,
    estado_juego,
    estado_victoria,
    ruta_carpeta_audio,
)
from datos import catalogo_escenarios, catalogo_audios_interfaz
from ia_models.agente_qlearning import AgenteQLearning
from ia_models.baseline_heuristico import BaselineHeuristico
from ia_models.entorno_simulacion import (
    ACCION_ESPERAR,
    ACCION_PISTA_NIVEL_1,
    ACCION_PISTA_NIVEL_2,
    ACCION_PISTA_NIVEL_3,
    SEGUNDOS_UMBRAL_INACTIVIDAD,
)


# clase encargada de la carga y reproduccion de audio con pygame mixer
class gestor_audio:
    def __init__(self):
        # inicializacion de mixer con buffer optimizado para baja latencia
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
                pygame.mixer.init()
        except Exception as error_mixer:
            print(f"aviso al inicializar mixer: {error_mixer}", file=sys.stderr)

        # almacenamiento en memoria para reutilizacion rapida
        self.cache_sonidos = {}

    def reproducir(self, subcarpeta, nombre_archivo):
        # reproduccion no bloqueante de archivo de audio
        if not nombre_archivo:
            return

        clave_cache = (subcarpeta, nombre_archivo)
        if clave_cache in self.cache_sonidos:
            try:
                pygame.mixer.stop()
                self.cache_sonidos[clave_cache].play()
                return
            except Exception:
                pass

        ruta_archivo = os.path.join(ruta_carpeta_audio, subcarpeta, nombre_archivo)
        if os.path.exists(ruta_archivo):
            try:
                pygame.mixer.stop()
                sonido = pygame.mixer.Sound(ruta_archivo)
                self.cache_sonidos[clave_cache] = sonido
                sonido.play()
            except Exception as error_reproduccion:
                print(f"error al reproducir {ruta_archivo}: {error_reproduccion}", file=sys.stderr)
        else:
            print(f"archivo de audio no encontrado: {ruta_archivo}", file=sys.stderr)

    def detener(self):
        # detiene cualquier sonido en curso
        try:
            pygame.mixer.stop()
        except Exception:
            pass


# clase encargada de las reglas de juego turnos y validacion sintactica bimodal
class logica_juego:
    def __init__(self, audio_motor):
        self.audio_motor = audio_motor
        self.estado_actual = estado_inicio
        self.numero_jugadores = 1
        self.jugador_actual = 1
        self.clave_tematica_actual = "granja"
        self.indice_escenario_actual = 0

        # control secuencial de seleccion bimodal
        self.numero_jugadores_seleccionado = False
        self.boton_comenzar_habilitado = False
        self.clave_tematica_seleccionada = None
        self.boton_jugar_habilitado = False

        # casillas del turno activo
        self.indice_casilla_activa = 0
        self.casillas_colocadas = [None, None, None]
        self.opciones_disponibles = []

        # control de tiempo para pistas adaptativas
        self.tiempo_ultima_interaccion = time.time()
        self.segundos_espera_ayuda = 10.0
        self.mostrar_pista_adaptativa = False
        self.datos_pista_actual = None

        # integracion de modelos de razonamiento (Hito 2)
        self.modo_agente = "qlearning"
        self.agente_qlearning = AgenteQLearning()
        ruta_modelo_q = os.path.join(os.path.dirname(__file__), "ia_models", "modelo_q_entrenado.json")
        self.agente_qlearning.cargar_modelo(ruta_modelo_q)
        self.agente_baseline = BaselineHeuristico()

        # variables de estado adaptativo
        self.intentos_fallidos_casilla = 0
        self.nivel_pista_actual = 0
        self.tarjeta_distractora_bloqueada = None

    def obtener_escenario_activo(self):
        # obtencion del escenario especifico en juego segun el indice
        conjunto = catalogo_escenarios[self.clave_tematica_actual]
        lista = conjunto["lista_escenarios"]
        return lista[self.indice_escenario_actual % len(lista)]

    def cambiar_estado(self, nuevo_estado):
        # transicion entre pantallas con reproduccion auditiva contextual
        self.estado_actual = nuevo_estado
        self.tiempo_ultima_interaccion = time.time()
        self.mostrar_pista_adaptativa = False

        if nuevo_estado == estado_inicio:
            self.numero_jugadores_seleccionado = False
            self.boton_comenzar_habilitado = False
            self.audio_motor.reproducir("ui", catalogo_audios_interfaz["bienvenida"])

        elif nuevo_estado == estado_seleccion_tematica:
            self.clave_tematica_seleccionada = None
            self.boton_jugar_habilitado = False

        elif nuevo_estado == estado_juego:
            self.reiniciar_tablero_turno()
            archivo_turno = catalogo_audios_interfaz["turnos"].get(self.jugador_actual, "turno_j1.mp3")
            self.audio_motor.reproducir("ui", archivo_turno)

        elif nuevo_estado == estado_victoria:
            escenario = self.obtener_escenario_activo()
            self.audio_motor.reproducir("oraciones", escenario["audio_oracion"])

    def seleccionar_jugadores(self, cantidad):
        # seleccion de participantes habilitando el avance tras el audio
        self.numero_jugadores = cantidad
        self.numero_jugadores_seleccionado = True
        self.boton_comenzar_habilitado = True
        archivo_jugador = catalogo_audios_interfaz["jugadores"].get(cantidad, "ui_jugador_1.mp3")
        self.audio_motor.reproducir("ui", archivo_jugador)

    def seleccionar_tematica(self, clave):
        # seleccion de conjunto tematico con reproduccion de audio descriptivo
        self.clave_tematica_seleccionada = clave
        self.boton_jugar_habilitado = True
        conjunto = catalogo_escenarios[clave]
        self.audio_motor.reproducir("ui", conjunto["audio_descripcion"])

    def confirmar_tematica_y_comenzar(self):
        # avance formal a la partida una vez seleccionada la tematica
        if self.boton_jugar_habilitado and self.clave_tematica_seleccionada:
            self.clave_tematica_actual = self.clave_tematica_seleccionada
            self.jugador_actual = 1
            self.indice_escenario_actual = 0
            self.cambiar_estado(estado_juego)

    def repetir_audio_turno(self):
        # repite la instruccion auditiva del turno
        archivo_turno = catalogo_audios_interfaz["turnos"].get(self.jugador_actual, "turno_j1.mp3")
        self.audio_motor.reproducir("ui", archivo_turno)

    def reiniciar_tablero_turno(self):
        # reinicio de posiciones y tarjetas disponibles para el turno
        escenario = self.obtener_escenario_activo()
        self.indice_casilla_activa = 0
        self.casillas_colocadas = [None, None, None]
        self.opciones_disponibles = [dict(opcion) for opcion in escenario["opciones"]]
        for opcion in self.opciones_disponibles:
            opcion["usada"] = False
        self.tiempo_ultima_interaccion = time.time()
        self.mostrar_pista_adaptativa = False
        self.datos_pista_actual = None
        self.intentos_fallidos_casilla = 0
        self.nivel_pista_actual = 0
        self.tarjeta_distractora_bloqueada = None

    def alternar_modo_agente(self):
        # cambia entre qlearning y baseline para sustentacion comparativa
        self.modo_agente = "baseline" if self.modo_agente == "qlearning" else "qlearning"
        return self.modo_agente

    def obtener_estado_discreto(self):
        # construccion de la tupla (casilla, fallos, nivel_pista, inactividad)
        casilla_activa = min(self.indice_casilla_activa, 2)
        fallos = min(self.intentos_fallidos_casilla, 3)
        pista = self.nivel_pista_actual
        inactividad = 1 if (time.time() - self.tiempo_ultima_interaccion) >= SEGUNDOS_UMBRAL_INACTIVIDAD else 0
        return (casilla_activa, fallos, pista, inactividad)

    def consultar_accion_tutor(self, es_solicitud_manual=False):
        # consulta la politica optima del modelo activo
        estado = self.obtener_estado_discreto()
        if self.modo_agente == "baseline":
            accion = self.agente_baseline.seleccionar_accion(estado)
        else:
            accion = self.agente_qlearning.seleccionar_accion(estado, en_entrenamiento=False)

        # si es solicitud manual con boton ?, garantizar respuesta minima Nivel 1
        if es_solicitud_manual and accion == ACCION_ESPERAR:
            accion = ACCION_PISTA_NIVEL_1
        return accion

    def aplicar_intervencion_pedagogica(self, accion):
        # ejecuta la accion pedagógica determinada por el agente inteligente
        if accion == ACCION_ESPERAR:
            return False

        self.nivel_pista_actual = accion
        self.mostrar_pista_adaptativa = True
        self.tiempo_ultima_interaccion = time.time()

        escenario = self.obtener_escenario_activo()
        casilla = min(self.indice_casilla_activa, 2)
        pista = escenario["pistas"][casilla]
        self.datos_pista_actual = pista

        if accion == ACCION_PISTA_NIVEL_3:
            self.identificar_tarjeta_distractora()
        else:
            self.tarjeta_distractora_bloqueada = None

        self.audio_motor.reproducir("pistas", pista["audio_pregunta"])
        return True

    def identificar_tarjeta_distractora(self):
        # localiza un distractor para atenuar carga cognitiva en Nivel 3
        escenario = self.obtener_escenario_activo()
        casilla = min(self.indice_casilla_activa, 2)
        id_objetivo = escenario["objetivo"][casilla]["id"]
        for indice, opcion in enumerate(self.opciones_disponibles):
            if not opcion.get("usada", False) and opcion["id"] != id_objetivo:
                self.tarjeta_distractora_bloqueada = indice
                return

    def solicitar_ayuda_manual(self):
        # atencion inmediata y adaptativa a la pulsacion del boton ?
        accion = self.consultar_accion_tutor(es_solicitud_manual=True)
        self.aplicar_intervencion_pedagogica(accion)

    def activar_pista(self, indice_casilla):
        # presentacion tradicional mantenida por compatibilidad
        self.solicitar_ayuda_manual()

    def cerrar_pista(self):
        # ocultar la ventana modal de pista
        self.mostrar_pista_adaptativa = False
        self.tiempo_ultima_interaccion = time.time()

    def reproducir_audio_opcion(self, indice_opcion):
        # lectura lexico-fonetica inmediata del pictograma pulsado o arrastrado
        if indice_opcion < len(self.opciones_disponibles):
            opcion = self.opciones_disponibles[indice_opcion]
            if not opcion.get("usada", False):
                self.tiempo_ultima_interaccion = time.time()
                self.audio_motor.reproducir("pictogramas", opcion["audio_locucion"])

    def colocar_opcion_en_casilla(self, indice_opcion, indice_casilla=None):
        # validacion y colocacion de una tarjeta arrastrada en la casilla correspondiente
        if indice_opcion >= len(self.opciones_disponibles):
            return False

        opcion_elegida = self.opciones_disponibles[indice_opcion]
        if opcion_elegida.get("usada", False):
            return False

        self.tiempo_ultima_interaccion = time.time()
        casilla_destino = self.indice_casilla_activa if indice_casilla is None else indice_casilla

        # si se intenta colocar en una casilla distinta a la activa actual
        if casilla_destino != self.indice_casilla_activa:
            self.intentos_fallidos_casilla += 1
            accion = self.consultar_accion_tutor(es_solicitud_manual=False)
            self.aplicar_intervencion_pedagogica(accion)
            return False

        escenario = self.obtener_escenario_activo()
        objetivo_esperado = escenario["objetivo"][self.indice_casilla_activa]

        if opcion_elegida["id"] == objetivo_esperado["id"]:
            # acierto confirmado en la casilla correspondiente
            self.casillas_colocadas[self.indice_casilla_activa] = opcion_elegida
            opcion_elegida["usada"] = True
            self.indice_casilla_activa += 1
            self.intentos_fallidos_casilla = 0
            self.nivel_pista_actual = 0
            self.tarjeta_distractora_bloqueada = None

            if self.indice_casilla_activa >= 3:
                self.cambiar_estado(estado_victoria)
            return True
        else:
            # error detectado consulta y ejecucion del agente adaptativo
            self.intentos_fallidos_casilla += 1
            accion = self.consultar_accion_tutor(es_solicitud_manual=False)
            self.aplicar_intervencion_pedagogica(accion)
            return False

    def seleccionar_opcion(self, indice_opcion):
        # seleccion directa con audio y validacion secuencial
        self.reproducir_audio_opcion(indice_opcion)
        return self.colocar_opcion_en_casilla(indice_opcion)

    def siguiente_turno(self):
        # avance al siguiente jugador y cambio al siguiente escenario del conjunto
        self.jugador_actual += 1
        conjunto = catalogo_escenarios[self.clave_tematica_actual]
        self.indice_escenario_actual = (self.indice_escenario_actual + 1) % len(conjunto["lista_escenarios"])
        self.cambiar_estado(estado_juego)

    def siguiente_reto(self):
        # avanzar al siguiente reto manteniendo el turno o para un solo jugador
        conjunto = catalogo_escenarios[self.clave_tematica_actual]
        self.indice_escenario_actual = (self.indice_escenario_actual + 1) % len(conjunto["lista_escenarios"])
        self.cambiar_estado(estado_juego)

    def felicitar_final_partida(self):
        # reproduce refuerzo sonoro positivo de fin de juego
        self.audio_motor.reproducir("ui", catalogo_audios_interfaz["felicitacion_final"])

    def finalizar_juego(self):
        # reproduce felicitacion final y regresa al inicio de partida
        self.felicitar_final_partida()
        self.jugador_actual = 1
        self.indice_escenario_actual = 0
        self.estado_actual = estado_inicio
        self.numero_jugadores_seleccionado = False
        self.boton_comenzar_habilitado = False

    def reiniciar_juego(self):
        # restablecer partida al inicio
        self.jugador_actual = 1
        self.indice_escenario_actual = 0
        self.cambiar_estado(estado_inicio)

    def actualizar_inactividad(self):
        # revision de tiempo sin respuesta asistida por el tutor inteligente
        if self.estado_actual == estado_juego and not self.mostrar_pista_adaptativa:
            segundos_transcurridos = time.time() - self.tiempo_ultima_interaccion
            if segundos_transcurridos >= SEGUNDOS_UMBRAL_INACTIVIDAD:
                accion = self.consultar_accion_tutor(es_solicitud_manual=False)
                self.aplicar_intervencion_pedagogica(accion)

    def obtener_tiempo_inactividad(self):
        # calculo de segundos transcurridos desde el ultimo clic
        return time.time() - self.tiempo_ultima_interaccion
