import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

def quantize_signal(signal, num_bits, min_val, max_val):
    """
    Cuantifica una señal según el número de bits del ADC.

    Parámetros:
    signal (array-like): La señal de entrada a cuantificar.
    num_bits (int): Número de bits del ADC.
    min_val (float): Valor mínimo de la señal.
    max_val (float): Valor máximo de la señal.

    Retorna:
    numpy.array: La señal cuantificada.
    """
    # Calcular el número de niveles de cuantificación
    levels = 2 ** num_bits

    # Calcular el tamaño del paso de cuantificación
    quant_step = (max_val - min_val) / levels

    # Cuantificar la señal
    quantized_signal = np.round((signal - min_val) / quant_step) * quant_step + min_val

    # Asegurarse de que los valores cuantificados estén dentro del rango
    quantized_signal = np.clip(quantized_signal, min_val, max_val)

    return quantized_signal

# Parámetros de la señal
amplitude = 1.0
duration = 2
sample_rate = 300  # Frecuencia de muestreo de audio estándar

# Crear el vector de tiempo
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Definir las frecuencias de la onda cuadrada y triangular
frequency_square = 440  # 440 Hz (La4)
frequency_triangle = 880  # 880 Hz (La5)

# Crear la onda cuadrada
square_wave = amplitude * np.sign(np.sin(2 * np.pi * frequency_square * t))

# Crear la onda triangular
triangle_wave = amplitude * (2 * np.arcsin(np.sin(2 * np.pi * frequency_triangle * t)) / np.pi)

# Sumar las dos ondas
combined_wave = square_wave + triangle_wave


def sonar():
    sd.play(square_wave, samplerate=sample_rate)
    sd.wait()
    sd.play(triangle_wave, samplerate=sample_rate)
    sd.wait()
    sd.play(combined_wave, samplerate=sample_rate)
    sd.wait()

def visualizar(a,b,c):
    # Crear la figura
    plt.figure(figsize=(10, 8))
    # Gráfico de la onda cuadrada
    plt.subplot(3, 1, 1)
    plt.plot(t, a)
    plt.title('Onda Cuadrada - 440 Hz')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.grid(True)

    # Gráfico de la onda triangular
    plt.subplot(3, 1, 2)
    plt.plot(t, b)
    plt.title('Onda Triangular - 880 Hz')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.grid(True)

    # Gráfico de la señal combinada
    plt.subplot(3, 1, 3)
    plt.plot(t, c)
    plt.title('Onda Combinada (Cuadrada + Triangular)')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.grid(True)

    # Ajustar el espaciado entre subplots
    plt.tight_layout()

    # Mostrar la gráfica
    plt.show()

while True:
    num_bits, min_val, max_val = int(input("numro de bits:\n")),int(input("valor minimo:\n")),int(input("valor maximo:\n"))
    triangular_cuantificada = quantize_signal(triangle_wave,num_bits,min_val,max_val)
    cuadrada_cuantificada = quantize_signal(square_wave,num_bits,min_val,max_val)
    combinada_cuantificada = quantize_signal(combined_wave,num_bits,min_val,max_val)
    visualizar_op = input("desea visualizar las funciones? (s/n)")
    if visualizar_op == "s":
        visualizar(triangular_cuantificada,cuadrada_cuantificada,combinada_cuantificada)
    
    audio_op = input("desea que las funciones suenen? (s/n)")
    if audio_op == "s":
        sonar()
    

