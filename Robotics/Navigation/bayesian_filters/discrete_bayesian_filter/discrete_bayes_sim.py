import numpy as np
import matplotlib.pyplot as plt


from discrete_bayes import predict, get_likelihood, update, plot_belief


def discrete_bayes_sim(prior, kernel, measurements, z_prob, hallway):
    posterior = np.array([.1]*10)
    priors, posteriors = [], []
    for i, z in enumerate(measurements):
        prior = predict(posterior, 1, kernel)
        priors.append(prior)

        likelihood = get_likelihood(hallway, z, z_prob)
        posterior = update(likelihood, prior)
        posteriors.append(posterior)
    return priors, posteriors


def plot_state(postition, prior, posterior):
    fig, ax = plt.subplots(1,2, figsize=(18,9))
    ax[0].bar(positions, prior)
    ax[0].set_title("Prior")
    ax[0].set_xlabel("Position")
    ax[0].set_ylabel("Probability")
    ax[0].set_ylim([0, 1])
    
    ax[1].bar(positions, posterior)
    ax[1].set_title("Posterior")
    ax[1].set_xlabel("Position")
    ax[1].set_ylabel("Probability")
    ax[1].set_ylim([0, 1])

def plot_evolution( positions, posteriors):
    n = len(posteriors) 
    fig , ax = plt.subplots((n+1)//2, 2, figsize=(12, n*3))
    plt.subplots_adjust(hspace=0.4)
    for i in range((n+1)//2):
        for j in range(2):
            if 2*i+j ==  n: break
            ax[i, j].bar(positions, posteriors[2*i+j])
            ax[i, j].set_title(f'Step {2*i+j+1}')
            ax[i, j].set_ylim([0, 1])
            ax[i, j].set_xticks(positions)


if __name__ == '__main__':
    # change these numbers to alter the simulation
    kernel = (.1, .8, .1)
    prior   = np.array([0.1]*10)
    z_prob = 1.0
    hallway = np.array([1, 1, 0, 0, 0, 0, 0, 0, 1, 0])
    positions = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])


    # measurements with no noise
    # zs = [hallway[i % len(hallway)] for i in range(50)]
    zs = [1, 0, 1, 1, 1]

    priors, posteriors = discrete_bayes_sim(prior, kernel, zs, z_prob, hallway)
    plot_state(positions, prior, posteriors[-1])
    plot_evolution(positions, posteriors)
    print(f'prior     : {prior}')
    print(f'posterior : {posteriors[-1]}')

    plt.show()