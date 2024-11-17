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

def graficar_señales(t, audio_signal, frequencies, fft_result, filtered_signal, fft_result_filtered):
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    axs[0, 0].plot(t, audio_signal)
    axs[0, 0].set_xlabel('Tiempo [s]')
    axs[0, 0].set_ylabel('Amplitud')
    axs[0, 0].set_title('Señal de audio')
    axs[0, 0].grid()

    axs[0, 1].plot(frequencies, np.abs(fft_result))
    axs[0, 1].set_xlabel('Frecuencia (Hz)')
    axs[0, 1].set_ylabel('Amplitud')
    axs[0, 1].set_title('Espectro de la señal de audio')
    axs[0, 1].grid()

    axs[1, 0].plot(t, filtered_signal)
    axs[1, 0].set_xlabel('Tiempo [s]')
    axs[1, 0].set_ylabel('Amplitud')
    axs[1, 0].set_title('Señal de audio filtrada')
    axs[1, 0].grid()

    axs[1, 1].plot(frequencies, np.abs(fft_result_filtered))
    axs[1, 1].set_xlabel('Frecuencia (Hz)')
    axs[1, 1].set_ylabel('Amplitud')
    axs[1, 1].set_title('Espectro de la señal filtrada')
    axs[1, 1].grid()
    max_amplitude = max(np.max(np.abs(fft_result)), np.max(np.abs(fft_result_filtered)))
    axs[0, 1].set_ylim(0, max_amplitude)
    axs[1, 1].set_ylim(0, max_amplitude)

    plt.tight_layout()
    plt.savefig('grafica.png')
    plt.show()

def start_recording():
    global audio_signal, filtered_signal

    duracion = 2 
    fs = 44100

    audio_signal = grabar_audio(duracion, fs)
    guardar_audio("audio_grabado.wav", audio_signal, fs)

    L = len(audio_signal)
    # Calcular el tiempo de muestreo
    Ts = 1.0 / fs
    # Crear un vector de tiempo
    t = Ts * np.arange(0, L)
    # Calcular la transformada de Fourier de la señal de audio
    fft_result = np.fft.fft(audio_signal)
    # Calcular las frecuencias correspondientes a cada punto de la FFT
    frequencies = np.fft.fftfreq(L, Ts)

    filtered_signal = aplicar_filtro(audio_signal)
    
    guardar_audio("audio_filtrado.wav", filtered_signal, fs)

    # Calcular la transformada de Fourier de la señal filtrada
    fft_result_filtered = np.fft.fft(filtered_signal)

    graficar_señales(t, audio_signal, frequencies, fft_result, filtered_signal, fft_result_filtered)

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
