# Dockerfile

# 1. Usar una imagen base oficial de Python ligera
FROM python:3.9-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de requisitos ANTES de copiar el resto del código
#    Esto aprovecha el caché de capas de Docker: si requirements.txt no cambia,
#    no se reinstalarán las dependencias cada vez que cambies tu código.
COPY requirements.txt .

# 4. Instalar las dependencias especificadas en requirements.txt
#    --no-cache-dir: reduce el tamaño de la imagen final
#    --upgrade pip: asegura que pip esté actualizado
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# 5. Copiar el resto del código de la aplicación al directorio de trabajo
COPY app.py .

# 6. Exponer el puerto en el que Flask escuchará dentro del contenedor
#    Este puerto debe coincidir con el que usa app.run() en app.py
EXPOSE 5000

# 7. Definir la variable de entorno para la API Key (será sobrescrita en `docker run`)
#    Es buena práctica definirla aquí aunque sea vacía o con un valor por defecto
#    para que quede claro que la aplicación la espera.
ENV GEMINI_API_KEY=""
ENV PORT=5000 

# 8. Comando para ejecutar la aplicación cuando el contenedor inicie
#    Usa la forma de lista para evitar problemas con señales del shell.
CMD ["python", "app.py"]