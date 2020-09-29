# -*- coding: utf-8 -*-
"""AudioPython2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1in9tFZoSncg6NCyK-Y6VdC2XhRxQzpK8

# ESPECTROGRAMAS


---
"""

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
# %matplotlib inline

import seaborn
import os
seaborn.set(style='ticks')

from IPython.display import Audio

import numpy as np 
import scipy

import librosa
import librosa.display

"""Carga el audio como una forma de onda en **y**,

Almacena la frecuencia de muestreo en **sr** (Hz)
"""

# y, sr = librosa.load('Guitarra-1.wav')
# y, sr = librosa.load('A-C#-E.wav')
y, sr = librosa.load('Violin_G4_G5.wav')
# y, sr = librosa.load('noise.wav')
# y, sr = librosa.load('A-C#-E.wav')



#from google.colab import drive
#drive.mount('/content/drive')

"""Duracion del audio en segundos"""

y.shape[0] / sr/2

"""Puedes probar el audio cargado, y comprobar la duración"""

Audio(data=y, rate=sr)

"""Se plotea la señal"""
plt.style.use('dark_background')

plt.tight_layout()

librosa.display.waveplot(y, sr, max_sr = 6000, label= 'acorde A-C#-E', color = 'y')


plt.xlim(left = 1.35, right = 1.38)
plt.grid(True)
plt.legend()
plt.title('Señal de audio en el dominio del tiempo')
plt.show()







