import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
import itertools as it


def old():
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


h = 6.626e-34
c = 3.0e+8
k = 1.38e-23
kb = 2.898e-3


def main():
    # see https://stackoverflow.com/questions/22417484/plancks-formula-for-blackbody-spectrum
    # styles
    plt.style.use('dark_background')
    plt.tight_layout()

    wavelengths = np.arange(1e-9, 4e-6, 1e-9)
    discrete_wl = np.arange(1e-9, 4e-6, 1e-9)

    fig, ax = plt.subplots(figsize=(10, 10))

    temperatures = [2000, 2400, 2800, 3200, 3600, 4000, 4300]
    colors = it.cycle(["#D04040", "#E29043", "#D08E40",
                       "#E2DF43", "#7AE243", "#43E2B4", "#43D7E2"])
    for T in temperatures:
        color = next(colors)
        label = f"$T = {str(T)}_K$"
        intensities = planck(wavelengths, T)
        plt.plot(wavelengths * 1e9, intensities, color=color, label=label)
        ymax = max(intensities)
        xpos = list(intensities).index(ymax)
        xmax = wavelengths[xpos] * 1e9
        print(f"[{xmax},{ymax}]")
        plt.plot(xmax, ymax, marker='o', color='w')

    # boltzmann_law = boltzmann(wavelengths * 1e9)
    # plt.plot(wavelengths * 1e9, boltzmann_law, linestyle='--', color='r')

    # plt.plot(wavelengths * 1e9, intensity5000, color='#3AA0CD',
    #          label='Curva experimental')  # 5000K green line
    # plt.plot(discrete_wl * 1e9, i5000, ls='--', color='#3ACD6F',
    #          label='Predicción clásica')  # 5000K green line
    plt.ylim(bottom=0, top=5*1e12)
    plt.xlim(left=0, right=4000)

    ax.set_xlabel('$\lambda [nm]$')
    ax.set_ylabel(
        'Intensidad $[ \\frac{W}{m^2\\cdot nm\\cdot sr}]$')
    plt.legend(loc='upper right')

    # show the plot
    plt.show()


def boltzmann(wl):
    #wl: wavelength
    cc = 130488154099.18523 * 1451.0000000000002
    dx = 800
    T = cc / (wl-dx)
    return T


def planck(wav, T):
    a = 2.0*h*c**2
    b = h*c/(wav*k*T)
    intensity = a / ((wav**5) * (np.exp(b) - 1.0))
    return intensity


def rayleigh(wav, T):
    a = 2 * c / (wav ** 4)
    b = k * T
    intensity = a * b
    return intensity


if __name__ == "__main__":
    main()
