import whisper
from docx import Document

ruta_audio = r"C:\Users\camil\Downloads\video-229983a8-0edb-48a4-be1a-43d2e3754b18.mp4"
model = whisper.load_model("large")

# Transcribir el audio con opción para obtener JSON detallado
result = model.transcribe(ruta_audio, language='es', verbose=False, fp16=False)

# Crear un nuevo documento de Word
doc = Document()

# Agregar solo la transcripción al documento sin los timestamps
for segment in result['segments']:
    # Crear el texto del segmento sin los timestamps
    segment_text = f"{segment['text']}\n"

    # Agregar el texto al documento
    doc.add_paragraph(segment_text)

# Guardar el documento
doc.save("IRAC_MONITORIA_large.docx")
