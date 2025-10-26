# Imagen base ligera de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el código de la app
COPY . .
# COPY ../requeriments.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Exponer el puerto usado por Uvicorn
EXPOSE 8000

# Comando para iniciar el servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
