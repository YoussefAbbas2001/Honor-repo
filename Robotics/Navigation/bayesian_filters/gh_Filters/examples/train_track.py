import numpy as np
import matplotlib.pyplot as plt

def compute_new_position(pos, vel, dt=1.):
    """ dt is the time delta in seconds."""
    return pos + (vel * dt)

def measure_position(pos):
    return pos + np.random.randn()*500

def gen_train_data(pos, vel, count, acc=2):
    zs = []
    for t in range(count):
        pos = compute_new_position(pos, vel)
        vel += 2
        zs.append(measure_position(pos))
    return np.asarray(zs)

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

pos, vel = 23.*1000, 15.
zs = gen_train_data(pos, vel, 100, 10)
estimated, predicted = g_h_filter(zs, pos, vel, g=0.01, h=0.001, dt=1)
filter_plotting( estimated, predicted, zs, 'gh Filter', 'Time (day)', 'Position (lb)')
