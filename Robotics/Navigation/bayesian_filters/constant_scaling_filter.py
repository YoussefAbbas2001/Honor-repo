# from kf_book.book_plots import figsize
import matplotlib.pyplot as plt
import numpy as np

weights = [158.0, 164.2, 160.3, 159.9, 162.1, 164.6, 
           169.6, 167.4, 166.4, 171.0, 171.2, 172.6]

time_step = 1.0        # day
scale_factor = 0.4 

def predict_using_gain_guess(estimated_weight, gain_rate, do_print=False):     
    # storage for the filtered results
    estimates, predictions = [estimated_weight], []

    # most filter literature uses 'z' for measurements
    for z in weights: 
        # predict new position
        predicted_weight = estimated_weight + gain_rate * time_step

        # update filter 
        estimated_weight = predicted_weight + scale_factor * (z - predicted_weight)

        # save and log
        estimates.append(estimated_weight)
        predictions.append(predicted_weight)
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

initial_estimate = 200.
estimates, predictions = predict_using_gain_guess(
    estimated_weight=initial_estimate, gain_rate=1, do_print=True)     


filter_plotting(estimates=estimates, predictions=predictions, weights=weights)