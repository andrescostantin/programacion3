import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# Configuración de la captura de audio
FORMAT = pyaudio.paInt16  # Formato de 16 bits
CHANNELS = 1              # Mono
RATE = 44100              # Frecuencia de muestreo
CHUNK = 1024              # Tamaño del bloque de datos
RECORD_SECONDS = 5        # Duración de la grabación

def record_audio():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* Grabando...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(np.frombuffer(data, dtype=np.int16))

    print("* Grabación finalizada")

    stream.stop_stream()
    stream.close()
    p.terminate()

    return np.concatenate(frames)

def exponential_moving_average(signal, alpha):
    ema = np.zeros_like(signal, dtype=np.float64)
    ema[0] = signal[0]
    for i in range(1, len(signal)):
        ema[i] = alpha * signal[i] + (1 - alpha) * ema[i - 1]
    return ema

def plot_signal(original, filtered_signals, alphas):
    plt.figure(figsize=(14, 8))

    plt.subplot(2, 1, 1)
    plt.plot(original, label='Original', color='black')
    for filtered, alpha in zip(filtered_signals, alphas):
        plt.plot(filtered, label=f'Suavizado α={alpha}')
    plt.legend()
    plt.title('Señal Original y Suavizada')
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')

    plt.subplot(2, 1, 2)
    N = len(original)
    yf = fft(original)
    xf = fftfreq(N, 1 / RATE)[:N//2]
    plt.plot(xf, np.abs(yf[:N//2]), label='Espectro de la señal original', color='black')
    
    for filtered, alpha in zip(filtered_signals, alphas):
        yf_filtered = fft(filtered)
        plt.plot(xf, np.abs(yf_filtered[:N//2]), label=f'Espectro suavizado α={alpha}')
    plt.legend()
    plt.title('Análisis de Espectro de Frecuencia')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')

    plt.tight_layout()
    plt.show()

# Captura de audio
signal = record_audio()

# Aplicar el filtro de media móvil exponencial con diferentes factores
alphas = [0.6, 0.2, 0.05]
filtered_signals = [exponential_moving_average(signal, alpha) for alpha in alphas]

# Visualización
plot_signal(signal, filtered_signals, alphas)