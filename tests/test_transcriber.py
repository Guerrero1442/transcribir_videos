import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.transcriber import VideoTranscriber
from src.exceptions import UnsupportedFormatError

@patch('src.transcriber.whisper.load_model')
@patch('src.transcriber.torch.cuda.is_available', return_value=False)
def test_transcriber_init(mock_cuda, mock_load_model):
    # Mockear la carga del modelo para no descargar whisper durante las pruebas
    transcriber = VideoTranscriber(model_name="tiny")
    assert transcriber.device == "cpu"
    assert transcriber.use_fp16 is False
    mock_load_model.assert_called_once_with("tiny", device="cpu")

@patch('src.transcriber.whisper.load_model')
def test_get_supported_files(mock_load_model, tmp_path):
    transcriber = VideoTranscriber(model_name="tiny")
    
    # Crear archivos falsos
    (tmp_path / "video1.mp4").touch()
    (tmp_path / "audio.mp3").touch()
    (tmp_path / "texto.txt").touch()
    (tmp_path / "imagen.jpg").touch()
    
    archivos = transcriber.get_supported_files(tmp_path)
    
    assert len(archivos) == 2
    nombres = [p.name for p in archivos]
    assert "video1.mp4" in nombres
    assert "audio.mp3" in nombres

@patch('src.transcriber.whisper.load_model')
def test_save_transcription_txt(mock_load_model, tmp_path):
    transcriber = VideoTranscriber(model_name="tiny")
    
    video_file = tmp_path / "mi_video.mp4"
    segmentos = ["Hola esto es una prueba", "Segmento 2"]
    
    transcriber.save_transcription(segmentos, video_file, "txt", with_timestamps=False)
    
    output_file = tmp_path / "mi_video.txt"
    assert output_file.exists()
    
    content = output_file.read_text(encoding="utf-8")
    assert "Hola esto es una prueba\nSegmento 2\n" == content

@patch('src.transcriber.whisper.load_model')
def test_save_transcription_unsupported_format(mock_load_model, tmp_path):
    transcriber = VideoTranscriber(model_name="tiny")
    video_file = tmp_path / "video.mp4"
    
    with pytest.raises(UnsupportedFormatError):
        transcriber.save_transcription(["Hola"], video_file, "pdf", False)
