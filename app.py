# app.py
import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv # Opcional: para cargar API key desde .env localmente

# --- Configuración ---
load_dotenv() # Carga variables de entorno desde .env si existe (para desarrollo local)

# Intenta obtener la API Key desde variables de entorno
# ¡IMPORTANTE!: Pasa la API key al contenedor usando variables de entorno (`docker run -e ...`)
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # Si no se proporciona, intenta usar un placeholder o lanza error.
    # En producción, es mejor lanzar un error o tener un manejo más robusto.
    print("¡Advertencia! No se encontró GEMINI_API_KEY. La funcionalidad AI no estará disponible.")
else:
    try:
        genai.configure(api_key=api_key)
        # Modelo a usar
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        print("Cliente Gemini configurado correctamente.")
    except Exception as e:
        print(f"Error configurando el cliente Gemini: {e}")
        model = None # Marcar que el modelo no está disponible

# Crear la aplicación Flask
app = Flask(__name__)

# --- Rutas de la API ---

# Ruta principal (/) - Muestra una interfaz web simple
@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = ""
    prompt_text = ""
    error_text = ""

    if request.method == 'POST':
        prompt_text = request.form.get('prompt')
        if not model:
             error_text = "Error: El modelo Gemini no está configurado (falta API key o hubo error)."
        elif not prompt_text:
            error_text = "Por favor, introduce un prompt."
        else:
            try:
                print(f"Recibido prompt: {prompt_text}")
                # Llamada a la API de Gemini
                response = model.generate_content(prompt_text)
                response_text = response.text
                print(f"Respuesta de Gemini: {response_text[:100]}...") # Log corto
            except Exception as e:
                print(f"Error al llamar a la API de Gemini: {e}")
                error_text = f"Error al contactar la IA: {e}"

    # HTML simple para la interfaz
    html_content = """
    <!doctype html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Prompt a IAG</title>
        <style>
            body { font-family: sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: auto; background-color: #f4f4f4;}
            .container { background-color: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            h1 { color: #333; }
            textarea { width: 95%; padding: 10px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 4px; font-size: 1rem;}
            input[type=submit] { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 1rem;}
            input[type=submit]:hover { background-color: #0056b3; }
            .response { margin-top: 20px; padding: 15px; background-color: #e9ecef; border: 1px solid #ced4da; border-radius: 4px; white-space: pre-wrap; } /* pre-wrap conserva espacios y saltos de línea */
            .error { color: red; font-weight: bold; margin-top: 10px;}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Interactuar con Gemini (vía Docker)</h1>
            <form method="post">
                <label for="prompt">Introduce tu prompt:</label><br>
                <textarea id="prompt" name="prompt" rows="4" required>{{ prompt_text }}</textarea><br>
                <input type="submit" value="Enviar Prompt">
            </form>

            {% if error_text %}
            <div class="error">{{ error_text }}</div>
            {% endif %}

            {% if response_text %}
            <h2>Respuesta de la IA:</h2>
            <div class="response">
                {{ response_text }}
            </div>
            {% endif %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content, prompt_text=prompt_text, response_text=response_text, error_text=error_text)

# --- Ejecutar la aplicación ---
if __name__ == '__main__':
    # Escucha en todas las interfaces (0.0.0.0) para ser accesible desde fuera del contenedor
    # El puerto 5000 es un puerto común para desarrollo con Flask
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) # Debug=False para producción/contenedores