# PictoSecuencias - Kallpa Play AI

<img src="assets/upc.png" height="120" style="display: block;">

## Informacion Academica

- **Institucion:** Universidad Peruana de Ciencias Aplicadas (UPC)
- **Carrera:** Ciencias de la Computacion
- **Curso:** Inteligencia Artificial (1ASI0404)
- **NRC:** 9134
- **Periodo:** 2026-20
- **Docente:** Jairo Pinedo Taquia

---

## Integrantes del Proyecto

| Codigo | Apellidos y Nombres | Rol |
| :---: | :--- | :--- |
| U202412310 | Victor Piero Arapa Titi | Reasoning & Game Logic Engineer |
| U202413112 | Salvador Arturo Diaz Miñano | Reasoning & Game Logic Engineer |
| U20241e410 | Rai Jeferson Manrique Anaya | Accessibility & UI Developer |
| U202211741 | Alvaro Alberto Neyra Salazar | Pipeline Architect & QA |

---

## Descripcion del Proyecto

PictoSecuencias es un juego de mesa digital interactivo asistido por Inteligencia Artificial, diseñado para personas con discapacidad intelectual leve a moderada y dificultades en la comunicacion atendidas por la Asociacion Educativa Kallpa.

El juego implementa principios de Comunicacion Aumentativa y Alternativa (CAA) para que los participantes aprendan a estructurar oraciones y secuencias logicas cotidianas bajo el esquema canonico:

**Sujeto + Verbo + Complemento**

Un agente inteligente evalua en tiempo real las elecciones del jugador. Ante errores o periodos prolongados de inactividad, el tutor proporciona pistas adaptativas (preguntas orientadoras, apoyo visual con pictogramas y locucion de audio) sin emitir penalizaciones ni generar frustracion.

### Alineacion con los Objetivos de Desarrollo Sostenible (ODS)

- **ODS 4 (Educacion de Calidad):** Brinda un entorno de aprendizaje accesible y adaptado al ritmo individual de cada participante, promoviendo la asimilacion de vocabulario funcional y logica secuencial.
- **ODS 10 (Reduccion de las Desigualdades):** Reduce barreras comunicativas mediante una interfaz inclusiva que fortalece la autonomia, la expresion y la participacion social.

---

## Caracteristicas Principales

1. **Modalidad Multijugador por Turnos:** Permite partidas de 1 a 4 jugadores con rotacion colaborativa en una misma pantalla.
2. **Interaccion Tactil y Arrastre (Drag and Drop):** El usuario puede pulsar una tarjeta para escuchar su pronunciacion inmediata o arrastrarla directamente hacia la casilla destino.
3. **Tematicas Cotidianas:**
   - Animales de Granja
   - Rutinas Diarias
   - Aseo Personal
4. **Retroalimentacion Bimodal:** Cada pictograma, pista, pregunta y oracion completa cuenta con audio sincronizado de alta fidelidad.
5. **Accesibilidad Visual:** Diseno con contraste cromático adaptado, tipografia clara, bordes definidos y limite de 3 a 6 elementos interactivos simultaneos para evitar la sobrecarga cognitiva.

---

## Requisitos del Sistema

- **Sistema Operativo:** Windows 10/11, Linux o macOS.
- **Lenguaje:** Python 3.9 o superior (probado en Python 3.12).
- **Librerias:** Pygame y pyttsx3 (especificadas en `requirements.txt`).

---

## Instalacion y Ejecucion Paso a Paso

### Paso 1: Clonar o descargar el repositorio
Descarga el proyecto en tu computadora y abre una terminal en la carpeta principal del proyecto:
```bash
cd DEMO
```

### Paso 2: Crear el entorno virtual (recomendado)
Crea un entorno virtual aislado para instalar las dependencias:
```bash
python -m venv .venv
```

### Paso 3: Activar el entorno virtual
- **En Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **En Windows (CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **En Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```

### Paso 4: Instalar las dependencias
Instala los paquetes necesarios utilizando el archivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

*(Opcional: Si utilizas el gestor uv, puedes ejecutar directamente: `uv run python main.py`)*

### Paso 5: Ejecutar el juego
Inicia la aplicacion ejecutando el archivo principal:
```bash
python main.py
```

---

## Estructura del Codigo

- `main.py`: Punto de entrada del juego, gestion de la ventana, cola de eventos y bucle principal.
- `logica.py`: Reglas de juego, maquina de estados, gestor de audio (`pygame.mixer`) y agente de pistas adaptativas.
- `graficos.py`: Renderizado visual de pantallas, componentes interactivos y animacion de arrastre.
- `datos.py`: Base de datos de tematicas, retos sintacticos, catalogos de pictogramas y rutas de audios.
- `configuracion.py`: Parametros generales de pantalla, dimensiones y paleta de colores.
- `assets/`: Recursos graficos (pictogramas, portadas, logo UPC) y archivos de audio (locuciones, pistas y oraciones).
- `requirements.txt`: Archivo de dependencias para instalacion rapida.
