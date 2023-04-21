import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

mean = 10
variance = 5
gaussian = stats.norm(loc = mean, scale= variance)

x = np.linspace(0, 20, 100)
y = gaussian.pdf(x)


plt.figure(figsize=(16,9))
plt.plot(x,y)
plt.show()