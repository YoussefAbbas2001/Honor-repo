import matplotlib.pyplot as plt
import numpy as np
plt.style.use("fivethirtyeight")

weights = [158.0, 164.2, 160.3, 159.9, 162.1, 164.6, 
           169.6, 167.4, 166.4, 171.0, 171.2, 172.6]

def g_h_filter(data, x0, dx, g, h, dt=1.):
    x_est       = x0
    results     = [x0]
    predictions = []

    for z in data:
        # prediction step
        x_pred = x_est + (dx*dt)
        dx = dx

        # update step
        residual = z - x_pred
        dx = dx + h * (residual) / dt
        x_est = x_pred + g * residual

        results.append(x_est)
        predictions.append(x_pred)
    return results, predictions

def filter_plotting(estimates, predictions, weights, title, xlabel, ylabel):
    time_vector = np.arange(0,len(predictions),1)
    plt.figure(figsize=(16,9))
    plt.title(title)
    plt.plot(time_vector,estimates[1:], color='blue', marker='o', label='Estimated')
    plt.plot(time_vector,predictions, color='red', marker='s',linestyle='--', linewidth=1, label='Predicted')
    plt.scatter(time_vector,weights,color='green', marker='x', label='Weights')
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


estimated, predicted = g_h_filter(data=weights, x0=160., dx=0.2, g=6./10, h=0.2, dt=1.)

filter_plotting( estimated, predicted, weights, 'gh Filter', 'Time (day)', 'weights (lb)')
