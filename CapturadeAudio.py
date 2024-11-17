import sounddevice as sd
import wave
import os
import numpy as np


def grabar_audio(nombre_archivo, duracion_segundos, frecuencia_muestreo):
    # Grabar audio
    audio = sd.rec(int(duracion_segundos * frecuencia_muestreo), samplerate=frecuencia_muestreo, channels=1, dtype='int16')
    sd.wait()  # Esperar a que termine la grabación

    # Guardar audio en formato WAV
    archivo_wav = wave.open(nombre_archivo, 'wb')
    archivo_wav.setnchannels(1)
    archivo_wav.setsampwidth(2)
    archivo_wav.setframerate(frecuencia_muestreo)
    archivo_wav.writeframes(audio.tobytes())
    archivo_wav.close()

    print(f"Audio guardado como {nombre_archivo}")

def imprimir_audio(nombre_archivo):
    # Abrir el archivo WAV
    archivo_wav = wave.open(nombre_archivo, 'rb')

    # Leer los datos del audio
    frames = archivo_wav.readframes(-1)
    muestra_audio = np.frombuffer(frames, dtype=np.int16)

    # Imprimir los valores de las muestras del audio
    print("Audio grabado:")
    print(muestra_audio)
    print("Puntos:")
    print(len(muestra_audio))

    # Cerrar el archivo
    archivo_wav.close()

if __name__ == "__main__":
    nombre_archivo = "audio_grabado.wav"
    duracion_segundos = 1
    frecuencia_muestreo = 44100

    print("Grabando audio...")
    grabar_audio(nombre_archivo, duracion_segundos, frecuencia_muestreo)

    # Mostrar la cantidad de puntos en el audio
    imprimir_audio(nombre_archivo)


