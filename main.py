import sys
import pygame

# habilitacion de alta resolucion y nitidez para pantallas modernas en windows
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

from configuracion import (
    ancho_pantalla,
    alto_pantalla,
    cuadros_por_segundo,
    color_fondo,
    color_texto,
    color_primario,
    color_exito,
    color_ayuda,
    estado_inicio,
    estado_seleccion_tematica,
    estado_juego,
    estado_victoria,
)
from datos import catalogo_escenarios
from logica import gestor_audio, logica_juego
from graficos import (
    boton_interactivo,
    dibujar_pantalla_inicio,
    dibujar_pantalla_tematicas,
    dibujar_pantalla_juego,
    dibujar_pista_adaptativa,
    dibujar_pantalla_victoria,
)


# clase coordinadora principal del juego
class juego_principal:
    def __init__(self):
        # inicializacion de subsistemas de pygame
        pygame.init()
        pygame.font.init()

        # creacion de la ventana y reloj de cuadros
        self.pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
        pygame.display.set_caption("PictoSecuencias - Kallpa Play AI")
        self.reloj = pygame.time.Clock()
        self.esta_ejecutandose = True

        # inicializacion de la logica y el gestor de audio
        self.audio_motor = gestor_audio()
        self.logica = logica_juego(self.audio_motor)

        # variables de control para arrastrar y soltar pictogramas
        self.indice_tarjeta_arrastrada = None
        self.posicion_arrastre = (0, 0)
        self.posicion_inicio_arrastre = (0, 0)
        self.distancia_arrastre = 0

        # creacion de botones y regiones interactivas
        self.inicializar_botones_e_interfaces()

        # transicion inicial al estado de inicio con reproduccion de bienvenida
        self.logica.cambiar_estado(estado_inicio)

    def inicializar_botones_e_interfaces(self):
        # 1. pantalla de inicio
        self.botones_jugadores = []
        ancho_b, alto_b = 90, 80
        separacion = 24
        inicio_x = (ancho_pantalla - (4 * ancho_b + 3 * separacion)) // 2
        for i in range(1, 5):
            x = inicio_x + (i - 1) * (ancho_b + separacion)
            boton = boton_interactivo((x, 320, ancho_b, alto_b), str(i), color_fondo=(255, 255, 255),
                                      color_texto=color_texto, tamano_letra=32)
            self.botones_jugadores.append(boton)

        self.boton_comenzar = boton_interactivo(((ancho_pantalla - 300) // 2, 460, 300, 75),
                                                "¡COMENZAR!", color_fondo=color_exito, tamano_letra=28)

        # 2. pantalla de seleccion de tematica
        self.rectangulos_tematicas = [
            pygame.Rect(100, 220, 330, 360),
            pygame.Rect(475, 220, 330, 360),
            pygame.Rect(850, 220, 330, 360)
        ]
        self.claves_tematicas = ["granja", "rutinas", "aseo"]

        # 3. tablero de juego sin emojis
        self.boton_altavoz = boton_interactivo((ancho_pantalla - 145, 26, 115, 48), "AUDIO",
                                               color_fondo=(255, 255, 255), color_texto=color_primario,
                                               tamano_letra=20, radio_borde=14)

        self.boton_ayuda = boton_interactivo((ancho_pantalla - 180, 480, 140, 65), "AYUDA",
                                             color_fondo=color_ayuda, tamano_letra=24)

        # casillas receptoras centrales
        ancho_casilla, alto_casilla = 180, 180
        espacio_casillas = 40
        total_ancho_casillas = 3 * ancho_casilla + 2 * espacio_casillas
        inicio_casillas_x = (ancho_pantalla - total_ancho_casillas) // 2
        y_casillas = 175
        self.rectangulos_casillas = [
            pygame.Rect(inicio_casillas_x + i * (ancho_casilla + espacio_casillas), y_casillas, ancho_casilla, alto_casilla)
            for i in range(3)
        ]

        # bandeja inferior de opciones
        ancho_opcion, alto_opcion = 170, 170
        espacio_opciones = 40
        total_ancho_opciones = 3 * ancho_opcion + 2 * espacio_opciones
        inicio_opciones_x = (ancho_pantalla - total_ancho_opciones) // 2
        y_opciones = 440
        self.rectangulos_opciones = [
            pygame.Rect(inicio_opciones_x + i * (ancho_opcion + espacio_opciones), y_opciones, ancho_opcion, alto_opcion)
            for i in range(3)
        ]

        # boton para cerrar pista modal
        self.boton_cerrar_pista = boton_interactivo(((ancho_pantalla - 220) // 2, 530, 220, 55),
                                                    "ENTENDIDO", color_fondo=color_primario, tamano_letra=20)

        # 4. pantalla de victoria
        self.boton_siguiente_turno = boton_interactivo(((ancho_pantalla - 320) // 2, 520, 320, 70),
                                                       "SIGUIENTE RETO", color_fondo=color_primario, tamano_letra=24)
        self.boton_terminar_juego = boton_interactivo(((ancho_pantalla - 320) // 2, 520, 320, 70),
                                                      "FINALIZAR JUEGO", color_fondo=color_exito, tamano_letra=24)

    def procesar_eventos(self):
        # procesamiento de la cola de eventos de pygame
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.esta_ejecutandose = False
                return

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.indice_tarjeta_arrastrada = None
                    if self.logica.mostrar_pista_adaptativa:
                        self.logica.cerrar_pista()
                    else:
                        self.logica.reiniciar_juego()

            if evento.type == pygame.MOUSEMOTION:
                if self.indice_tarjeta_arrastrada is not None:
                    self.posicion_arrastre = evento.pos
                    dx = evento.pos[0] - self.posicion_inicio_arrastre[0]
                    dy = evento.pos[1] - self.posicion_inicio_arrastre[1]
                    distancia = (dx * dx + dy * dy) ** 0.5
                    if distancia > self.distancia_arrastre:
                        self.distancia_arrastre = distancia
                self.actualizar_resaltados(evento.pos)

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # en el tablero revisamos si se pulsa una tarjeta de la bandeja para escucharla e iniciar arrastre
                if self.logica.estado_actual == estado_juego and not self.logica.mostrar_pista_adaptativa:
                    tarjeta_pulsada = False
                    if not self.boton_altavoz.es_clic(evento.pos) and not self.boton_ayuda.es_clic(evento.pos):
                        for indice, rectangulo in enumerate(self.rectangulos_opciones):
                            if indice < len(self.logica.opciones_disponibles):
                                opcion = self.logica.opciones_disponibles[indice]
                                if not opcion.get("usada", False) and rectangulo.collidepoint(evento.pos):
                                    self.indice_tarjeta_arrastrada = indice
                                    self.posicion_arrastre = evento.pos
                                    self.posicion_inicio_arrastre = evento.pos
                                    self.distancia_arrastre = 0
                                    # lectura lexico-fonetica al pulsar el pictograma
                                    self.logica.reproducir_audio_opcion(indice)
                                    tarjeta_pulsada = True
                                    break
                    if tarjeta_pulsada:
                        continue

                self.manejar_clic(evento.pos)

            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if self.logica.estado_actual == estado_juego and self.indice_tarjeta_arrastrada is not None:
                    # si el usuario desplazo la tarjeta con intencion de colocarla
                    if self.distancia_arrastre > 12:
                        casilla_destino = None
                        ancho_t, alto_t = 170, 170
                        rect_arrastrado = pygame.Rect(
                            evento.pos[0] - ancho_t // 2,
                            evento.pos[1] - alto_t // 2,
                            ancho_t,
                            alto_t
                        )
                        for ind_casilla, rect_casilla in enumerate(self.rectangulos_casillas):
                            if rect_casilla.collidepoint(evento.pos) or rect_casilla.colliderect(rect_arrastrado):
                                casilla_destino = ind_casilla
                                break

                        if casilla_destino is not None:
                            self.logica.colocar_opcion_en_casilla(self.indice_tarjeta_arrastrada, casilla_destino)

                    self.indice_tarjeta_arrastrada = None

    def actualizar_resaltados(self, posicion_raton):
        # actualizacion visual del estado hover en botones y cambio dinamico de cursor
        hay_interaccion = False

        if self.indice_tarjeta_arrastrada is not None:
            hay_interaccion = True

        elif self.logica.estado_actual == estado_inicio:
            self.boton_comenzar.actualizar_resaltado(posicion_raton)
            if self.boton_comenzar.esta_resaltado:
                hay_interaccion = True
            for boton in self.botones_jugadores:
                boton.actualizar_resaltado(posicion_raton)
                if boton.esta_resaltado:
                    hay_interaccion = True

        elif self.logica.estado_actual == estado_seleccion_tematica:
            for rectangulo in self.rectangulos_tematicas:
                if rectangulo.collidepoint(posicion_raton):
                    hay_interaccion = True
                    break

        elif self.logica.estado_actual == estado_juego:
            if self.logica.mostrar_pista_adaptativa:
                self.boton_cerrar_pista.actualizar_resaltado(posicion_raton)
                if self.boton_cerrar_pista.esta_resaltado:
                    hay_interaccion = True
            else:
                self.boton_altavoz.actualizar_resaltado(posicion_raton)
                self.boton_ayuda.actualizar_resaltado(posicion_raton)
                if self.boton_altavoz.esta_resaltado or self.boton_ayuda.esta_resaltado:
                    hay_interaccion = True

                for indice, rectangulo in enumerate(self.rectangulos_opciones):
                    if indice < len(self.logica.opciones_disponibles):
                        opcion = self.logica.opciones_disponibles[indice]
                        if not opcion.get("usada", False) and rectangulo.collidepoint(posicion_raton):
                            hay_interaccion = True
                            break

        elif self.logica.estado_actual == estado_victoria:
            self.boton_siguiente_turno.actualizar_resaltado(posicion_raton)
            if self.boton_siguiente_turno.esta_resaltado:
                hay_interaccion = True
            if not (self.logica.numero_jugadores > 1 and self.logica.jugador_actual < self.logica.numero_jugadores):
                self.boton_terminar_juego.actualizar_resaltado(posicion_raton)
                if self.boton_terminar_juego.esta_resaltado:
                    hay_interaccion = True

        # ajuste de forma del puntero a mano si apunta a un elemento interactivo
        try:
            if hay_interaccion:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        except Exception:
            pass

    def manejar_clic(self, posicion_raton):
        # atencion a clics con el boton principal
        if self.logica.mostrar_pista_adaptativa:
            if self.boton_cerrar_pista.es_clic(posicion_raton):
                self.logica.cerrar_pista()
            return

        if self.logica.estado_actual == estado_inicio:
            for indice, boton in enumerate(self.botones_jugadores):
                if boton.es_clic(posicion_raton):
                    self.logica.seleccionar_jugadores(indice + 1)
                    return

            if self.boton_comenzar.es_clic(posicion_raton):
                self.logica.cambiar_estado(estado_seleccion_tematica)
                return

        elif self.logica.estado_actual == estado_seleccion_tematica:
            for indice, rectangulo in enumerate(self.rectangulos_tematicas):
                if rectangulo.collidepoint(posicion_raton):
                    clave = self.claves_tematicas[indice]
                    if self.logica.clave_tematica_seleccionada == clave:
                        self.logica.confirmar_tematica_y_comenzar()
                    else:
                        self.logica.seleccionar_tematica(clave)
                    return

        elif self.logica.estado_actual == estado_juego:
            # boton de altavoz para repetir instruccion del turno
            if self.boton_altavoz.es_clic(posicion_raton):
                self.logica.repetir_audio_turno()
                return

            # boton de ayuda manual
            if self.boton_ayuda.es_clic(posicion_raton):
                self.logica.activar_pista(self.logica.indice_casilla_activa)
                return

            # seleccion en bandeja inferior
            for indice, rectangulo in enumerate(self.rectangulos_opciones):
                if rectangulo.collidepoint(posicion_raton):
                    self.logica.seleccionar_opcion(indice)
                    return

        elif self.logica.estado_actual == estado_victoria:
            if self.logica.numero_jugadores > 1 and self.logica.jugador_actual < self.logica.numero_jugadores:
                if self.boton_siguiente_turno.es_clic(posicion_raton):
                    self.logica.siguiente_turno()
            else:
                if self.boton_siguiente_turno.es_clic(posicion_raton):
                    self.logica.siguiente_reto()
                elif self.boton_terminar_juego.es_clic(posicion_raton):
                    self.logica.finalizar_juego()

    def actualizar(self):
        # actualizacion de logica interna y revision de inactividad
        self.logica.actualizar_inactividad()

    def renderizar(self):
        # llenado con fondo neutro de alto descanso
        self.pantalla.fill(color_fondo)

        # renderizado segun estado activo
        if self.logica.estado_actual == estado_inicio:
            dibujar_pantalla_inicio(self.pantalla, self.logica, self.botones_jugadores, self.boton_comenzar)
        elif self.logica.estado_actual == estado_seleccion_tematica:
            dibujar_pantalla_tematicas(self.pantalla, self.logica, self.rectangulos_tematicas, self.claves_tematicas)
        elif self.logica.estado_actual == estado_juego:
            dibujar_pantalla_juego(
                self.pantalla,
                self.logica,
                self.rectangulos_casillas,
                self.rectangulos_opciones,
                self.boton_altavoz,
                self.boton_ayuda,
                self.indice_tarjeta_arrastrada,
                self.posicion_arrastre
            )
        elif self.logica.estado_actual == estado_victoria:
            dibujar_pantalla_victoria(
                self.pantalla,
                self.logica,
                self.boton_siguiente_turno,
                self.boton_terminar_juego
            )

        # superposicion de la pista modal si esta activa
        if self.logica.mostrar_pista_adaptativa:
            dibujar_pista_adaptativa(self.pantalla, self.logica, self.boton_cerrar_pista)

        pygame.display.flip()

    def ejecutar(self):
        # ciclo principal a 60 cuadros por segundo
        while self.esta_ejecutandose:
            self.procesar_eventos()
            self.actualizar()
            self.renderizar()
            self.reloj.tick(cuadros_por_segundo)

        pygame.quit()
        sys.exit()


# punto de entrada principal
if __name__ == "__main__":
    aplicacion = juego_principal()
    aplicacion.ejecutar()
