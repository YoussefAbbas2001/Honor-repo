import matplotlib.pyplot as plt
import numpy as np
plt.style.use("fivethirtyeight")


def update(likelhood, prior):
    '''
    Update Step
    get posterior which is the probability after incorporating the measurement
    from prior which is the probability before include the measurement
    using likelihood which is the likely each position was given the measurement
    '''
    posterior = prior * likelhood
    return posterior / sum(posterior)

def perfect_predict(belief, move):
    """ move the position by `move` spaces, where positive is 
    to the right, and negative is to the left
    """
    n = len(belief)
    result = np.zeros(n)
    for i in range(n):
        result[i] = belief[(i-move) % n]
    return result

def predict_diff(belief, move, p_correct,  p_over, p_under):
    n = len(belief)
    result = np.zeros(n)
    for i in range(n):
        result[i] = belief[(i-move) % n]*p_correct + belief[(i-move-1) % n]*p_over + belief[(i-move+1) % n]*p_under
    return result

def predict(pdf, offset, kernel):
    N = len(pdf)
    kN = len(kernel)
    width = int((kN - 1) / 2)

    prior = np.zeros(N)
    for i in range(N):
        for k in range (kN):
            index = (i + (width-k) - offset) % N
            prior[i] += pdf[index] * kernel[k]
    return prior


def get_likelihood(hall,  z, z_prob):
    '''
    Compute likelihood
    '''
    try:
        correct_scale = z_prob/(1-z_prob)
    except ZeroDivisionError:
        correct_scale = 1e8
    likelihood = np.ones(len(hall))
    likelihood[hall==z] *= correct_scale
    return likelihood

def plot_belief(positions, belief,fig, title, show=False):
    plt.figure(fig)
    plt.bar(positions, belief)
    plt.title(title)
    plt.xticks(positions)
    plt.xlabel("positions")
    if show: plt.show()

if __name__ == "__main__":
    positions = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    hallway = np.array([1, 1, 0, 0, 0, 0, 0, 0, 1, 0])
    prior   = np.array([0.1]*10)
    reading = 1    # Door open
    pz      = 0.99
    likelihood = get_likelihood(hallway, reading, pz )
    posterior  = update(likelihood, prior)

    print(posterior)
    plot_belief(positions, posterior, 0,"Belief Distribution")

    # Perfect Prediction
    # belief = perfect_predict(posterior, 1)
    belief = predict_diff(posterior, 4, p_correct=0.8, p_under=0.1, p_over=0.1)
    plot_belief(positions, belief, 1,title="Perfect Prediction")


    belief = predict([0.1, 0.8, 0.05, 0.03,0.02,0,0,0,0,0], offset=3, kernel=[0.15, 0.8, 0.05])
    plot_belief(positions, belief, 2,title="Convolution Prediction")
    print(belief)

    plt.show()
