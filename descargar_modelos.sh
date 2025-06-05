#!/bin/bash

echo "🤖 Script para Descargar Modelos de IA"
echo "======================================"
echo ""

# Función para mostrar el menú
mostrar_menu() {
    echo "Selecciona los modelos que quieres descargar:"
    echo ""
    echo "📱 MODELOS LIGEROS (1-3GB):"
    echo "1) phi3:mini (2.3GB) - Microsoft Phi-3, muy eficiente"
    echo "2) gemma2:2b (1.6GB) - Google Gemma 2, ligero"
    echo "3) qwen2.5:3b (2.0GB) - Qwen 2.5, multilingüe"
    echo ""
    echo "⚖️ MODELOS MEDIANOS (4-8GB):"
    echo "4) llama3.1:8b (4.7GB) - Llama 3.1, excelente calidad"
    echo "5) qwen2.5:7b (4.4GB) - Qwen 2.5, multilingüe premium"
    echo "6) mistral:7b (4.1GB) - Mistral AI, muy bueno"
    echo "7) codellama:7b (3.8GB) - Especializado en programación"
    echo ""
    echo "💻 MODELOS PARA CÓDIGO:"
    echo "8) deepseek-coder:6.7b (3.8GB) - Excelente para código"
    echo "9) starcoder2:3b (1.7GB) - Ligero para programación"
    echo ""
    echo "🔥 MODELOS PREMIUM (8GB+):"
    echo "10) qwen2.5:14b (8.2GB) - Premium multilingüe"
    echo "11) llama3.1:70b (40GB) - Máxima calidad (requiere mucha RAM)"
    echo ""
    echo "0) Salir"
    echo ""
}

# Función para descargar modelo
descargar_modelo() {
    local modelo=$1
    local descripcion=$2
    
    echo "📥 Descargando $modelo - $descripcion"
    echo "Esto puede tomar varios minutos dependiendo del tamaño..."
    echo ""
    
    if ollama pull "$modelo"; then
        echo "✅ $modelo descargado exitosamente!"
    else
        echo "❌ Error al descargar $modelo"
    fi
    echo ""
}

# Verificar que Ollama está ejecutándose
if ! pgrep -x "ollama" > /dev/null; then
    echo "⚠️ Ollama no está ejecutándose. Iniciando..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

# Mostrar modelos actuales
echo "📋 Modelos actualmente instalados:"
ollama list
echo ""

# Bucle principal
while true; do
    mostrar_menu
    read -p "Ingresa tu opción (0-11): " opcion
    
    case $opcion in
        1)
            descargar_modelo "phi3:mini" "Microsoft Phi-3 Mini (2.3GB)"
            ;;
        2)
            descargar_modelo "gemma2:2b" "Google Gemma 2 2B (1.6GB)"
            ;;
        3)
            descargar_modelo "qwen2.5:3b" "Qwen 2.5 3B (2.0GB)"
            ;;
        4)
            descargar_modelo "llama3.1:8b" "Llama 3.1 8B (4.7GB)"
            ;;
        5)
            descargar_modelo "qwen2.5:7b" "Qwen 2.5 7B (4.4GB)"
            ;;
        6)
            descargar_modelo "mistral:7b" "Mistral 7B (4.1GB)"
            ;;
        7)
            descargar_modelo "codellama:7b" "Code Llama 7B (3.8GB)"
            ;;
        8)
            descargar_modelo "deepseek-coder:6.7b" "DeepSeek Coder 6.7B (3.8GB)"
            ;;
        9)
            descargar_modelo "starcoder2:3b" "StarCoder2 3B (1.7GB)"
            ;;
        10)
            descargar_modelo "qwen2.5:14b" "Qwen 2.5 14B (8.2GB)"
            ;;
        11)
            echo "⚠️ ADVERTENCIA: Este modelo requiere al menos 64GB de RAM"
            read -p "¿Estás seguro de que quieres continuar? (y/N): " confirmar
            if [[ $confirmar =~ ^[Yy]$ ]]; then
                descargar_modelo "llama3.1:70b" "Llama 3.1 70B (40GB)"
            fi
            ;;
        0)
            echo "👋 ¡Hasta luego!"
            break
            ;;
        *)
            echo "❌ Opción inválida. Por favor selecciona un número del 0 al 11."
            echo ""
            ;;
    esac
    
    # Mostrar modelos actualizados después de cada descarga
    if [[ $opcion != "0" && $opcion =~ ^[1-9]|1[01]$ ]]; then
        echo "📋 Modelos actualizados:"
        ollama list
        echo ""
        read -p "Presiona Enter para continuar..."
        echo ""
    fi
done