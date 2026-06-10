import os
from pathlib import Path
from typing import List, Dict, Any
import whisper
import torch
from docx import Document
from src.exceptions import TranscriptionError, UnsupportedFormatError
from loguru import logger

class VideoTranscriber:
    def __init__(self, model_name: str = "large"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.use_fp16 = self.device == "cuda"
        logger.info(f"Cargando modelo Whisper '{model_name}' en dispositivo: {self.device}")
        
        if self.device == "cuda":
            try:
                logger.info(f"GPU: {torch.cuda.get_device_name(0)} | CUDA: {torch.version.cuda}")
            except Exception:
                pass
                
        try:
            self.model = whisper.load_model(model_name, device=self.device)
        except Exception as e:
            logger.error(f"Error al cargar el modelo: {e}")
            raise TranscriptionError(f"Error al cargar el modelo Whisper: {e}") from e

    def get_supported_files(self, input_path: Path) -> List[Path]:
        """Obtiene una lista de archivos de video/audio soportados."""
        extensions = [".mp4", ".wav", ".flac", ".mp3", ".mkv", ".m4a", ".aac", ".wma", ".ogg", ".dat"]
        if input_path.is_file():
            if input_path.suffix.lower() in extensions:
                return [input_path]
            return []
        elif input_path.is_dir():
            return [p for p in input_path.iterdir() if p.is_file() and p.suffix.lower() in extensions]
        else:
            raise FileNotFoundError(f"La ruta no existe: {input_path}")

    def transcribe_file(self, file_path: Path, with_timestamps: bool) -> List[str]:
        """Transcribe un archivo y devuelve una lista de segmentos formateados."""
        logger.info(f"Iniciando transcripción de: {file_path.name}")
        try:
            result = self.model.transcribe(str(file_path), language="es", fp16=self.use_fp16, verbose=False)
            segments_text = []
            
            for segment in result["segments"]:
                if with_timestamps:
                    start_time = f"{int(segment['start'] // 3600):02d}:{int((segment['start'] % 3600) // 60):02d}:{int(segment['start'] % 60):02d}"
                    end_time = f"{int(segment['end'] // 3600):02d}:{int((segment['end'] % 3600) // 60):02d}:{int(segment['end'] % 60):02d}"
                    segments_text.append(f"Start: {start_time} - End: {end_time}\n{segment['text'].strip()}\n")
                else:
                    segments_text.append(segment['text'].strip())
                    
            logger.success(f"Transcripción completada para: {file_path.name}")
            return segments_text
        except Exception as e:
            logger.error(f"Error durante la transcripción de {file_path.name}: {e}")
            raise TranscriptionError(f"Error transcribiendo {file_path.name}: {e}") from e

    def save_transcription(self, segments: List[str], input_file: Path, output_format: str, with_timestamps: bool):
        """Guarda la transcripción en el formato especificado."""
        base_name = input_file.stem
        output_file = input_file.parent / f"{base_name}.{output_format}"
        
        logger.info(f"Guardando transcripción en formato {output_format}: {output_file}")
        
        try:
            if output_format == "docx":
                doc = Document()
                for segment in segments:
                    doc.add_paragraph(segment)
                doc.save(str(output_file))
            elif output_format == "txt":
                with open(output_file, "w", encoding="utf-8") as f:
                    for segment in segments:
                        f.write(f"{segment}\n")
            elif output_format == "md":
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(f"# Transcripción: {base_name}\n\n")
                    for segment in segments:
                        if with_timestamps:
                            parts = segment.split('\n', 1)
                            if len(parts) == 2:
                                f.write(f"**{parts[0]}**\n\n{parts[1]}\n\n")
                            else:
                                f.write(f"{segment}\n\n")
                        else:
                            f.write(f"{segment}\n\n")
            else:
                raise UnsupportedFormatError(f"El formato '{output_format}' no está soportado.")
                
            logger.success(f"Archivo guardado exitosamente: {output_file}")
        except UnsupportedFormatError:
            raise
        except Exception as e:
            logger.error(f"Error al guardar el archivo {output_file}: {e}")
            raise TranscriptionError(f"Error guardando transcripción: {e}") from e
