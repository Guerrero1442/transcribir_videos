from pydantic import BaseModel, Field, field_validator
from typing import Literal
from pathlib import Path

class AppConfig(BaseModel):
    input_path: Path = Field(description="Ruta del archivo o directorio a transcribir.")
    timestamps: bool = Field(default=False, description="Incluir marcas de tiempo en la transcripción.")
    output_format: Literal["txt", "docx", "md"] = Field(default="docx", description="Formato del archivo de salida.")

    @field_validator("input_path")
    def validate_path_exists(cls, v):
        if not v.exists():
            raise ValueError(f"La ruta no existe: {v}")
        return v
