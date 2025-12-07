'''
Este codelab fue realizado por:
- Nombre: Jhon Alejandro Martinez
- Código: 202259565

- Nombre: Juan Miguel Posso Alvarado
- Código: 202259610

- Nombre: Nicolas Mauricio Rojas Mendoza
- Código: 202259460

- Nombre: Esteban Alexander Revelo Salazar
- Código: 202067507

'''
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import tempfile, os, webbrowser
from googletrans import Translator

SRATE = 16000     # tasa de muestreo
DUR = 5           # segundos

translator = Translator()

def traducir_a_espanol(texto_en):
    """Traduce texto del inglés al español"""
    try:
        traduccion = translator.translate(texto_en, src="en", dest="es")
        return traduccion.text
    except Exception as e:
        return f"Error al traducir: {e}"

print("Grabando en inglés... habla ahora!")
audio = sd.rec(int(DUR*SRATE), samplerate=SRATE, channels=1, dtype='int16')
sd.wait()
print("Listo, procesando...")

# guarda a WAV temporal
tmp_wav = tempfile.mktemp(suffix=".wav")
write(tmp_wav, SRATE, audio)

r = sr.Recognizer()

try:
    with sr.AudioFile(tmp_wav) as source:
        data = r.record(source)

    # Reconocer solo en inglés
    texto_en = r.recognize_google(data, language="en-US").lower()
    print("Dijiste en inglés:", texto_en)

    if "youtube" in texto_en:
        print(" Abriendo YouTube...")
        webbrowser.open("https://www.youtube.com")
    elif "facebook" in texto_en:
        print(" Abriendo Facebook...")
        webbrowser.open("https://www.facebook.com")
    elif "instagram" in texto_en:
        print(" Abriendo Instagram...")
        webbrowser.open("https://www.instagram.com")

    traduccion = traducir_a_espanol(texto_en)
    print(f"Traducción al español: {traduccion}")

except sr.UnknownValueError:
    print("No entendí lo que dijiste en inglés.")
except sr.RequestError as e:
    print("Error con el servicio:", e)
finally:
    if os.path.exists(tmp_wav):
        os.remove(tmp_wav)
