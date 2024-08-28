import numpy as np
from random import randrange, seed
import datetime
import matplotlib.pyplot as plt

# ====================
#  Generación de g[n]
# ====================

fB = 32e9    # Velocidad de simbolos (baud rate)
# Es la frecuencia de los simbolos, 32 GBaudios

T = 1 / fB   # Tiempo entre símbolos
M = 8        # Factor de sobremuestreo
fs = fB * M  # Sample rate

alpha = 0.3  # Factor de roll-off
L = 20       # ( 2 * L * M + 1 ) es el largo del filtro sobremuestreado

t = np.arange( -L, L, 1 / M ) * T

gn = np.sinc( t / T ) * np.cos( np.pi * alpha * t / T ) / ( 1 - 4 * alpha**2 * t**2 / T**2 )

segundos_desde_1970 = int( datetime.datetime.now().timestamp() )

print( 'Pasaron', segundos_desde_1970, 'segundos desde el 1ero de enero de 1970' )
seed( segundos_desde_1970 )

cantidad_simbolos = 1000
simbolos_PAM2 = np.empty( cantidad_simbolos )

for i in range( cantidad_simbolos ) :
    simbolos_PAM2[ i ] = randrange( -3, 4, 2 )

print( '\nUna muestra de los símbolos generados:\n', simbolos_PAM2[ 0 : 50 ] )

xn = np.zeros( cantidad_simbolos * M )

for i in range( cantidad_simbolos ) :
    xn[ i * M ] = simbolos_PAM2[ i ]

params = { 'legend.fontsize': 'large',
           'figure.figsize': ( 12, 6 ),
           'axes.labelsize': 20,
           'axes.titlesize': 20,
           'xtick.labelsize': 15,
           'ytick.labelsize': 15,
           'axes.titlepad': 30 }
plt.rcParams.update( params )

fig, ax = plt.subplots()

cuantos_chupetines = 60
ax.stem( np.arange( 0, cuantos_chupetines ), xn[ 0 : cuantos_chupetines ] )

plt.show()

from scipy.signal import convolve

sn = convolve( xn, gn )

fig, ax = plt.subplots()

cuantos_chupetines = 1600
ax.plot( np.arange( 1000, cuantos_chupetines ), sn[ 1000 : cuantos_chupetines ] )
# ax.stem( np.arange( 1000, cuantos_chupetines ), sn[ 1000 : cuantos_chupetines ] )

plt.show()

d = 4;  # Delay para centrar el ojo

for i in range( 2 * L + 1, cantidad_simbolos - ( 2 * L + 1 ) ) :
    sn_p = sn[ i * M + d : i * M + d + M ]
    plt.plot( np.arange( -3, 4 ), sn_p[ 1 : 8 ] )

plt.show()


