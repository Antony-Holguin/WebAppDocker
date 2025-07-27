
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    sudo \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación
COPY . .

# Crear script de inicialización
COPY start.sh /start.sh
RUN chmod +x /start.sh


EXPOSE 5000


CMD ["/start.sh"]