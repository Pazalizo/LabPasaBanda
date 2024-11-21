import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import tkinter as tk
import wavio

# Variables globales para almacenar las señales de audio
audio_signal = None
filtered_signal = None

def grabar_audio(duracion, fs):
    print("Grabando audio...")
    audio_data = sd.rec(int(duracion * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()  
    print("Grabación finalizada.")
    return audio_data.flatten()

def guardar_audio(filename, data, fs):
    wavio.write(filename, data, fs, sampwidth=3)

def aplicar_filtro(x):
    y = np.zeros_like(x)
    for n in range(4, len(x)): 
        y[n] = (0.0168191501071807855)*x[n] - (0.033638300214361571)*x[n-2] + (0.0168191501071807855)*x[n-4] - (0.6676747243939615715)*y[n-4] + (2.7693644473767826031)*y[n-3] - (4.4963496122681461004)*y[n-2] + (3.3939656190685235049)*y[n-1]
    return y

def graficar_espectros(frequencies, fft_result, fft_result_filtered):
    # Filtrar solo frecuencias positivas
    positive_freqs = frequencies > 0
    frequencies = frequencies[positive_freqs]
    fft_result = np.abs(fft_result[positive_freqs])
    fft_result_filtered = np.abs(fft_result_filtered[positive_freqs])

    # Encontrar los máximos
    max_original = np.max(fft_result)
    max_filtered = np.max(fft_result_filtered)
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Gráfica del espectro de la señal de audio original
    axs[0].plot(frequencies, fft_result)
    axs[0].set_xlabel('Frecuencia (Hz)')
    axs[0].set_ylabel('Amplitud')
    axs[0].set_title('Espectro de la señal de audio')
    axs[0].grid()
    axs[0].set_ylim(0, max_original * 1.1)  # Ajustar el límite Y al máximo de la gráfica
    axs[0].set_xlim(0, 8000)  # Limitar el eje x a 8000 Hz
    axs[0].axvline(x=1600, color='red', linestyle='--')  # Línea en x=1600
    axs[0].axvline(x=3600, color='red', linestyle='--')  # Línea en x=3600

    # Gráfica del espectro de la señal de audio filtrada
    axs[1].plot(frequencies, fft_result_filtered)
    axs[1].set_xlabel('Frecuencia (Hz)')
    axs[1].set_ylabel('Amplitud')
    axs[1].set_title('Espectro de la señal filtrada')
    axs[1].grid()
    axs[1].set_ylim(0, max_filtered * 1.1)  # Ajustar el límite Y al máximo de la gráfica
    axs[1].set_xlim(0, 8000)  # Limitar el eje x a 8000 Hz
    axs[1].axvline(x=1600, color='red', linestyle='--')  # Línea en x=1600
    axs[1].axvline(x=3600, color='red', linestyle='--')  # Línea en x=3600

    plt.tight_layout()
    plt.savefig('grafica_ajustada.png')
    plt.show()


def start_recording():
    global audio_signal, filtered_signal

    duracion = 15
    fs = 44100

    audio_signal = grabar_audio(duracion, fs)
    guardar_audio("audio_grabado.wav", audio_signal, fs)

    L = len(audio_signal)
    Ts = 1.0 / fs
    frequencies = np.fft.fftfreq(L, Ts)

    fft_result = np.fft.fft(audio_signal)
    filtered_signal = aplicar_filtro(audio_signal)
    guardar_audio("audio_filtrado.wav", filtered_signal, fs)
    fft_result_filtered = np.fft.fft(filtered_signal)

    graficar_espectros(frequencies, fft_result, fft_result_filtered)

def play_audio():
    if audio_signal is not None:
        sd.play(audio_signal, samplerate=44100)
        sd.wait()
    else:
        print("No hay audio grabado para reproducir.")

def play_filtered_audio():
    if filtered_signal is not None:
        sd.play(filtered_signal, samplerate=44100)
        sd.wait()
    else:
        print("No hay audio filtrado para reproducir.")

# Crear la ventana principal
root = tk.Tk()
root.title("Grabadora de Audio")

# Crear un botón para iniciar la grabación
record_button = tk.Button(root, text="Iniciar Grabación", command=start_recording)
record_button.pack(pady=10)

# Crear un botón para reproducir el audio grabado
play_button = tk.Button(root, text="Reproducir Audio Grabado", command=play_audio)
play_button.pack(pady=10)

# Crear un botón para reproducir el audio filtrado
play_filtered_button = tk.Button(root, text="Reproducir Audio Filtrado", command=play_filtered_audio)
play_filtered_button.pack(pady=10)

# Iniciar el loop de la interfaz
root.mainloop()
