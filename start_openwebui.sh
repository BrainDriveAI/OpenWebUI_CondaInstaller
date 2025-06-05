#!/bin/bash

# Script para iniciar OpenWebUI
echo "Iniciando OpenWebUI..."

# Activar el entorno conda
source ~/.bashrc
conda activate openwebui

# Configurar variables de entorno
export WEBUI_SECRET_KEY="$(openssl rand -base64 32)"
export WEBUI_HOST="0.0.0.0"
export WEBUI_PORT="12000"

# Iniciar OpenWebUI
echo "OpenWebUI se iniciará en: http://localhost:$WEBUI_PORT"
echo "También disponible en: https://work-1-pmibcoomalqbelgr.prod-runtime.all-hands.dev"
echo ""
echo "Para detener el servidor, presiona Ctrl+C"
echo ""

open-webui serve --host $WEBUI_HOST --port $WEBUI_PORT