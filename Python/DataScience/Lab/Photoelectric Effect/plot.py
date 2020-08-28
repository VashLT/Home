import matplotlib.pyplot as plt
import numpy as np
import itertools as it


def current_intensity_plot():
    intensity = np.array([0] + [i/100 for i in np.arange(20, 110, 10)])
    current = np.array([0, 0.016, 0.024, 0.032, 0.04,
                        0.048, 0.056, 0.064, 0.072, 0.08])
    # print(intensity)

    fig, ax = plt.subplots(figsize=(6, 6))
    plt.plot(intensity, current, color='#3E185B',
             label='$\lambda = 350 [nm]$')
    plt.legend(loc='upper center')
    plt.title(label='Corriente [A] vs intensidad [%]')
    plt.show()


def column_plot():
    energies = np.array([
        3.68e-19, 6.93e-19, 7.59e-19, 1.01e-18, 4.68e-19
    ])
    wavelength = np.array([540, 287, 262, 196, 425])
    fig, ax = plt.subplots(figsize=(6, 6))

    labels = it.cycle(['Na', 'Zn', 'Cu', 'Pt', 'Ca'])
    colors = it.cycle(['#2EC968', '#3B1085', '#3C2A59', '#1B1427', '#5024DF'])
    for index, x in enumerate(wavelength):
        name = next(labels)
        color = next(colors)
        plt.bar(x, energies[index], width=20,
                color=color, align='center', label=name)

    plt.legend(loc='upper center')
    plt.ylim(top=1.02e-18) , plt.xlim(left=160, right=550)
    plt.xlabel('Longitud de onda [nm]'), plt.ylabel('Energía umbral [J]')
    plt.show()


def main():
    column_plot()


if __name__ == '__main__':
    main()
