import matplotlib.pyplot as plt
import numpy as np

# Parámetros de la señal
frequency = 1000  # 1 kHz
amplitude = 5     # Amplitud de -5 a 5
duration = 0.01   # 10 ms

# Parámetros de muestreo
sample_rate = 50000  # 50.000 samples per second
num_samples = int(sample_rate * duration)

# Crear el vector de tiempo para la señal continua
t_cont = np.linspace(0, duration, num_samples * 10)  # Más puntos para la señal continua
y_cont = amplitude * np.sin(2 * np.pi * frequency * t_cont)

# Crear el vector de tiempo para la señal muestreada
t_sample = np.linspace(0, duration, num_samples)
y_sample = amplitude * np.sin(2 * np.pi * frequency * t_sample)

# Cuantificación con un ADC de 12 bits
adc_bits = 12
adc_levels = 2 ** adc_bits
quant_step = 2 * amplitude / adc_levels
y_quant = np.round(y_sample / quant_step) * quant_step

# Crear la figura y los ejes para tres subgráficas
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

# Gráfica de la señal continua
ax1.plot(t_cont * 1000, y_cont)  # Convertir tiempo a milisegundos para la gráfica
ax1.set_title('Señal Continua Senoidal de 1 kHz')
ax1.set_xlabel('Tiempo (ms)')
ax1.set_ylabel('Amplitud')
ax1.grid(True)

# Gráfica de las primeras 50 muestras sin cuantificar
ax2.stem(t_sample[:50] * 1000, y_sample[:50])  # Convertir tiempo a milisegundos
ax2.set_title('Primeras 50 muestras sin cuantificar')
ax2.set_xlabel('Tiempo (ms)')
ax2.set_ylabel('Amplitud')
ax2.grid(True)

# Gráfica de las primeras 50 muestras cuantificadas
ax3.stem(t_sample[:50] * 1000, y_quant[:50])  # Convertir tiempo a milisegundos
ax3.set_title('Primeras 50 muestras cuantificadas (ADC de 12 bits)')
ax3.set_xlabel('Tiempo (ms)')
ax3.set_ylabel('Amplitud')
ax3.grid(True)

# Ajustar el espaciado entre las subgráficas
plt.tight_layout()

# Mostrar la gráfica
plt.show()