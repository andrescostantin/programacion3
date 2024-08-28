import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def generar_senal(num_simbolos=100):
    # Genera una señal aleatoria de 0s y 1s
    return np.random.choice([0, 1], size=num_simbolos)

def filtro_coseno_alzado(beta, sps, num_taps):
    """
    Crea un filtro de coseno alzado.
    
    beta: Roll-off factor
    sps: Símbolos por segundo (samples per symbol)
    num_taps: Número de coeficientes del filtro (taps)
    """
    t = np.arange(-num_taps // 2, num_taps // 2 + 1) / sps
    sinc = np.sinc(t)
    denominator = (1 - (2 * beta * t)**2)
    
    # Prevenir división por cero
    cos_alzado = np.where(np.abs(denominator) < 1e-10,
                          np.pi / 4 * np.sin(np.pi / (2 * beta)),
                          np.cos(np.pi * beta * t) / denominator)
    
    return sinc * cos_alzado

def aplicar_filtro(senal, filtro):
    # Convolucionar la señal con el filtro
    return np.convolve(senal, filtro, mode='same')

def graficar_senal(fig, ax, t, senal, titulo):
    ax.clear()
    ax.plot(t, senal)
    ax.set_title(titulo)
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Amplitud')
    fig.canvas.draw()

def preparar_interfaz():
    ventana = tk.Tk()
    ventana.title("Simulación de Transmisión de Señal con Filtro de Coseno Alzado")

    frame_graficas = ttk.Frame(ventana)
    frame_graficas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
    canvas = FigureCanvasTkAgg(fig, master=frame_graficas)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def simular():
        num_simbolos = int(entry_simbolos.get())
        beta = float(entry_rolloff.get())
        sps = int(entry_sps.get())
        num_taps = int(entry_taps.get())

        senal = generar_senal(num_simbolos)
        filtro = filtro_coseno_alzado(beta, sps, num_taps)
        senal_filtrada = aplicar_filtro(senal, filtro)

        # Ajustar longitud de t para que coincida con la señal filtrada
        t = np.arange(len(senal_filtrada))

        graficar_senal(fig, ax1, np.arange(len(senal)), senal, 'Señal Original')
        graficar_senal(fig, ax2, t, senal_filtrada, 'Señal Filtrada')

    frame_controles = ttk.Frame(ventana)
    frame_controles.pack(side=tk.BOTTOM, fill=tk.X)

    ttk.Label(frame_controles, text="Número de símbolos:").pack(side=tk.LEFT)
    entry_simbolos = ttk.Entry(frame_controles, width=5)
    entry_simbolos.pack(side=tk.LEFT)
    entry_simbolos.insert(0, "100")

    ttk.Label(frame_controles, text="Factor de roll-off (beta):").pack(side=tk.LEFT)
    entry_rolloff = ttk.Entry(frame_controles, width=5)
    entry_rolloff.pack(side=tk.LEFT)
    entry_rolloff.insert(0, "0.25")

    ttk.Label(frame_controles, text="Símbolos por segundo:").pack(side=tk.LEFT)
    entry_sps = ttk.Entry(frame_controles, width=5)
    entry_sps.pack(side=tk.LEFT)
    entry_sps.insert(0, "8")

    ttk.Label(frame_controles, text="Número de taps:").pack(side=tk.LEFT)
    entry_taps = ttk.Entry(frame_controles, width=5)
    entry_taps.pack(side=tk.LEFT)
    entry_taps.insert(0, "101")

    ttk.Button(frame_controles, text="Simular", command=simular).pack(side=tk.RIGHT)

    ventana.mainloop()

if __name__ == "__main__":
    preparar_interfaz()