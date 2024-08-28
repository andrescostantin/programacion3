import matplotlib.pyplot as plt
import numpy as np

# Crear un array de valores n
n = np.arange(-40, 41, 1)

# Definir la señal usando una combinación de una senoidal y una función gaussiana
y = np.sin(n / 2) * np.exp(-0.1 * n**2 / 10)

# Crear la gráfica
plt.stem(n, y)
plt.axhline(0, color='red', linewidth=0.5)

# Añadir títulos y etiquetas
plt.title('Secuencia Replicada')
plt.xlabel('n')
plt.ylabel('Amplitud')

# Mostrar la gráfica
plt.grid(True)
plt.show()