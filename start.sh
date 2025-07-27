#!/bin/bash

# Inicializar PostgreSQL
service postgresql start

# Esperar a que PostgreSQL esté listo
sleep 2

# Crear usuario y base de datos
sudo -u postgres psql -c "CREATE USER webapp_user WITH PASSWORD 'webapp_pass';" 2>/dev/null || true
sudo -u postgres psql -c "CREATE DATABASE webapp_db OWNER webapp_user;" 2>/dev/null || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE webapp_db TO webapp_user;" 2>/dev/null || true

# Configurar PostgreSQL para permitir conexiones locales
echo "host all all 127.0.0.1/32 md5" >> /etc/postgresql/*/main/pg_hba.conf
echo "local all all md5" >> /etc/postgresql/*/main/pg_hba.conf

# Reiniciar PostgreSQL con la nueva configuración
service postgresql restart
sleep 2

echo "🚀 Iniciando aplicación web..."
echo "📊 Base de datos PostgreSQL configurada"
echo "🌐 Aplicación disponible en http://localhost:5000"

# Verificar que app.py existe
if [ ! -f "/app/app.py" ]; then
    echo "❌ Error: app.py no encontrado en /app/"
    echo "📁 Contenido de /app/:"
    ls -la /app/
    exit 1
fi

# Ejecutar la aplicación Flask
python app.py