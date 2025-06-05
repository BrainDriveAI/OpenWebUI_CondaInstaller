#!/bin/bash

echo "🚀 Instalando Ollama para modelos locales..."

# Descargar e instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Verificar instalación
ollama --version

echo "✅ Ollama instalado correctamente"
echo ""
echo "📥 Descargando modelos recomendados..."

# Descargar modelos populares (puedes comentar los que no necesites)
echo "Descargando Llama 3.2 (3B) - Modelo rápido y eficiente..."
ollama pull llama3.2:3b

echo "Descargando Llama 3.2 (1B) - Modelo muy ligero..."
ollama pull llama3.2:1b

echo "Descargando Qwen2.5 (7B) - Excelente modelo multilingüe..."
ollama pull qwen2.5:7b

echo "Descargando CodeLlama (7B) - Especializado en código..."
ollama pull codellama:7b

echo ""
echo "🎉 Modelos descargados exitosamente!"
echo ""
echo "🔧 Para usar con OpenWebUI:"
echo "1. Asegúrate de que Ollama esté ejecutándose: ollama serve"
echo "2. En OpenWebUI, los modelos aparecerán automáticamente"
echo ""
echo "📋 Modelos disponibles:"
ollama list