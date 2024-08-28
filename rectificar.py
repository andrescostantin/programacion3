import matplotlib.pyplot as plt
import numpy as np

# Gráfico 1: Secuencia y = cos(n) modificando a cero los valores negativos

# Crear un array de valores n desde 0 hasta 49
n = np.arange(0, 50, 1)

# Definir la señal discreta y = cos(n)
y_cos = np.cos(n)

# Modificar los valores menores a cero a cero
y_cos = np.array([0 if val < 0 else val for val in y_cos])

# Gráfico 2: Secuencia senoidal con 12 muestras por ciclo

# Crear un array de valores n para un ciclo completo
n_sine = np.arange(0, 12, 1)

# Definir la señal discreta y = sin(2*pi*n/12) para un ciclo
y_sine = np.sin(2 * np.pi * n_sine / 12)

# Repetir el ciclo para tener al menos 50 muestras
y_sine = np.tile(y_sine, 5)

# Crear la figura y los ejes para dos subgráficas
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

# Gráfica de la primera señal
ax1.stem(n, y_cos)
ax1.set_title('Señal Discreta y = cos(n) con valores negativos modificados a cero')
ax1.set_xlabel('n')
ax1.set_ylabel('y')
ax1.grid(True)

# Gráfica de la segunda señal
ax2.stem(n[:50], y_sine[:50])  # Asegurar que solo graficamos los primeros 50 valores
ax2.set_title('Señal Senoidal con 12 muestras por ciclo')
ax2.set_xlabel('n')
ax2.set_ylabel('y')
ax2.grid(True)

# Ajustar el espaciado entre las subgráficas
plt.tight_layout()

# Mostrar la gráfica
plt.show()