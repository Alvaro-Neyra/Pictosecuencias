import os

# dimensiones de la ventana principal adaptada a alta definicion
ancho_pantalla = 1280
alto_pantalla = 720
cuadros_por_segundo = 60

# paleta de colores accesibles para descanso visual y alto contraste wcag aaa
color_fondo = (248, 250, 252)
color_superficie = (255, 255, 255)
color_tarjeta_hover = (240, 246, 255)
color_texto = (15, 23, 42)
color_texto_secundario = (71, 85, 105)
color_borde = (15, 23, 42)
color_borde_claro = (203, 213, 225)

# colores de estados deshabilitados para interaccion bimodal
color_deshabilitado = (226, 232, 240)
color_deshabilitado_texto = (148, 163, 184)

# colores tematicos y de interaccion con contrastes calibrados
color_primario = (37, 99, 235)
color_primario_resaltado = (29, 78, 216)
color_exito = (22, 101, 52)
color_exito_fondo = (220, 252, 231)
color_ayuda = (234, 88, 12)
color_ayuda_pulso = (249, 115, 22)
color_casilla_vacia = (241, 245, 249)
color_capa_oscura = (15, 23, 42, 180)

# familia tipografica de alta definicion para pantallas
fuente_sistema = "segoe ui, arial, sans-serif"

# estados de la aplicacion
estado_inicio = "estado_inicio"
estado_seleccion_tematica = "estado_seleccion_tematica"
estado_juego = "estado_juego"
estado_victoria = "estado_victoria"

# rutas de carpetas de recursos
ruta_directorio_base = os.path.dirname(os.path.abspath(__file__))
ruta_carpeta_pictogramas = os.path.join(ruta_directorio_base, "assets", "pictogramas")
ruta_carpeta_audio = os.path.join(ruta_directorio_base, "assets", "audio")
