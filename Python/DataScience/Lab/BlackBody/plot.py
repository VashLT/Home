import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

fig, ax = plt.subplots(figsize=(4, 4))
wavelength = np.array([
    0.483, 0.580, 0.644, 0.724, 0.828, 0.966, 1.159, 1.449, 2.898
])
wavelength = np.array([i * 1000 for i in wavelength])
data = [i * 1000 for i in range(1, 7)]
data.reverse()
temperature = np.array(data)
wl_smooth = gaussian_filter1d(wavelength, sigma=2)
# t_smooth = gaussian_filter1d(np.array(data), sigma=2)

x0 = np.linspace(0, 9, len(wavelength))
x1 = np.linspace(0, 9, len(data))
plt.plot(x0, wl_smooth, color='#8EDB4D', label='Longitud de onda [$n$m]')
plt.plot(x1, temperature, color='#4DBDDB', label='Temperatura [$K$]')
ax.set_xticklabels([])
ax.set_xticks([])
plt.legend(loc='upper center')
plt.show()
