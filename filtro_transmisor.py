import numpy as np
import matplotlib.pyplot as plt

# ====================
#  Generación de g[n]
# ====================

fB = 32e9    # Velocidad de simbolos (baud rate)
# Es la frecuencia de los simbolos, 32 GBaudios

T = 1 / fB   # Tiempo entre símbolos
M = 8        # Factor de sobremuestreo
fs = fB * M  # Sample rate

alpha = 0.1  # Factor de roll-off
L = 20       # ( 2 * L * M + 1 ) es el largo del filtro sobremuestreado

t = np.arange( -L, L, 1 / M ) * T

gn = np.sinc( t / T ) * np.cos( np.pi * alpha * t / T ) / ( 1 - 4 * alpha**2 * t**2 / T**2 )

params = { 'legend.fontsize': 'large',
           'figure.figsize': ( 15, 6 ),
           'axes.labelsize': 20,
           'axes.titlesize': 20,
           'xtick.labelsize': 15,
           'ytick.labelsize': 15,
           'axes.titlepad': 30 }
plt.rcParams.update( params )

fig, ax = plt.subplots()

x1_ejeVertical, y1_ejeVertical = [ 0, 0 ], [ 0, 1.5 ]
ax.plot( x1_ejeVertical, y1_ejeVertical, linewidth = 2.5, color = 'black' )
ax.scatter( x1_ejeVertical[ 1 ], y1_ejeVertical[ 1 ], marker = "^", color = 'black', s = 150 )

x1_ejeHorizontal, y1_ejeHorizontal = [ -5*T, 4.9*T ], [ 0, 0 ]
ax.plot( x1_ejeHorizontal, y1_ejeHorizontal, linewidth = 2.5, color = 'black' )

ax.stem( t, gn )
ax.set_title( 'Filtro transmisor' )

plt.text( T/6, 1.45, r'$g_{[n]}$', fontsize = 25, color = 'black' )
plt.text( 5.2*T, 0, r'$n$', fontsize = 25, color = 'black' )

abcisas = [ -5*T, -4*T, -3*T, -2*T, -T, 0, T/2, T, 2*T, 3*T, 4*T, 5*T ]
textos_abcisas = [ '-5T', '-4T', r'$-3T$', '-2T', '-T', '0', r'$\frac{1}{2} \ T$', 'T', '2T', '3T', '4T', '5T' ]
plt.xticks( abcisas, textos_abcisas )
ordenadas = [ 0, 1 ]
textos_ordenadas = [ '0', '1' ]
plt.yticks( ordenadas, textos_ordenadas )

plt.xlim( [ -5*T, 5*T ] )

plt.show()
