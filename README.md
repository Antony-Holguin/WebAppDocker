

## Instrucciones

### Prerrequisitos
- Docker instalado en el sistema

### 1. Construir la imagen Docker
```bash
docker build -t webapp-docker .
```

### 2. Ejecutar la aplicación web

**Modo producción:**
```bash
docker run -p 5000:5000 webapp-docker
```

**Modo desarrollo (con hot reload):**
```bash
# Debe estar en el directorio del proyecto donde está el código
docker run -p 5000:5000 -v "$(pwd):/app" webapp-docker
```

### 3. Acceder a la aplicación
Abrir navegador web en: **http://localhost:5000**


## 🔧 Scripts alternativos (legacy)

```bash
# Ejecutar script de análisis original
docker run webapp-docker python tagger_post.py

# Ejecutar script de análisis con URL externa
docker run webapp-docker python tagger_get.py
```

