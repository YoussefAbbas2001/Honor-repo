import matplotlib.pyplot as plt
import numpy as np

weights = [158.0, 164.2, 160.3, 159.9, 162.1, 164.6, 
           169.6, 167.4, 166.4, 171.0, 171.2, 172.6]

time_step = 1.0        # day



def predict_using_gain_guess(estimated_weight, gain_rate, weight_rate ,do_print=False):         
    gain = 0          # Initial gain Used

    # storage for the filtered results
    estimates, gains,  predictions = [estimated_weight], [], []


    # most filter literature uses 'z' for measurements
    for z in weights: 
        # predict new position
        predicted_weight = estimated_weight + gain * time_step

        # Compute Gain 
        gain = gain + gain_rate * (z - predicted_weight)

        # update filter 
        estimated_weight = predicted_weight + weight_rate * (z - predicted_weight)

        print(f'gain : {gain}')
        print(f'gain rate : {gain_rate}')

        # save and log
        estimates.append(estimated_weight)
        predictions.append(predicted_weight)
        gains.append(gain)

        if do_print:
            print(f'measurement: {z:.4}, prediction: {predicted_weight:.4}, estimate: {estimated_weight:.4}')

    return estimates, predictions

def filter_plotting(estimates, predictions, weights):
    time_vector = np.arange(0,len(predictions),1)
    plt.figure(figsize=(16,9))
    plt.plot(estimates[1:], color='blue', marker='o', label='Estimated')
    plt.plot(predictions, color='red', marker='s', label='Predicted')
    plt.plot(weights,color='green', marker='x', label='Weights')
    plt.legend()
    plt.show()

gain_rate = 0.05           # gain rate 
weight_rate = 0.5          # weight rate
initial_estimate = 200.
estimates, predictions = predict_using_gain_guess(
    estimated_weight=initial_estimate, gain_rate=gain_rate, weight_rate=weight_rate, do_print=True)     


filter_plotting(estimates=estimates, predictions=predictions, weights=weights)