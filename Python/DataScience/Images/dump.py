import matplotlib.pyplot as plt
import numpy as np


sample_domain = np.linspace(0, 10, num=100)
outputs = np.exp(sample_domain)

plt.plot(sample_domain, outputs, alpha=.5, animated=True)
plt.show()
