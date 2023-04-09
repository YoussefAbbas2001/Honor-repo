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

def plot_belief(positions, belief):
    plt.bar(positions, belief)
    plt.title("Belief Distribution")
    plt.xticks(positions)
    plt.xlabel("positions")
    plt.show()

positions = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
hallway = np.array([1, 1, 0, 0, 0, 0, 0, 0, 1, 0])
prior   = np.array([0.1]*10)
reading = 1    # Door open
pz      = 0.99
likelihood = get_likelihood(hallway, reading, pz )
posterior  = update(likelihood, prior)

print(posterior)
plot_belief(positions, posterior)