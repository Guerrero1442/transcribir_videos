import pytest
from pydantic import ValidationError
from pathlib import Path
from src.config import AppConfig

def test_valid_config(tmp_path):
    # Setup un directorio temporal válido
    d = tmp_path / "videos"
    d.mkdir()
    
    config = AppConfig(input_path=d, timestamps=True, output_format="md")
    
    assert config.input_path == d
    assert config.timestamps is True
    assert config.output_format == "md"

def test_invalid_input_path():
    with pytest.raises(ValidationError):
        AppConfig(input_path=Path("/ruta/que/no/existe/999"))

def test_invalid_output_format(tmp_path):
    d = tmp_path / "videos"
    d.mkdir()
    
    with pytest.raises(ValidationError):
        AppConfig(input_path=d, output_format="mp3") # Formato no soportado

def test_default_values(tmp_path):
    d = tmp_path / "videos"
    d.mkdir()
    
    config = AppConfig(input_path=d)
    assert config.timestamps is False
    assert config.output_format == "docx"
