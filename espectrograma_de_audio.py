import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft

# Cargar el archivo de audio
file_path = 'ruta/a/tu/archivo.wav'  # Reemplaza con la ruta de tu archivo
sample_rate, data = wavfile.read(file_path)

# Información del archivo de audio
num_channels = data.shape[1] if len(data.shape) > 1 else 1
duration = data.shape[0] / sample_rate

print(f"Frecuencia de muestreo: {sample_rate} Hz")
print(f"Duración: {duration:.2f} segundos")
print(f"Cantidad de canales: {num_channels}")

# Si el audio tiene más de un canal, seleccionamos solo el primer canal
if num_channels > 1:
    data = data[:, 0]

# Gráfica de la señal en el tiempo
plt.figure(figsize=(10, 4))
time = np.linspace(0., duration, data.shape[0])
plt.plot(time, data)
plt.title("Señal de Audio en el Tiempo")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")
plt.show()

# Gráfica de la señal en el dominio de la frecuencia
frequencies = np.fft.fftfreq(len(data), 1 / sample_rate)
fft_data = np.abs(fft(data))
plt.figure(figsize=(10, 4))
plt.plot(frequencies[:len(frequencies)//2], fft_data[:len(frequencies)//2])
plt.title("Transformada de Fourier")
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Amplitud")
plt.show()

# Espectrograma
plt.figure(figsize=(10, 4))
plt.specgram(data, Fs=sample_rate, NFFT=1024, noverlap=512, cmap='inferno')
plt.title("Espectrograma")
plt.xlabel("Tiempo [s]")
plt.ylabel("Frecuencia [Hz]")
plt.colorbar(label="Intensidad [dB]")
plt.show()