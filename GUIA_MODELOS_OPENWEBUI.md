# 🤖 Guía Completa de Modelos para OpenWebUI

## ✅ Estado Actual: MODELOS INSTALADOS

### 🎉 Modelos Disponibles:

1. **Llama 3.2 1B** (1.3 GB) - Modelo ultraligero y rápido
2. **Llama 3.2 3B** (2.0 GB) - Modelo equilibrado y eficiente

### 🔧 Servicios Ejecutándose:

- ✅ **OpenWebUI**: Puerto 12000
- ✅ **Ollama**: Puerto 11434
- ✅ **Conexión**: Configurada automáticamente

## 🚀 Cómo Usar los Modelos

### 1. Acceder a OpenWebUI:
- URL: https://work-1-pmibcoomalqbelgr.prod-runtime.all-hands.dev
- Crear cuenta de administrador (si no existe)
- Los modelos aparecerán automáticamente en el selector

### 2. Seleccionar Modelo:
- En la interfaz, busca el selector de modelos
- Verás: `llama3.2:1b` y `llama3.2:3b`
- Selecciona el que prefieras usar

## 📥 Descargar Más Modelos

### Modelos Recomendados por Tamaño:

#### 🟢 Ligeros (1-3GB) - Rápidos:
```bash
ollama pull llama3.2:1b          # 1.3GB - Ultraligero
ollama pull llama3.2:3b          # 2.0GB - Ya instalado
ollama pull phi3:mini            # 2.3GB - Microsoft Phi-3
ollama pull gemma2:2b            # 1.6GB - Google Gemma 2
```

#### 🟡 Medianos (4-8GB) - Equilibrados:
```bash
ollama pull llama3.1:8b          # 4.7GB - Llama 3.1
ollama pull qwen2.5:7b           # 4.4GB - Multilingüe excelente
ollama pull mistral:7b           # 4.1GB - Mistral AI
ollama pull codellama:7b         # 3.8GB - Especializado en código
```

#### 🔴 Grandes (10GB+) - Máxima calidad:
```bash
ollama pull llama3.1:70b         # 40GB - Modelo premium
ollama pull qwen2.5:14b          # 8.2GB - Muy bueno
ollama pull mixtral:8x7b         # 26GB - Mixture of Experts
```

### Modelos Especializados:

#### 💻 Para Programación:
```bash
ollama pull codellama:7b         # Código general
ollama pull deepseek-coder:6.7b  # Excelente para código
ollama pull starcoder2:3b        # Ligero para código
```

#### 🌍 Multilingües:
```bash
ollama pull qwen2.5:7b           # Excelente en español
ollama pull aya:8b               # Multilingüe de Cohere
```

#### 🔬 Matemáticas y Ciencias:
```bash
ollama pull mathstral:7b         # Especializado en matemáticas
ollama pull llama3.1:8b          # Bueno en razonamiento
```

## 🛠️ Comandos Útiles

### Gestión de Modelos:
```bash
# Listar modelos instalados
ollama list

# Descargar un modelo
ollama pull [nombre_modelo]

# Eliminar un modelo
ollama rm [nombre_modelo]

# Probar un modelo
ollama run [nombre_modelo] "Hola, ¿cómo estás?"

# Ver información de un modelo
ollama show [nombre_modelo]
```

### Gestión de Servicios:
```bash
# Verificar que Ollama está ejecutándose
ps aux | grep ollama

# Iniciar Ollama (si no está ejecutándose)
ollama serve &

# Verificar modelos disponibles via API
curl http://localhost:11434/api/tags
```

## 🎯 Recomendaciones por Uso

### Para Empezar (Recursos Limitados):
- **llama3.2:1b** - Ya instalado, muy rápido
- **phi3:mini** - Alternativa ligera de Microsoft

### Para Uso General (Equilibrio):
- **llama3.2:3b** - Ya instalado, buen equilibrio
- **qwen2.5:7b** - Excelente multilingüe

### Para Programación:
- **codellama:7b** - Especializado en código
- **deepseek-coder:6.7b** - Muy bueno para desarrollo

### Para Máxima Calidad (Si tienes recursos):
- **llama3.1:8b** - Excelente rendimiento general
- **qwen2.5:14b** - Premium multilingüe

## 🔧 Configuración Avanzada

### Variables de Entorno para Ollama:
```bash
export OLLAMA_HOST=0.0.0.0:11434
export OLLAMA_MODELS=/path/to/models  # Cambiar ubicación de modelos
export OLLAMA_NUM_PARALLEL=2          # Modelos en paralelo
export OLLAMA_MAX_LOADED_MODELS=3     # Máximo modelos cargados
```

### Configurar OpenWebUI para Ollama:
OpenWebUI detecta automáticamente Ollama en `http://localhost:11434`

Si necesitas configurar manualmente:
1. Ve a Configuración en OpenWebUI
2. Busca "Connections" o "Models"
3. Añade: `http://localhost:11434`

## 📊 Comparación de Modelos Instalados

| Modelo | Tamaño | Velocidad | Calidad | Uso Recomendado |
|--------|--------|-----------|---------|-----------------|
| llama3.2:1b | 1.3GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Chat rápido, pruebas |
| llama3.2:3b | 2.0GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Uso general equilibrado |

## 🚨 Solución de Problemas

### Modelo no aparece en OpenWebUI:
```bash
# Verificar que Ollama está ejecutándose
curl http://localhost:11434/api/tags

# Reiniciar OpenWebUI si es necesario
pkill -f open-webui
# Luego reiniciar con el script
```

### Error de memoria:
- Usa modelos más pequeños (1b, 3b)
- Cierra otros programas
- Considera usar cuantización Q4 o Q8

### Modelo muy lento:
- Usa modelos más pequeños
- Verifica que no hay otros procesos pesados
- Considera usar GPU si está disponible

## 🎉 ¡Listo para Usar!

Tus modelos están instalados y funcionando. Puedes:

1. **Acceder a OpenWebUI**: https://work-1-pmibcoomalqbelgr.prod-runtime.all-hands.dev
2. **Crear/Iniciar sesión** en tu cuenta
3. **Seleccionar modelo** en el selector
4. **¡Comenzar a chatear!**

Los modelos `llama3.2:1b` y `llama3.2:3b` están listos para usar inmediatamente.