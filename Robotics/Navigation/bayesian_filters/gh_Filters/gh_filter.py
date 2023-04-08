import matplotlib.pyplot as plt
import numpy as np
plt.style.use("fivethirtyeight")



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

def gen_data(x0, dx, count, noise_factor, accel=0.):
    zs = []
    for i in range(count):
        zs.append(x0 + accel * (i**2) / 2 + dx*i + np.random.randn()*noise_factor)
        dx += accel
    return zs

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

def vary_filter_parameters(weights, g_list, h_list, title='gh Filter', xlabel='Time (day)', ylabel='weights (lb)'):
    time_vector = np.arange(0,len(weights),1)
    plt.figure(figsize=(16,9))
    plt.scatter(time_vector,weights,color='green', marker='x', label='Weights')
    for gs in g_list:
        for hs in h_list:
            estimated, predicted = g_h_filter(data=noisy_weights, x0=90., dx=0.2, g=gs, h=hs, dt=1.)
            plt.plot(time_vector, estimated[1:],linewidth=1, label=f'g:{float(gs):.2}, h:{float(hs):.2}')

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

# weights = [158.0, 164.2, 160.3, 159.9, 162.1, 164.6, 
#            169.6, 167.4, 166.4, 171.0, 171.2, 172.6]

noisy_weights = gen_data(80, 0.1, 20, 100, accel=0)
estimated, predicted = g_h_filter(data=noisy_weights, x0=90., dx=0.2, g=0.6, h=0.06, dt=1.)


# filter_plotting( estimated, predicted, noisy_weights, 'gh Filter', 'Time (day)', 'weights (lb)')
vary_filter_parameters(weights=noisy_weights, g_list=[0.5],h_list=[0,0.5,1])