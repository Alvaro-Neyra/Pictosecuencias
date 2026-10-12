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

    def activar_pista(self, indice_casilla):
        # presentacion de pista adaptativa multimodal con reproduccion de pregunta
        escenario = self.obtener_escenario_activo()
        pista = escenario["pistas"][indice_casilla]
        self.datos_pista_actual = pista
        self.mostrar_pista_adaptativa = True
        self.tiempo_ultima_interaccion = time.time()
        self.audio_motor.reproducir("pistas", pista["audio_pregunta"])

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
            self.activar_pista(self.indice_casilla_activa)
            return False

        escenario = self.obtener_escenario_activo()
        objetivo_esperado = escenario["objetivo"][self.indice_casilla_activa]

        if opcion_elegida["id"] == objetivo_esperado["id"]:
            # acierto confirmado en la casilla correspondiente
            self.casillas_colocadas[self.indice_casilla_activa] = opcion_elegida
            opcion_elegida["usada"] = True
            self.indice_casilla_activa += 1

            if self.indice_casilla_activa >= 3:
                self.cambiar_estado(estado_victoria)
            return True
        else:
            # error detectado activacion de pista adaptativa contextual
            self.activar_pista(self.indice_casilla_activa)
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
        # revision de tiempo sin respuesta durante el juego activo
        if self.estado_actual == estado_juego and not self.mostrar_pista_adaptativa:
            segundos_transcurridos = time.time() - self.tiempo_ultima_interaccion
            if segundos_transcurridos > (self.segundos_espera_ayuda * 2.5):
                self.activar_pista(self.indice_casilla_activa)

    def obtener_tiempo_inactividad(self):
        # calculo de segundos transcurridos desde el ultimo clic
        return time.time() - self.tiempo_ultima_interaccion
