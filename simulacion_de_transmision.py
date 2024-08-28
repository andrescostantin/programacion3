def preparar_mensaje():
    mensaje = "Hola, esta es una simulación de transmisión de datos."
    print("Mensaje original:", mensaje)
    return mensaje

def fragmentar_mensaje(mensaje, tamaño_segmento=20):
    # Fragmenta el mensaje en segmentos de tamaño fijo
    segmentos = [mensaje[i:i+tamaño_segmento] for i in range(0, len(mensaje), tamaño_segmento)]
    print("\nFragmentos de mensaje (Capa de Transporte):")
    for i, segmento in enumerate(segmentos):
        print(f"Segmento {i+1}: '{segmento}'")
    return segmentos

def encapsular_ip(segmentos):
    paquetes = []
    print("\nEncapsulamiento en paquetes IP (Capa de Red):")
    for i, segmento in enumerate(segmentos):
        paquete = f"IP_Header_{i+1} | {segmento}"
        paquetes.append(paquete)
        print(f"Paquete IP {i+1}: '{paquete}'")
    return paquetes

def generar_senal_4D_PAM5(paquetes):
    # Usamos niveles -2, -1, 0, 1, 2 para PAM5
    niveles_PAM5 = [-2, -1, 0, 1, 2]
    señales = []
    print("\nGeneración de señal 4D-PAM5 (Capa de Enlace de Datos):")
    
    for paquete in paquetes:
        señal = np.random.choice(niveles_PAM5, size=(len(paquete), 4))  # 4 dimensiones
        señales.append(señal)
        print(f"Señal para '{paquete}':\n{señal}")
    
    return señales

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

def aplicar_filtro_4D(signales, filtro):
    señales_filtradas = []
    print("\nAplicación del filtro (Capa Física):")
    
    for señal in señales:
        señal_filtrada = np.array([np.convolve(dim, filtro, mode='same') for dim in señal.T]).T
        señales_filtradas.append(señal_filtrada)
        print(f"Señal filtrada:\n{señal_filtrada}")
    
    return señales_filtradas

import matplotlib.pyplot as plt
import numpy as np

def graficar_señales(señales, señales_filtradas):
    fig, axes = plt.subplots(len(señales), 2, figsize=(10, len(señales) * 3))
    
    for i, (señal, señal_filtrada) in enumerate(zip(señales, señales_filtradas)):
        ax1, ax2 = axes[i]
        for dim in range(4):  # 4 dimensiones para 4D-PAM5
            ax1.plot(señal[:, dim], label=f'Canal {dim+1}')
            ax2.plot(señal_filtrada[:, dim], label=f'Canal {dim+1}')
        
        ax1.set_title(f'Señal Original {i+1}')
        ax1.legend()
        ax1.grid()
        ax2.set_title(f'Señal Filtrada {i+1}')
        ax2.legend()
        ax2.grid()
    
    plt.tight_layout()
    plt.show()

# Simulación completa
mensaje = preparar_mensaje()
segmentos = fragmentar_mensaje(mensaje)
paquetes = encapsular_ip(segmentos)
señales = generar_senal_4D_PAM5(paquetes)

# Parámetros del filtro
beta = 0.25
sps = 8
num_taps = 101
filtro = filtro_coseno_alzado(beta, sps, num_taps)
señales_filtradas = aplicar_filtro_4D(señales, filtro)

# Graficar señales
graficar_señales(señales, señales_filtradas)