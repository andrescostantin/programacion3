import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.fft import fft, fftfreq
import tkinter as tk
from tkinter import ttk

# Configuración de la captura de audio
FORMAT = pyaudio.paInt16  # Formato de 16 bits
CHANNELS = 1              # Mono
RATE = 44100              # Frecuencia de muestreo
CHUNK = 1024              # Tamaño del bloque de datos
RECORD_SECONDS = 5        # Duración de la grabación

# Variables globales
signal = None

def record_audio():
    global signal
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

    signal = np.concatenate(frames)
    update_plots()  # Mostrar la señal grabada inicialmente

def simple_moving_average(signal, window_size):
    sma = np.zeros_like(signal, dtype=np.float64)
    for n in range(window_size, len(signal)):
        sma[n] = sma[n-1] + (1 / window_size) * (signal[n] - signal[n - window_size])
    sma[:window_size] = np.mean(signal[:window_size])  # Inicialización con la media de la ventana inicial
    return sma

def exponential_moving_average(signal, alpha):
    ema = np.zeros_like(signal, dtype=np.float64)
    ema[0] = signal[0]
    for i in range(1, len(signal)):
        ema[i] = alpha * signal[i] + (1 - alpha) * ema[i - 1]
    return ema

def update_plots():
    if signal is None:
        return

    fig.clear()

    ax1 = fig.add_subplot(211)
    ax1.plot(signal, label='Original', color='#00FF00')  # Verde neón
    if sma_var.get():
        filtered_sma = simple_moving_average(signal, window_size.get())
        ax1.plot(filtered_sma, label=f'SMA Ventana={window_size.get()}', color='#FF00FF')  # Rosa neón
    if ema_var.get():
        filtered_ema = exponential_moving_average(signal, alpha.get())
        ax1.plot(filtered_ema, label=f'EMA α={alpha.get()}', color='#00FFFF')  # Cian neón
    ax1.set_title('Señal de Audio')
    ax1.set_xlabel('Muestras')
    ax1.set_ylabel('Amplitud')
    ax1.legend()

    ax2 = fig.add_subplot(212)
    N = len(signal)
    yf = fft(signal)
    xf = fftfreq(N, 1 / RATE)[:N//2]
    ax2.plot(xf, np.abs(yf[:N//2]), label='Original', color='#00FF00')  # Verde neón
    if sma_var.get():
        yf_filtered = fft(filtered_sma)
        ax2.plot(xf, np.abs(yf_filtered[:N//2]), label=f'SMA Ventana={window_size.get()}', color='#FF00FF')  # Rosa neón
    if ema_var.get():
        yf_filtered = fft(filtered_ema)
        ax2.plot(xf, np.abs(yf_filtered[:N//2]), label=f'EMA α={alpha.get()}', color='#00FFFF')  # Cian neón
    ax2.set_title('Espectro de Frecuencia')
    ax2.set_xlabel('Frecuencia (Hz)')
    ax2.set_ylabel('Magnitud')
    ax2.legend()

    # Estética moderna
    for ax in [ax1, ax2]:
        ax.set_facecolor('#2D2D2D')
        ax.tick_params(axis='x', colors='#FFFFFF')
        ax.tick_params(axis='y', colors='#FFFFFF')
        ax.xaxis.label.set_color('#FFFFFF')
        ax.yaxis.label.set_color('#FFFFFF')
        ax.title.set_color('#FFFFFF')
    
    fig.patch.set_facecolor('#1E1E1E')
    canvas.get_tk_widget().config(bg='#1E1E1E')
    canvas.draw()

# Interfaz gráfica
root = tk.Tk()
root.title("Análisis de Señales de Audio")
root.configure(bg='#1E1E1E')  # Fondo oscuro

# Variables
window_size = tk.IntVar(value=10)
alpha = tk.DoubleVar(value=0.6)
sma_var = tk.BooleanVar(value=True)
ema_var = tk.BooleanVar(value=True)

# Configuración de la interfaz con un diseño en cuadrícula
frame_controls = ttk.Frame(root, padding="10 10 10 10", style="TFrame")
frame_controls.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame_controls.configure(relief='flat')

ttk.Label(frame_controls, text="Tamaño de Ventana SMA:", style="TLabel").grid(column=0, row=0, padx=10, pady=10, sticky='w')
ttk.Entry(frame_controls, textvariable=window_size, width=10).grid(column=1, row=0, padx=10, pady=10)

ttk.Label(frame_controls, text="Factor de Suavizado EMA:", style="TLabel").grid(column=0, row=1, padx=10, pady=10, sticky='w')
ttk.Entry(frame_controls, textvariable=alpha, width=10).grid(column=1, row=1, padx=10, pady=10)

ttk.Checkbutton(frame_controls, text="Habilitar SMA", variable=sma_var, style="TCheckbutton").grid(column=0, row=2, padx=10, pady=10, sticky='w')
ttk.Checkbutton(frame_controls, text="Habilitar EMA", variable=ema_var, style="TCheckbutton").grid(column=1, row=2, padx=10, pady=10, sticky='w')

ttk.Button(frame_controls, text="Grabar Audio", command=record_audio, style="TButton").grid(column=0, row=3, padx=10, pady=20)
ttk.Button(frame_controls, text="Aplicar Filtros", command=update_plots, style="TButton").grid(column=1, row=3, padx=10, pady=20)

# Configuración de la visualización de gráficos
fig = plt.Figure(figsize=(8, 6), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=1, row=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

# Estilo moderno
style = ttk.Style()
style.configure("TFrame", background='#1E1E1E')
style.configure("TLabel", background='#1E1E1E', foreground='#FFFFFF')
style.configure("TButton", background='#00FF00', foreground='#000000', font=('Helvetica', 10, 'bold'))
style.configure("TCheckbutton", background='#1E1E1E', foreground='#FFFFFF')

root.mainloop()