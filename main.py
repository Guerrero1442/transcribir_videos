import whisper
from docx import Document
from tkinter import filedialog


# Seleccionar el archivo de audio
ruta_audio = filedialog.askopenfilename(title="Selecciona el archivo de audio", filetypes=[("Audio files", "*.mp4 *.wav *.flac *.mp3 *.mkv")])
model = whisper.load_model("medium")

# Transcribir el audio con opción para obtener JSON detallado
result = model.transcribe(ruta_audio, language='es', verbose=False, fp16=False)

# Crear un nuevo documento de Word
doc = Document()

# Agregar la transcripción y los timestamps al documento
for segment in result['segments']:
    # Formatear los timestamps
    start_time = f"{int(segment['start'] // 3600):02d}:{int((segment['start'] % 3600) // 60):02d}:{int(segment['start'] % 60):02d}"
    end_time = f"{int(segment['end'] // 3600):02d}:{int((segment['end'] % 3600) // 60):02d}:{int(segment['end'] % 60):02d}"

    # Crear el texto del segmento con los timestamps
    segment_text = f"Start: {start_time} - End: {end_time}\n{segment['text']}\n\n"

    # Agregar el texto al documento
    doc.add_paragraph(segment_text)

# Guardar el documento
doc.save("propuestas_continuidad_representacion.docx")
