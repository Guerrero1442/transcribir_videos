import argparse
from pathlib import Path
import sys
from loguru import logger
from pydantic import ValidationError

from src.config import AppConfig
from src.logger import setup_logger
from src.transcriber import VideoTranscriber
from src.exceptions import TranscriptionProjectError

def main():
    setup_logger()
    
    parser = argparse.ArgumentParser(description="Automatización de transcripción de videos.")
    parser.add_argument("--input_path", type=str, required=True, help="Ruta del archivo o directorio a transcribir.")
    parser.add_argument("--timestamps", action="store_true", help="Incluir marcas de tiempo en la transcripción.")
    parser.add_argument("--format", type=str, choices=["txt", "docx", "md"], default="docx", help="Formato del archivo de salida (txt, docx, md).")
    
    args = parser.parse_args()
    
    try:
        # Validar configuración con Pydantic
        config = AppConfig(
            input_path=Path(args.input_path),
            timestamps=args.timestamps,
            output_format=args.format
        )
        logger.info(f"Configuración validada: Ruta='{config.input_path}', Timestamps={config.timestamps}, Formato='{config.output_format}'")
        
        # Inicializar transcriptor
        transcriber = VideoTranscriber()
        
        # Obtener archivos
        files_to_process = transcriber.get_supported_files(config.input_path)
        if not files_to_process:
            logger.warning(f"No se encontraron archivos de video/audio soportados en {config.input_path}")
            return
            
        logger.info(f"Se encontraron {len(files_to_process)} archivos para procesar.")
        
        # Procesar archivos
        for idx, file_path in enumerate(files_to_process, 1):
            logger.info(f"Procesando archivo {idx}/{len(files_to_process)}: {file_path.name}")
            segments = transcriber.transcribe_file(file_path, config.timestamps)
            transcriber.save_transcription(segments, file_path, config.output_format, config.timestamps)
            
        logger.success("¡Proceso completado exitosamente para todos los archivos!")
        
    except ValidationError as e:
        logger.error("Error de validación en los parámetros proporcionados:")
        for error in e.errors():
            logger.error(f" - {error['loc'][0]}: {error['msg']}")
        sys.exit(1)
    except TranscriptionProjectError as e:
        logger.error(f"Error en el proyecto de transcripción: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
