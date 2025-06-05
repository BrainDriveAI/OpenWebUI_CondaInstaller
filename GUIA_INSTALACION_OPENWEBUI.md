# Guía Paso a Paso: Instalación de OpenWebUI con Conda

## 📋 Requisitos Previos

- Sistema operativo: Linux (Ubuntu/Debian recomendado)
- Acceso a internet
- Permisos de administrador (sudo)
- Al menos 4GB de espacio libre en disco

## 🚀 Instalación Paso a Paso

### Paso 1: Descargar e Instalar Miniconda

```bash
# Descargar Miniconda
cd /tmp
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Instalar Miniconda
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3

# Inicializar conda
export PATH="$HOME/miniconda3/bin:$PATH"
conda init bash
source ~/.bashrc
```

### Paso 2: Crear Entorno Conda para OpenWebUI

```bash
# Crear entorno con Python 3.11
conda create -n openwebui python=3.11 -y

# Activar el entorno
conda activate openwebui
```

### Paso 3: Instalar OpenWebUI

```bash
# Instalar OpenWebUI y todas sus dependencias
pip install open-webui
```

### Paso 4: Configurar Variables de Entorno

```bash
# Generar clave secreta
export WEBUI_SECRET_KEY="$(openssl rand -base64 32)"

# Configurar host y puerto
export WEBUI_HOST="0.0.0.0"
export WEBUI_PORT="8080"
```

### Paso 5: Iniciar OpenWebUI

```bash
# Iniciar el servidor
open-webui serve --host $WEBUI_HOST --port $WEBUI_PORT
```

## 🔧 Script de Inicio Automático

Crea un archivo `start_openwebui.sh`:

```bash
#!/bin/bash

# Script para iniciar OpenWebUI
echo "Iniciando OpenWebUI..."

# Activar el entorno conda
source ~/.bashrc
conda activate openwebui

# Configurar variables de entorno
export WEBUI_SECRET_KEY="$(openssl rand -base64 32)"
export WEBUI_HOST="0.0.0.0"
export WEBUI_PORT="8080"

# Iniciar OpenWebUI
echo "OpenWebUI se iniciará en: http://localhost:$WEBUI_PORT"
echo ""
echo "Para detener el servidor, presiona Ctrl+C"
echo ""

open-webui serve --host $WEBUI_HOST --port $WEBUI_PORT
```

Hacer el script ejecutable:
```bash
chmod +x start_openwebui.sh
```

## 🌐 Acceso a la Aplicación

Una vez iniciado el servidor, puedes acceder a OpenWebUI en:

- **Local**: http://localhost:8080
- **Red local**: http://[tu-ip]:8080

## 📝 Comandos Útiles

### Verificar instalación:
```bash
conda activate openwebui
open-webui --help
```

### Ver procesos en ejecución:
```bash
ps aux | grep open-webui
```

### Detener el servidor:
```bash
# Encontrar el PID del proceso
ps aux | grep open-webui
# Matar el proceso
kill [PID]
```

### Actualizar OpenWebUI:
```bash
conda activate openwebui
pip install --upgrade open-webui
```

## 🔧 Configuración Avanzada

### Variables de Entorno Importantes:

- `WEBUI_SECRET_KEY`: Clave secreta para la aplicación
- `WEBUI_HOST`: Host donde se ejecuta (0.0.0.0 para todas las interfaces)
- `WEBUI_PORT`: Puerto de la aplicación (por defecto 8080)
- `DATA_DIR`: Directorio para almacenar datos
- `OLLAMA_BASE_URL`: URL del servidor Ollama (si usas modelos locales)

### Ejemplo de configuración completa:
```bash
export WEBUI_SECRET_KEY="tu-clave-secreta-aqui"
export WEBUI_HOST="0.0.0.0"
export WEBUI_PORT="8080"
export DATA_DIR="./data"
export OLLAMA_BASE_URL="http://localhost:11434"
```

## 🐛 Solución de Problemas

### Error: "conda: command not found"
```bash
export PATH="$HOME/miniconda3/bin:$PATH"
source ~/.bashrc
```

### Error: "Environment not found"
```bash
conda info --envs
conda create -n openwebui python=3.11 -y
```

### Puerto ocupado:
```bash
# Verificar qué proceso usa el puerto
lsof -i :8080
# Cambiar puerto
export WEBUI_PORT="8081"
```

### Problemas de permisos:
```bash
# Asegurar permisos correctos
chmod -R 755 $HOME/miniconda3
```

## 📚 Recursos Adicionales

- [Documentación oficial de OpenWebUI](https://github.com/open-webui/open-webui)
- [Documentación de Conda](https://docs.conda.io/)
- [Guía de Ollama](https://ollama.ai/) (para modelos locales)

## ✅ Verificación de la Instalación

Para verificar que todo funciona correctamente:

1. **Verificar conda**: `conda --version`
2. **Verificar entorno**: `conda activate openwebui && python --version`
3. **Verificar OpenWebUI**: `open-webui --help`
4. **Probar servidor**: `curl http://localhost:8080`

## 🎉 ¡Instalación Completada!

Si has seguido todos los pasos correctamente, ahora tienes OpenWebUI funcionando en tu sistema. Puedes acceder a la interfaz web y comenzar a usar la aplicación.

### Primer uso:
1. Abre tu navegador web
2. Ve a http://localhost:8080
3. Crea tu primera cuenta de usuario
4. ¡Comienza a usar OpenWebUI!

---

**Nota**: Esta guía está basada en la instalación exitosa realizada en el entorno de desarrollo. Algunos pasos pueden variar según tu sistema operativo específico.