# iag-docker-gemini
Repositorio para una tarea de la asignatura M2D del curso de especialización de Inteligencia Artificial.

# Implementación de Prompt en Docker con Gemini API

Este proyecto implementa una aplicación web simple dentro de un contenedor Docker que permite a los usuarios enviar prompts a un modelo de Inteligencia Artificial Generativa (IAG) gratuito, específicamente Google Gemini Pro, a través de su API.

## Requisitos Previos

*   Docker instalado y funcionando.
*   Una clave API de Google Gemini. Puedes obtenerla gratuitamente en [Google AI Studio](https://aistudio.google.com/app/apikey).
*   Git (opcional, para clonar si lo subes a un repositorio).

## Estructura del Proyecto 
/
├── Dockerfile # Instrucciones para construir la imagen Docker
├── app.py # Aplicación web Flask que interactúa con Gemini
├── requirements.txt # Dependencias de Python
└── README.md # Esta documentación

## Configuración y Ejecución

1.  **Clonar el Repositorio (si aplica):**
    ```bash
    git clone https://github.com/Santiago20032015/iag-docker-gemini
    cd iag-docker-gemini
    ```

2.  **Obtener API Key:** Asegúrate de tener tu clave API de Google Gemini.

3.  **Construir la Imagen Docker:**
    Desde la raíz del proyecto, ejecuta:
    ```bash
    docker build -t iag-gemini-app .
    ```

4.  **Ejecutar el Contenedor Docker:**
    Reemplaza `"TU_API_KEY_DE_GEMINI"` con tu clave API real.
    ```bash
    docker run -p 5050:5000 -e GEMINI_API_KEY="TU_API_KEY_DE_GEMINI" --name gemini_container iag-gemini-app
    ```
    *   `-p 5050:5000`: Mapea el puerto 5050 de tu máquina al puerto 5000 del contenedor.
    *   `-e GEMINI_API_KEY="..."`: Pasa la API Key al contenedor de forma segura como variable de entorno.
    *   `--name gemini_container`: Asigna un nombre al contenedor.

## Interacción con el Sistema

Una vez que el contenedor esté en ejecución:

1.  Abre tu navegador web y navega a `http://localhost:5050` (o el puerto que hayas mapeado).
2.  Verás una interfaz simple con un área de texto.
3.  **Prompt:** Escribe tu pregunta o instrucción en el área de texto.
4.  Haz clic en el botón "Enviar Prompt".
5.  **Respuesta:** La respuesta generada por el modelo Gemini aparecerá debajo del formulario.

*(Opcional: Si hubieras hecho un endpoint API JSON en `/api/prompt`)*
*   Puedes interactuar programáticamente enviando una solicitud POST con `curl`:
    ```bash
    curl -X POST -H "Content-Type: application/json" \
         -d '{"prompt": "Explica Docker en términos simples"}' \
         http://localhost:5050/api/prompt
    ```
*   La respuesta sería un JSON como: `{"response": "Docker es como un contenedor mágico..."}`

## Modelo IAG Utilizado: Google Gemini

*   **Modelo Específico:** `gemini-1.5-pro-latest` (a través de la API de Google AI).
*   **Cómo se conecta:** Mediante la API REST oficial de Google AI (`generativelanguage.googleapis.com`). La conexión se realiza desde el script `app.py` usando la librería `google-generativeai` y requiere autenticación mediante una API Key pasada como variable de entorno al contenedor.
*   **Tipo de Modelo:** Es un modelo de lenguaje grande (LLM) multimodal de última generación basado en la arquitectura Transformer, desarrollado por Google. En este caso, lo usamos principalmente para generación de texto.
*   **Limitaciones:**
    *   **Coste:** Tiene un nivel gratuito generoso, pero el uso por encima de los límites puede incurrir en costes. Verifica la [página de precios de Google AI](https://ai.google.dev/pricing) para detalles actualizados.
    *   **Tokens:** Existen límites en la cantidad de tokens (palabras/subpalabras) por prompt y por respuesta. Consulta la documentación de Gemini para los límites específicos del modelo `gemini-1.5-pro-latest`.
    *   **Rendimiento:** La latencia de la API puede variar. El rendimiento y la calidad de la respuesta dependen del prompt y la carga actual del servicio.
    *   **Filtros de Seguridad:** Google aplica filtros de seguridad que pueden bloquear prompts o respuestas consideradas inapropiadas o dañinas.
    *   **Disponibilidad:** La API depende de los servicios de Google Cloud y podría tener tiempos de inactividad.

## Explicación del Código Principal (`app.py`)

*   **Importaciones:** Se importan Flask (para el servidor web), `google.generativeai` (para la API de Gemini), `os` (para leer variables de entorno) y `render_template_string` (para generar el HTML simple).
*   **Configuración de Gemini:** Se lee la `GEMINI_API_KEY` de las variables de entorno y se configura el cliente de `google-generativeai`. Se instancia el modelo `gemini-1.5-pro-latest`.
*   **Aplicación Flask:** Se crea una instancia de la aplicación Flask.
*   **Ruta `/` (GET y POST):**
    *   Maneja tanto las solicitudes GET (para mostrar el formulario) como las POST (cuando se envía el formulario).
    *   Si es POST, extrae el `prompt` del formulario.
    *   Llama a `model.generate_content(prompt)` para obtener la respuesta de Gemini.
    *   Maneja posibles errores durante la llamada a la API.
    *   Renderiza una plantilla HTML simple (`render_template_string`) pasándole el prompt anterior, la respuesta obtenida o cualquier error.
*   **Ejecución del Servidor:** `app.run(host='0.0.0.0', port=5000)` inicia el servidor Flask, haciéndolo accesible desde fuera del contenedor en el puerto 5000. `host='0.0.0.0'` es crucial para la accesibilidad desde Docker.

## Explicación del `Dockerfile`

*   `FROM python:3.9-slim`: Usa una imagen base oficial de Python ligera.
*   `WORKDIR /app`: Establece el directorio de trabajo dentro del contenedor.
*   `COPY requirements.txt .` y `RUN pip install ...`: Copia e instala las dependencias primero para aprovechar el caché de Docker.
*   `COPY app.py .`: Copia el código de la aplicación.
*   `EXPOSE 5000`: Informa a Docker que el contenedor escuchará en el puerto 5000.
*   `ENV GEMINI_API_KEY=""`: Declara la variable de entorno que espera la aplicación (se proporciona en `docker run`).
*   `CMD ["python", "app.py"]`: Define el comando por defecto para ejecutar cuando el contenedor inicie.
