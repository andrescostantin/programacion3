import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Audio

def generate_shepard_tone(base_freq, num_tones, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    tone = np.zeros_like(t)

    for i in range(num_tones):
        freq = base_freq * (2 ** i)
        amplitude = np.sin(np.pi * i / num_tones) ** 2
        tone += amplitude * np.sin(2 * np.pi * freq * t)

    return tone

def generate_shepard_scale(base_freq, num_tones, duration, sample_rate, steps, descending=False):
    scale = []
    for step in range(steps):
        if descending:
            # Frecuencia base decreciente para la escala descendente
            freq = base_freq * (2 ** ((steps - step - 1) / steps))
        else:
            # Frecuencia base creciente para la escala ascendente
            freq = base_freq * (2 ** (step / steps))
        tone = generate_shepard_tone(freq, num_tones, duration, sample_rate)
        scale.append(tone)
    return np.concatenate(scale)

# Parámetros
base_freq = 440  # Frecuencia base en Hz (Nota La)
num_tones = 6    # Número de tonos superpuestos
duration = 0.5   # Duración de cada tono en segundos
sample_rate = 44100  # Tasa de muestreo
steps = 100  # Número de pasos en la escala (equivalente a una octava)

# Generar la escala de Shepard descendente
shepard_scale_descending = generate_shepard_scale(base_freq, num_tones, duration, sample_rate, steps, descending=True)

# Reproducir la escala descendente
Audio(shepard_scale_descending, rate=sample_rate)

def plot_signal_and_spectrum(signal, sample_rate, title=''):
    # Calcular el tiempo de la señal
    t = np.linspace(0, len(signal) / sample_rate, num=len(signal))

    # Calcular la FFT de la señal
    freqs = np.fft.fftfreq(len(signal), 1/sample_rate)
    spectrum = np.abs(np.fft.fft(signal))

    # Graficar la señal en el dominio del tiempo
    plt.figure(figsize=(14, 8))
    
    plt.subplot(3, 1, 1)
    plt.plot(t, signal)
    plt.title(f'Señal en el tiempo {title}')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')

    # Graficar el espectro de frecuencias
    plt.subplot(3, 1, 2)
    plt.plot(freqs[:len(freqs)//2], spectrum[:len(spectrum)//2])
    plt.title(f'Espectro de frecuencias {title}')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Amplitud')

    # Graficar el espectrograma
    plt.subplot(3, 1, 3)
    plt.specgram(signal, NFFT=1024, Fs=sample_rate, noverlap=512, cmap='inferno')
    plt.title(f'Espectrograma {title}')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Frecuencia [Hz]')
    
    plt.tight_layout()
    plt.show()

# Graficar la señal, espectro y espectrograma de la escala descendente
plot_signal_and_spectrum(shepard_scale_descending, sample_rate, title='Escala Descendente de Shepard')