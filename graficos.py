import os
import math
import pygame

from configuracion import (
    ancho_pantalla,
    alto_pantalla,
    color_fondo,
    color_superficie,
    color_tarjeta_hover,
    color_texto,
    color_texto_secundario,
    color_borde,
    color_borde_claro,
    color_deshabilitado,
    color_deshabilitado_texto,
    color_primario,
    color_primario_resaltado,
    color_exito,
    color_exito_fondo,
    color_ayuda,
    color_ayuda_pulso,
    color_casilla_vacia,
    color_capa_oscura,
    fuente_sistema,
    ruta_carpeta_pictogramas,
)
from datos import catalogo_escenarios

# diccionario para almacenar en memoria las superficies de pictogramas ya renderizadas
cache_pictogramas = {}
cache_portadas = {}


# funcion para localizar el archivo del pictograma de forma tolerante a mayusculas
def buscar_ruta_pictograma(nombre_archivo):
    if not nombre_archivo:
        return None

    # alias para tolerancia a variaciones de escritura
    nombre_limpio = nombre_archivo.strip()
    if "ruinas" in nombre_limpio.lower():
        nombre_limpio = "Rutinas diarias.jpg"

    # comprobacion directa de existencia
    ruta_directa = os.path.join(ruta_carpeta_pictogramas, nombre_limpio)
    if os.path.exists(ruta_directa):
        return ruta_directa

    # busqueda tolerante si difieren mayusculas o tildes
    if os.path.exists(ruta_carpeta_pictogramas):
        nombre_comparar = nombre_limpio.lower()
        for archivo in os.listdir(ruta_carpeta_pictogramas):
            if archivo.strip().lower() == nombre_comparar:
                return os.path.join(ruta_carpeta_pictogramas, archivo)

    return None


# carga de portada tematica rectangular con escalado suave
def obtener_superficie_portada(nombre_archivo, dimensiones=(240, 135)):
    clave_cache = (nombre_archivo, dimensiones)
    if clave_cache in cache_portadas:
        return cache_portadas[clave_cache]

    ancho, alto = dimensiones
    ruta_imagen = buscar_ruta_pictograma(nombre_archivo)
    superficie_tarjeta = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    rectangulo_base = pygame.Rect(0, 0, ancho, alto)

    # fondo blanco base con bordes redondeados
    pygame.draw.rect(superficie_tarjeta, color_superficie, rectangulo_base, border_radius=12)

    if ruta_imagen and os.path.exists(ruta_imagen):
        try:
            if pygame.display.get_surface() is not None:
                imagen_cruda = pygame.image.load(ruta_imagen).convert_alpha()
            else:
                imagen_cruda = pygame.image.load(ruta_imagen)

            ancho_crudo, alto_crudo = imagen_cruda.get_size()
            factor_escala = min((ancho - 12) / ancho_crudo, (alto - 12) / alto_crudo)
            nuevo_ancho = max(1, int(ancho_crudo * factor_escala))
            nuevo_alto = max(1, int(alto_crudo * factor_escala))

            imagen_escalada = pygame.transform.smoothscale(imagen_cruda, (nuevo_ancho, nuevo_alto))
            rectangulo_centrado = imagen_escalada.get_rect(center=(ancho // 2, alto // 2))
            superficie_tarjeta.blit(imagen_escalada, rectangulo_centrado)
        except Exception as error_portada:
            print(f"error al cargar portada {nombre_archivo}: {error_portada}")

    # contorno sutil de la imagen
    pygame.draw.rect(superficie_tarjeta, color_borde_claro, rectangulo_base, width=2, border_radius=12)
    cache_portadas[clave_cache] = superficie_tarjeta
    return superficie_tarjeta


# carga de imagen y creacion de tarjeta de pictograma con fondo blanco para transparencias
def obtener_superficie_pictograma(nombre_archivo, texto_etiqueta, dimensiones=(160, 160)):
    clave_cache = (nombre_archivo, texto_etiqueta, dimensiones)
    if clave_cache in cache_pictogramas:
        return cache_pictogramas[clave_cache]

    ancho, alto = dimensiones
    ruta_imagen = buscar_ruta_pictograma(nombre_archivo) if nombre_archivo else None
    imagen_procesada = None

    if ruta_imagen and os.path.exists(ruta_imagen):
        try:
            # carga de la imagen con soporte de canal alfa en pygame
            if pygame.display.get_surface() is not None:
                imagen_cruda = pygame.image.load(ruta_imagen).convert_alpha()
            else:
                imagen_cruda = pygame.image.load(ruta_imagen)
            ancho_crudo, alto_crudo = imagen_cruda.get_size()

            # creacion de superficie con fondo blanco para eliminar cualquier transparencia
            superficie_fondo_blanco = pygame.Surface((ancho_crudo, alto_crudo))
            superficie_fondo_blanco.fill((255, 255, 255))
            superficie_fondo_blanco.blit(imagen_cruda, (0, 0))

            # calculo de escalado proporcional respetando el recuadro superior
            alto_maximo_interior = int(alto * 0.65)
            ancho_maximo_interior = ancho - 20
            factor_escala = min(ancho_maximo_interior / ancho_crudo, alto_maximo_interior / alto_crudo)
            nuevo_ancho = max(1, int(ancho_crudo * factor_escala))
            nuevo_alto = max(1, int(alto_crudo * factor_escala))

            imagen_procesada = pygame.transform.smoothscale(superficie_fondo_blanco, (nuevo_ancho, nuevo_alto))
        except Exception as error_carga:
            print(f"aviso al procesar pictograma {nombre_archivo}: {error_carga}")
            imagen_procesada = None

    # construccion de la tarjeta con soporte de transparencia para bordes redondeados
    superficie_tarjeta = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    rectangulo_tarjeta = pygame.Rect(0, 0, ancho, alto)

    # 1. dibujo del fondo blanco de la tarjeta
    pygame.draw.rect(superficie_tarjeta, color_superficie, rectangulo_tarjeta, border_radius=14)

    if imagen_procesada:
        # centrado de la imagen en la parte superior
        centro_y = int(alto * 0.40)
        rectangulo_imagen = imagen_procesada.get_rect(center=(ancho // 2, centro_y))
        superficie_tarjeta.blit(imagen_procesada, rectangulo_imagen)
    else:
        # placeholder ilustrativo en caso de no existir archivo
        margen = 12
        alto_recuadro = int(alto * 0.64)
        rectangulo_interior = pygame.Rect(margen, margen, ancho - 2 * margen, alto_recuadro)
        pygame.draw.rect(superficie_tarjeta, (241, 245, 249), rectangulo_interior, border_radius=8)
        pygame.draw.rect(superficie_tarjeta, (203, 213, 225), rectangulo_interior, width=2, border_radius=8)

        # elemento geometrico representativo
        centro_x = ancho // 2
        centro_y_icono = margen + alto_recuadro // 2
        pygame.draw.circle(superficie_tarjeta, (148, 163, 184), (centro_x, centro_y_icono - 10), 16)
        puntos = [
            (centro_x - 32, centro_y_icono + 22),
            (centro_x, centro_y_icono - 6),
            (centro_x + 32, centro_y_icono + 22)
        ]
        pygame.draw.polygon(superficie_tarjeta, (100, 116, 139), puntos)

    # 2. etiqueta inferior en mayusculas negrita y centrada
    tamano_fuente = max(12, int(ancho * 0.095))
    fuente_texto = pygame.font.SysFont(fuente_sistema, tamano_fuente, bold=True)
    superficie_texto = fuente_texto.render(texto_etiqueta.upper(), True, color_texto)
    while superficie_texto.get_width() > (ancho - 16) and tamano_fuente > 10:
        tamano_fuente -= 1
        fuente_texto = pygame.font.SysFont(fuente_sistema, tamano_fuente, bold=True)
        superficie_texto = fuente_texto.render(texto_etiqueta.upper(), True, color_texto)
    rectangulo_texto = superficie_texto.get_rect(center=(ancho // 2, int(alto * 0.79)))
    superficie_tarjeta.blit(superficie_texto, rectangulo_texto)

    # 3. borde exterior grueso para contraste
    pygame.draw.rect(superficie_tarjeta, color_borde, rectangulo_tarjeta, width=3, border_radius=14)

    cache_pictogramas[clave_cache] = superficie_tarjeta
    return superficie_tarjeta


# funcion auxiliar para dibujar flecha vectorial limpia sin emojis
def dibujar_flecha_secuencia(superficie, centro_x, centro_y, longitud=32, color=color_borde_claro):
    inicio_x = centro_x - longitud // 2
    fin_x = centro_x + longitud // 2
    # linea principal
    pygame.draw.line(superficie, color, (inicio_x, centro_y), (fin_x, centro_y), 4)
    # cabeza triangular
    puntos_punta = [
        (fin_x, centro_y),
        (fin_x - 10, centro_y - 7),
        (fin_x - 10, centro_y + 7)
    ]
    pygame.draw.polygon(superficie, color, puntos_punta)


# funcion auxiliar para dibujar marca de verificacion vectorial sin emojis
def dibujar_marca_verificacion(superficie, centro_x, centro_y, tamano=26, color=color_exito):
    puntos_marca = [
        (centro_x - tamano // 2, centro_y),
        (centro_x - tamano // 6, centro_y + tamano // 3),
        (centro_x + tamano // 2, centro_y - tamano // 2)
    ]
    pygame.draw.lines(superficie, color, False, puntos_marca, 5)


# clase para botones accesibles con soporte de estados activo hover y deshabilitado
class boton_interactivo:
    def __init__(self, rectangulo, texto, color_fondo=color_primario, color_texto=(255, 255, 255),
                 color_borde=color_borde, ancho_borde=3, tamano_letra=24, radio_borde=14,
                 color_fondo_hover=None, color_borde_hover=None, esta_habilitado=True):
        self.rectangulo = pygame.Rect(rectangulo)
        self.texto = texto
        self.color_fondo = color_fondo
        self.color_texto = color_texto
        self.color_borde = color_borde
        self.ancho_borde = ancho_borde
        self.tamano_letra = tamano_letra
        self.radio_borde = radio_borde
        self.color_fondo_hover = color_fondo_hover
        self.color_borde_hover = color_borde_hover
        self.esta_habilitado = esta_habilitado
        self.esta_resaltado = False

    def dibujar(self, superficie):
        # aplicacion de estilos segun si esta habilitado y hover
        if not self.esta_habilitado:
            fondo_activo = color_deshabilitado
            borde_activo = color_borde_claro
            color_txt = color_deshabilitado_texto
            ancho_activo = 2
        elif self.esta_resaltado:
            if self.color_fondo_hover:
                fondo_activo = self.color_fondo_hover
            else:
                fondo_activo = tuple(min(255, canal + 24) for canal in self.color_fondo)

            if self.color_borde_hover:
                borde_activo = self.color_borde_hover
            else:
                borde_activo = color_borde

            color_txt = self.color_texto
            ancho_activo = max(self.ancho_borde, 4)
        else:
            fondo_activo = self.color_fondo
            borde_activo = self.color_borde
            color_txt = self.color_texto
            ancho_activo = self.ancho_borde

        pygame.draw.rect(superficie, fondo_activo, self.rectangulo, border_radius=self.radio_borde)
        if ancho_activo > 0:
            pygame.draw.rect(superficie, borde_activo, self.rectangulo, width=ancho_activo, border_radius=self.radio_borde)

        if self.texto:
            fuente = pygame.font.SysFont(fuente_sistema, self.tamano_letra, bold=True)
            superficie_texto = fuente.render(self.texto, True, color_txt)
            rectangulo_texto = superficie_texto.get_rect(center=self.rectangulo.center)
            superficie.blit(superficie_texto, rectangulo_texto)

    def actualizar_resaltado(self, posicion_raton):
        self.esta_resaltado = self.esta_habilitado and self.rectangulo.collidepoint(posicion_raton)

    def es_clic(self, posicion_raton):
        return self.esta_habilitado and self.rectangulo.collidepoint(posicion_raton)


# dibujo estandarizado del encabezado
def dibujar_encabezado(superficie, titulo, subtitulo=None):
    fuente_titulo = pygame.font.SysFont(fuente_sistema, 32, bold=True)
    superficie_titulo = fuente_titulo.render(titulo, True, color_texto)
    superficie.blit(superficie_titulo, (60, 32))

    if subtitulo:
        fuente_subtitulo = pygame.font.SysFont(fuente_sistema, 18)
        superficie_subtitulo = fuente_subtitulo.render(subtitulo, True, color_texto_secundario)
        superficie.blit(superficie_subtitulo, (60, 72))


# renderizado de la pantalla de bienvenida y configuracion de participantes con seleccion en 2 pasos
def dibujar_pantalla_inicio(superficie, logica, lista_botones_jugadores, boton_comenzar):
    dibujar_encabezado(superficie, "PictoSecuencias", "Kallpa Play AI - Juego de Mesa Inclusivo")

    # tarjeta contenedor central con proporciones adaptadas
    rectangulo_panel = pygame.Rect((ancho_pantalla - 780) // 2, 130, 780, 490)
    pygame.draw.rect(superficie, color_superficie, rectangulo_panel, border_radius=18)
    pygame.draw.rect(superficie, color_borde, rectangulo_panel, width=3, border_radius=18)

    # rotulo de pregunta con tipografia mejorada
    fuente_pregunta = pygame.font.SysFont(fuente_sistema, 26, bold=True)
    superficie_pregunta = fuente_pregunta.render("¿Cuántos participantes van a jugar?", True, color_texto)
    superficie.blit(superficie_pregunta, superficie_pregunta.get_rect(center=(ancho_pantalla // 2, 210)))

    fuente_descripcion = pygame.font.SysFont(fuente_sistema, 18)
    superficie_desc = fuente_descripcion.render("Selecciona el número para escuchar la confirmación y habilitar el juego.", True, color_texto_secundario)
    superficie.blit(superficie_desc, superficie_desc.get_rect(center=(ancho_pantalla // 2, 250)))

    # dibujo de botones selectores de cantidad de jugadores
    for indice, boton in enumerate(lista_botones_jugadores):
        cantidad = indice + 1
        if logica.numero_jugadores_seleccionado and cantidad == logica.numero_jugadores:
            boton.color_fondo = color_primario
            boton.color_texto = (255, 255, 255)
            boton.color_borde = color_borde
            boton.ancho_borde = 4
        else:
            boton.color_fondo = color_tarjeta_hover if boton.esta_resaltado else (255, 255, 255)
            boton.color_texto = color_texto
            boton.color_borde = color_primario if boton.esta_resaltado else color_borde_claro
            boton.ancho_borde = 3
        boton.dibujar(superficie)

    # estado de habilitacion secuencial del boton de comenzar
    boton_comenzar.esta_habilitado = logica.boton_comenzar_habilitado
    boton_comenzar.dibujar(superficie)


# renderizado de la seleccion de tematica con seleccion en 2 pasos e imagen de portada
def dibujar_pantalla_tematicas(superficie, logica, lista_rectangulos_tematicas, lista_claves_tematicas):
    dibujar_encabezado(superficie, "Elige un Conjunto de Pictogramas", "Haz clic en una temática para escuchar su descripción y habilitar la partida")

    posicion_raton = pygame.mouse.get_pos()
    for indice, clave in enumerate(lista_claves_tematicas):
        conjunto = catalogo_escenarios[clave]
        rectangulo = lista_rectangulos_tematicas[indice]

        es_seleccionada = (clave == logica.clave_tematica_seleccionada)
        esta_sobre = rectangulo.collidepoint(posicion_raton)

        if es_seleccionada:
            color_caja = color_tarjeta_hover
            borde_caja = color_primario
            ancho_caja = 5
        elif esta_sobre:
            color_caja = color_tarjeta_hover
            borde_caja = color_primario
            ancho_caja = 3
        else:
            color_caja = (255, 255, 255)
            borde_caja = color_borde
            ancho_caja = 3

        pygame.draw.rect(superficie, color_caja, rectangulo, border_radius=18)
        pygame.draw.rect(superficie, borde_caja, rectangulo, width=ancho_caja, border_radius=18)

        # imagen de portada del conjunto
        superficie_portada = obtener_superficie_portada(conjunto["imagen_portada"], dimensiones=(250, 140))
        rectangulo_portada = superficie_portada.get_rect(center=(rectangulo.centerx, rectangulo.top + 88))
        superficie.blit(superficie_portada, rectangulo_portada)

        # titulo de la tematica
        fuente_titulo = pygame.font.SysFont(fuente_sistema, 22, bold=True)
        superficie_titulo = fuente_titulo.render(conjunto["titulo"], True, color_texto)
        superficie.blit(superficie_titulo, superficie_titulo.get_rect(center=(rectangulo.centerx, rectangulo.top + 180)))

        # texto descriptivo
        fuente_desc = pygame.font.SysFont(fuente_sistema, 15)
        palabras = conjunto["descripcion"].split(" ")
        linea_1 = " ".join(palabras[:4])
        linea_2 = " ".join(palabras[4:])
        superficie_linea_1 = fuente_desc.render(linea_1, True, color_texto_secundario)
        superficie_linea_2 = fuente_desc.render(linea_2, True, color_texto_secundario)
        superficie.blit(superficie_linea_1, superficie_linea_1.get_rect(center=(rectangulo.centerx, rectangulo.top + 214)))
        superficie.blit(superficie_linea_2, superficie_linea_2.get_rect(center=(rectangulo.centerx, rectangulo.top + 236)))

        # indicador de cantidad de escenarios disponibles sin emojis
        cantidad_retos = len(conjunto.get("lista_escenarios", []))
        rect_badge = pygame.Rect(rectangulo.centerx - 90, rectangulo.top + 258, 180, 26)
        pygame.draw.rect(superficie, color_exito_fondo, rect_badge, border_radius=8)
        pygame.draw.rect(superficie, color_exito, rect_badge, width=1, border_radius=8)
        fuente_badge = pygame.font.SysFont(fuente_sistema, 13, bold=True)
        superficie_badge = fuente_badge.render(f"{cantidad_retos} RETOS DISPONIBLES", True, color_exito)
        superficie.blit(superficie_badge, superficie_badge.get_rect(center=rect_badge.center))

        # boton integrado de jugar aqui con retroalimentacion bimodal secuencial
        rectangulo_boton = pygame.Rect(rectangulo.centerx - 95, rectangulo.bottom - 58, 190, 44)
        if es_seleccionada:
            color_btn = color_primario_resaltado if esta_sobre else color_primario
            color_txt = (255, 255, 255)
            color_borde_btn = color_borde
            ancho_borde_btn = 3
            texto_btn = "JUGAR AQUÍ"
        elif esta_sobre:
            color_btn = (255, 255, 255)
            color_txt = color_primario
            color_borde_btn = color_primario
            ancho_borde_btn = 2
            texto_btn = "SELECCIONAR"
        else:
            color_btn = color_deshabilitado
            color_txt = color_deshabilitado_texto
            color_borde_btn = color_borde_claro
            ancho_borde_btn = 2
            texto_btn = "JUGAR AQUÍ"

        pygame.draw.rect(superficie, color_btn, rectangulo_boton, border_radius=12)
        pygame.draw.rect(superficie, color_borde_btn, rectangulo_boton, width=ancho_borde_btn, border_radius=12)
        fuente_boton = pygame.font.SysFont(fuente_sistema, 17, bold=True)
        texto_surf = fuente_boton.render(texto_btn, True, color_txt)
        superficie.blit(texto_surf, texto_surf.get_rect(center=rectangulo_boton.center))


# renderizado del tablero principal de juego sin emojis
def dibujar_pantalla_juego(superficie, logica, lista_rectangulos_casillas, lista_rectangulos_opciones, boton_altavoz, boton_ayuda, indice_arrastrado=None, posicion_arrastre=None):
    escenario = logica.obtener_escenario_activo()
    conjunto = catalogo_escenarios[logica.clave_tematica_actual]

    # cabecera de turno y guia
    fuente_turno = pygame.font.SysFont(fuente_sistema, 28, bold=True)
    num_reto = logica.indice_escenario_actual + 1
    total_retos = len(conjunto["lista_escenarios"])
    texto_turno = f"Jugador {logica.jugador_actual} de {logica.numero_jugadores}: Tu Turno | Reto {num_reto} de {total_retos}"
    superficie_turno = fuente_turno.render(texto_turno, True, color_primario)
    superficie.blit(superficie_turno, (60, 30))

    fuente_instruccion = pygame.font.SysFont(fuente_sistema, 18)
    texto_instruccion = "Arrastra la tarjeta correcta a cada casilla o haz clic para escuchar su pronunciación"
    superficie_instruccion = fuente_instruccion.render(texto_instruccion, True, color_texto_secundario)
    superficie.blit(superficie_instruccion, (60, 68))

    # boton superior de altavoz para repetir locucion
    boton_altavoz.dibujar(superficie)

    # calculo de rectangulo proyectado si hay arrastre en curso
    rect_arrastrado = None
    if indice_arrastrado is not None and posicion_arrastre is not None:
        rect_arrastrado = pygame.Rect(posicion_arrastre[0] - 85, posicion_arrastre[1] - 85, 170, 170)

    # 1. casillas receptoras superiores
    for indice, rectangulo in enumerate(lista_rectangulos_casillas):
        etiqueta_casilla = escenario["etiquetas_casillas"][indice]
        es_activa = (indice == logica.indice_casilla_activa)
        tarjeta_colocada = logica.casillas_colocadas[indice]

        if tarjeta_colocada:
            # pictograma ya ordenado exitosamente
            superficie_tarjeta = obtener_superficie_pictograma(
                tarjeta_colocada["archivo"],
                tarjeta_colocada["etiqueta"],
                (rectangulo.width, rectangulo.height)
            )
            superficie.blit(superficie_tarjeta, rectangulo)
            pygame.draw.rect(superficie, color_exito, rectangulo, width=4, border_radius=14)
        else:
            # verificacion si la tarjeta arrastrada sobrevuela la casilla activa
            esta_sobrevolando = False
            if es_activa and rect_arrastrado is not None:
                esta_sobrevolando = rectangulo.collidepoint(posicion_arrastre) or rectangulo.colliderect(rect_arrastrado)

            color_fondo_ranura = (240, 253, 244) if esta_sobrevolando else color_casilla_vacia
            pygame.draw.rect(superficie, color_fondo_ranura, rectangulo, border_radius=14)

            if esta_sobrevolando:
                color_borde_ranura = color_exito
                ancho_borde_ranura = 5
            elif es_activa:
                color_borde_ranura = color_primario
                ancho_borde_ranura = 4
            else:
                color_borde_ranura = color_borde_claro
                ancho_borde_ranura = 2

            pygame.draw.rect(superficie, color_borde_ranura, rectangulo, width=ancho_borde_ranura, border_radius=14)

            fuente_etiqueta = pygame.font.SysFont(fuente_sistema, 13, bold=True)
            superficie_etiqueta = fuente_etiqueta.render(etiqueta_casilla, True, color_texto if es_activa else color_texto_secundario)
            superficie.blit(superficie_etiqueta, superficie_etiqueta.get_rect(center=(rectangulo.centerx, rectangulo.bottom - 24)))

            # indicador numerico vectorial claro sin emojis
            if es_activa:
                fuente_numero = pygame.font.SysFont(fuente_sistema, 42, bold=True)
                color_num = color_exito if esta_sobrevolando else color_primario
                superficie_numero = fuente_numero.render(str(indice + 1), True, color_num)
                superficie.blit(superficie_numero, superficie_numero.get_rect(center=rectangulo.center))
            else:
                fuente_espera = pygame.font.SysFont(fuente_sistema, 32, bold=True)
                superficie_espera = fuente_espera.render(str(indice + 1), True, color_borde_claro)
                superficie.blit(superficie_espera, superficie_espera.get_rect(center=rectangulo.center))

    # flechas indicadoras de la secuencia sintactica vectoriales sin emojis
    y_flechas = lista_rectangulos_casillas[0].centery
    dibujar_flecha_secuencia(superficie, lista_rectangulos_casillas[0].right + 20, y_flechas)
    dibujar_flecha_secuencia(superficie, lista_rectangulos_casillas[1].right + 20, y_flechas)

    # linea divisoria horizontal
    pygame.draw.line(superficie, (226, 232, 240), (80, 395), (ancho_pantalla - 80, 395), 2)
    fuente_bandeja = pygame.font.SysFont(fuente_sistema, 16, bold=True)
    superficie_bandeja = fuente_bandeja.render("TARJETAS DISPONIBLES (Arrastra a la casilla o haz clic para escuchar):", True, color_texto_secundario)
    superficie.blit(superficie_bandeja, (80, 410))

    # 2. bandeja inferior de tarjetas disponibles
    posicion_raton = pygame.mouse.get_pos()
    for indice, rectangulo in enumerate(lista_rectangulos_opciones):
        if indice < len(logica.opciones_disponibles):
            opcion = logica.opciones_disponibles[indice]
            if opcion.get("usada", False):
                # tarjeta ya utilizada en el tablero con marca vectorial
                pygame.draw.rect(superficie, (241, 245, 249), rectangulo, border_radius=14)
                pygame.draw.rect(superficie, (203, 213, 225), rectangulo, width=2, border_radius=14)
                dibujar_marca_verificacion(superficie, rectangulo.centerx, rectangulo.centery)
            elif indice == indice_arrastrado:
                # espacio base tenue mientras se arrastra la tarjeta
                pygame.draw.rect(superficie, (241, 245, 249), rectangulo, border_radius=14)
                pygame.draw.rect(superficie, (203, 213, 225), rectangulo, width=2, border_radius=14)
            else:
                # tarjeta lista para ser seleccionada o arrastrada
                superficie_tarjeta = obtener_superficie_pictograma(
                    opcion["archivo"],
                    opcion["etiqueta"],
                    (rectangulo.width, rectangulo.height)
                )
                superficie.blit(superficie_tarjeta, rectangulo)

                # resalte al pasar el puntero
                if rectangulo.collidepoint(posicion_raton) and indice_arrastrado is None:
                    pygame.draw.rect(superficie, color_primario, rectangulo, width=4, border_radius=14)

    # 3. boton lateral de ayuda con pulso de inactividad a partir de 10 segundos
    tiempo_inactivo = logica.obtener_tiempo_inactividad()
    if tiempo_inactivo >= logica.segundos_espera_ayuda:
        factor_pulso = (math.sin(pygame.time.get_ticks() / 200.0) + 1.0) / 2.0
        r = int(color_ayuda[0] + (color_ayuda_pulso[0] - color_ayuda[0]) * factor_pulso)
        g = int(color_ayuda[1] + (color_ayuda_pulso[1] - color_ayuda[1]) * factor_pulso)
        b = int(color_ayuda[2] + (color_ayuda_pulso[2] - color_ayuda[2]) * factor_pulso)
        boton_ayuda.color_fondo = (r, g, b)
        boton_ayuda.ancho_borde = 4
    else:
        boton_ayuda.color_fondo = color_ayuda
        boton_ayuda.ancho_borde = 3

    boton_ayuda.dibujar(superficie)

    # 4. renderizado superpuesto de la tarjeta que esta siendo arrastrada
    if indice_arrastrado is not None and posicion_arrastre is not None and rect_arrastrado is not None:
        if indice_arrastrado < len(logica.opciones_disponibles):
            opcion = logica.opciones_disponibles[indice_arrastrado]
            superficie_tarjeta = obtener_superficie_pictograma(
                opcion["archivo"],
                opcion["etiqueta"],
                (rect_arrastrado.width, rect_arrastrado.height)
            )
            rect_tarjeta = superficie_tarjeta.get_rect(center=posicion_arrastre)

            # sombra suave proyectada debajo de la tarjeta
            sombra = pygame.Surface((rect_tarjeta.width, rect_tarjeta.height), pygame.SRCALPHA)
            pygame.draw.rect(sombra, (15, 23, 42, 60), (0, 0, rect_tarjeta.width, rect_tarjeta.height), border_radius=16)
            superficie.blit(sombra, (rect_tarjeta.x + 8, rect_tarjeta.y + 10))

            # dibujo de la tarjeta flotante y su contorno activo
            superficie.blit(superficie_tarjeta, rect_tarjeta)
            pygame.draw.rect(superficie, color_primario, rect_tarjeta, width=4, border_radius=14)


# renderizado de la ventana modal de pista adaptativa sin emojis
def dibujar_pista_adaptativa(superficie, logica, boton_cerrar_pista):
    # capa oscura de fondo con transparencia
    superficie_oscura = pygame.Surface((ancho_pantalla, alto_pantalla), pygame.SRCALPHA)
    superficie_oscura.fill(color_capa_oscura)
    superficie.blit(superficie_oscura, (0, 0))

    # ventana modal centrada
    ancho_modal, alto_modal = 680, 460
    rectangulo_modal = pygame.Rect((ancho_pantalla - ancho_modal) // 2, (alto_pantalla - alto_modal) // 2, ancho_modal, alto_modal)
    pygame.draw.rect(superficie, color_superficie, rectangulo_modal, border_radius=20)
    pygame.draw.rect(superficie, color_borde, rectangulo_modal, width=4, border_radius=20)

    # cabecera de la pista del tutor sin emojis
    fuente_cabecera = pygame.font.SysFont(fuente_sistema, 24, bold=True)
    superficie_cabecera = fuente_cabecera.render("PISTA", True, color_ayuda)
    superficie.blit(superficie_cabecera, superficie_cabecera.get_rect(center=(rectangulo_modal.centerx, rectangulo_modal.top + 45)))

    # pregunta y pictograma de ayuda
    if logica.datos_pista_actual:
        pregunta = logica.datos_pista_actual["pregunta"]
        fuente_pregunta = pygame.font.SysFont(fuente_sistema, 26, bold=True)
        superficie_pregunta = fuente_pregunta.render(pregunta, True, color_texto)
        superficie.blit(superficie_pregunta, superficie_pregunta.get_rect(center=(rectangulo_modal.centerx, rectangulo_modal.top + 105)))

        # renderizado del pictograma de ayuda con fondo blanco garantizado
        superficie_ayuda = obtener_superficie_pictograma(
            logica.datos_pista_actual["archivo_ayuda"],
            logica.datos_pista_actual["etiqueta_ayuda"],
            dimensiones=(200, 195)
        )
        rectangulo_ayuda = superficie_ayuda.get_rect(center=(rectangulo_modal.centerx, rectangulo_modal.top + 235))
        superficie.blit(superficie_ayuda, rectangulo_ayuda)

    # boton de entendido para cerrar el apoyo
    boton_cerrar_pista.rectangulo.center = (rectangulo_modal.centerx, rectangulo_modal.bottom - 45)
    boton_cerrar_pista.dibujar(superficie)


# renderizado de la pantalla de celebracion y rotacion de turnos
def dibujar_pantalla_victoria(superficie, logica, boton_siguiente_turno, boton_terminar_juego):
    escenario = logica.obtener_escenario_activo()

    dibujar_encabezado(superficie, "¡Objetivo Completado!", "Excelente trabajo colaborativo en Kallpa Play AI")

    # tarjeta contenedor de celebracion
    rectangulo_panel = pygame.Rect((ancho_pantalla - 840) // 2, 120, 840, 520)
    pygame.draw.rect(superficie, color_superficie, rectangulo_panel, border_radius=20)
    pygame.draw.rect(superficie, color_exito, rectangulo_panel, width=4, border_radius=20)

    # texto de felicitacion
    fuente_felicitacion = pygame.font.SysFont(fuente_sistema, 32, bold=True)
    superficie_felicitacion = fuente_felicitacion.render("¡MUY BIEN! ORACIÓN COMPLETADA", True, color_exito)
    superficie.blit(superficie_felicitacion, superficie_felicitacion.get_rect(center=(rectangulo_panel.centerx, rectangulo_panel.top + 55)))

    # oracion sintactica formada
    fuente_oracion = pygame.font.SysFont(fuente_sistema, 24, bold=True)
    superficie_oracion = fuente_oracion.render(f'"{escenario["texto_oracion"]}"', True, color_texto)
    superficie.blit(superficie_oracion, superficie_oracion.get_rect(center=(rectangulo_panel.centerx, rectangulo_panel.top + 105)))

    # hilera con los tres pictogramas completados
    ancho_tarjeta, alto_tarjeta = 160, 160
    espacio = 30
    ancho_total = 3 * ancho_tarjeta + 2 * espacio
    inicio_x = rectangulo_panel.centerx - ancho_total // 2
    posicion_y = rectangulo_panel.top + 160

    for indice, tarjeta in enumerate(escenario["objetivo"]):
        superficie_pictograma = obtener_superficie_pictograma(tarjeta["archivo"], tarjeta["etiqueta"], (ancho_tarjeta, alto_tarjeta))
        superficie.blit(superficie_pictograma, (inicio_x + indice * (ancho_tarjeta + espacio), posicion_y))

    # botones interactivos para continuar la progresion o finalizar
    if logica.numero_jugadores > 1 and logica.jugador_actual < logica.numero_jugadores:
        boton_siguiente_turno.texto = "SIGUIENTE TURNO"
        boton_siguiente_turno.rectangulo.center = (rectangulo_panel.centerx, rectangulo_panel.bottom - 60)
        boton_siguiente_turno.dibujar(superficie)
    else:
        # opcion de avanzar al siguiente reto o finalizar la partida
        boton_siguiente_turno.texto = "SIGUIENTE RETO"
        boton_siguiente_turno.rectangulo.center = (rectangulo_panel.centerx - 170, rectangulo_panel.bottom - 60)
        boton_terminar_juego.rectangulo.center = (rectangulo_panel.centerx + 170, rectangulo_panel.bottom - 60)
        boton_siguiente_turno.dibujar(superficie)
        boton_terminar_juego.dibujar(superficie)
