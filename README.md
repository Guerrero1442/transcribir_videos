# Transcripción de Videos con Whisper 🎙️

Este es un proyecto automatizado de línea de comandos (CLI) para transcribir archivos de audio y video utilizando la potente inteligencia artificial de [OpenAI Whisper](https://github.com/openai/whisper). 

## Características Principales

* **Transcriptor por Lotes e Individual**: Puedes enviarle un único archivo de audio/video o apuntar directamente a una carpeta para procesar todos sus archivos multimedia automáticamente.
* **Formatos Flexibles**: Permite exportar las transcripciones en formatos `.docx`, `.md` o `.txt`.
* **Marcas de Tiempo (Timestamps)**: Soporte opcional para añadir los tiempos de inicio y fin para cada línea hablada.
* **Logs Robustos**: Integración con `Loguru` para visualización por terminal y registro histórico en `transcription.log`.
* **Rápido y Seguro**: Escrito utilizando `Pydantic` para validaciones de parámetros de entrada.

## Instalación

El proyecto utiliza [`uv`](https://github.com/astral-sh/uv) como gestor de dependencias ultrarrápido.

1. Clona este repositorio o asegúrate de estar en su directorio.
2. Ejecuta el comando para instalar el entorno y todas las dependencias requeridas (incluyendo PyTorch con soporte CUDA):

```powershell
uv sync
```

## Uso de la Herramienta

Todo el programa se ejecuta a través del script principal `main.py`.

### Comandos Comunes

**1. Procesar un archivo único (Salida en `.docx` por defecto):**
```powershell
uv run python main.py --input_path "C:\ruta\al\video.mp4"
```

**2. Procesar una carpeta entera:**
Si pasas una carpeta, encontrará todos los audios y videos dentro de ella y los procesará uno a uno.
```powershell
uv run python main.py --input_path "C:\ruta\a\tus\videos"
```

**3. Activar las marcas de tiempo (Timestamps):**
```powershell
uv run python main.py --input_path "C:\ruta\al\video.mp4" --timestamps
```

**4. Elegir el formato de salida:**
Actualmente se soportan `docx`, `txt` y `md` (Markdown).
```powershell
uv run python main.py --input_path "C:\ruta\al\video.mp4" --format md
```

### Argumentos de Línea de Comandos
* `--input_path`: (Requerido) Ruta hacia un archivo multimedia individual o un directorio.
* `--timestamps`: (Opcional) Activa la inclusión de timestamps (Start/End) en el archivo resultante.
* `--format`: (Opcional) Tipo de archivo de salida. Valores permitidos: `txt`, `docx`, `md`. (Por defecto: `docx`).

---

## 🖥️ ¿Qué pasa si no tengo una tarjeta gráfica NVIDIA?

El script de transcripción está diseñado para ser inteligente respecto al hardware en el que se ejecuta:

1. **Autodetección:** El script busca automáticamente si existe una tarjeta de video compatible y configurada con los drivers correctos (CUDA de NVIDIA).
2. **Uso de GPU (Recomendado):** Si tienes una gráfica NVIDIA compatible (ej. RTX 3060, 4070, etc.), el sistema cargará el modelo Whisper en la VRAM de tu gráfica. Esto habilitará la aceleración por hardware (usando procesamiento `fp16`), haciendo que transcribir un video sea **extremadamente rápido**.
3. **Uso de CPU (Fallback):** Si **NO tienes una tarjeta gráfica NVIDIA** (o usas AMD/Intel integrado), el programa **NO FALLARÁ**. Simplemente detectará que no hay una GPU compatible e iniciará automáticamente el procesamiento utilizando la **CPU** (procesador central) de tu computadora.

> [!WARNING]
> **Nota sobre el uso en CPU:** 
> Transcribir usando solo el procesador (CPU) funciona perfectamente y arroja los mismos resultados de calidad. Sin embargo, puede llegar a ser *significativamente más lento*, sobre todo porque por defecto la herramienta usa el modelo `large` de Whisper, el cual es el más pesado y preciso. Si ves que en tu procesador el programa toma demasiado tiempo, considera abrir `src/transcriber.py` y cambiar `model_name = "large"` por `"medium"` o `"small"` para sacrificar un poco de exactitud a cambio de mucha velocidad.
