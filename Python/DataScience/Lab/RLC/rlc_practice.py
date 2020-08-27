import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d
import numpy as np
import csv
import os


SAMPLES = 300


def read_csv_data(path):
    if not path.endswith('.csv'):
        raise Exception("A csv file is expected.")
        return
    parse_path = os.path.join(os.getcwd(), path)

    data = np.genfromtxt(parse_path, delimiter=',')
    return data


def overlap_frequencies(files):
    folder = r'Lab\\'
    ext = '.csv'

    # create canvas
    fig, ax = plt.subplots(figsize=(10, 10))

    name1 = files[0][4:].replace('hz', ' Hz')
    name2 = files[1][4:].replace('hz', ' Hz')
    name3 = files[2][4:].replace('hz', ' Hz')
    name4 = files[3][4:].replace('hz', ' Hz')
    name5 = files[4][4:].replace('hz', ' Hz')

    data1 = read_csv_data(folder + files[0] + ext)
    data2 = read_csv_data(folder + files[1] + ext)
    data3 = read_csv_data(folder + files[2] + ext)
    data4 = read_csv_data(folder + files[3] + ext)
    data5 = read_csv_data(folder + files[4] + ext)

    plt.plot(data1[:SAMPLES, 0], data1[:SAMPLES, 1], '--',
             color='#448ABD', label=name1, alpha=0.6)
    plt.plot(data2[:SAMPLES, 0], data2[:SAMPLES, 1], '#FF6F6A', label=name2)
    plt.plot(data3[:SAMPLES, 0], data3[:SAMPLES, 1], '--',
             color='#E6C42D', label=name3, alpha=0.6)
    plt.plot(data4[:SAMPLES, 0], data4[:SAMPLES, 1], '--',
             color='#A04FF9', label=name4, alpha=0.6)
    plt.plot(data5[:SAMPLES, 0], data5[:SAMPLES, 1], '--',
             color='#4FF9DF', label=name5, alpha=0.6)

    # increase axes range
    plt.ylim(top=0.03, bottom=-0.03)
    plt.xlim()
    plt.xlim(left=0.01, right=0.03)

    ax.legend(frameon=False, loc='lower center', ncol=8)
    # ax.axis('equal')
    ax.set_xlabel('time [s]')
    ax.set_ylabel('Current Amplitude [mA]')
    # plt.xticks(np.arange(0,0.5, 0.1))

    plt.show()


def impedance_plot():
    data = []
    fig, ax = plt.subplots(figsize=(10, 10))
    current = np.array([3.4469, 4.3049, 5.2610, 6.4027, 7.7114,
                        9.2484, 11.0950, 13.2450, 15.5940, 17.8750, 17.8070,
                        16.1130, 14.6040, 13.1770, 12.0110, 10.9660, 10.0950, 9.3771, 8.7427,
                        8.1825])
    impedance = np.array([
        290.1158,
        232.2934,
        190.0779,
        156.1841,
        129.6781,
        108.1268,
        90.1307,
        75.5002,
        64.1272,
        55.9441,
        56.1577,
        62.0617,
        68.4744,
        75.8898,
        83.2570,
        91.1910,
        99.0589,
        106.6428,
        114.3811,
        122.2120
    ])
    smoothed_impedance = gaussian_filter1d(impedance, sigma=2)
    smoothed_current = gaussian_filter1d(current, sigma=2)

    x = np.linspace(0, 8, len(current))
    x_i = np.linspace(0, 8, len(impedance))

    plt.plot(x, smoothed_current, color='#F46941',
             label='Corriente [mA]', alpha=1)
    # plt.plot(x_i, impedance, '--', color='#F46941', label='Corriente [mA]', alpha=0.5)
    plt.plot(x_i, smoothed_impedance, color='#4196D8',
             label='Impedancia [Ω]', alpha=1)
    plt.ylim(top=260, bottom=0)
    ax.set_xticklabels([])
    ax.set_xticks([])
    plt.legend(loc='upper center')
    plt.show()


def main():
    files = [r"rlc_90hz", 'rlc_160hz', 'rlc_200hz', 'rlc_60hz', 'rlc_270hz']
    # overlap_frequencies(files)
    impedance_plot()


if __name__ == "__main__":
    main()
