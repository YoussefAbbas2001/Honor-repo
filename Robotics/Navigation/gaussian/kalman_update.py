from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt 
from  scipy import stats
plt.style.use('fivethirtyeight')
# plt.rc('text', usetex=True)
# plt.rc('font', family='serif')

N = 500     # Number of samples in time  base vector
gaussian = namedtuple('Gaussian', ['mean', 'var'])
gaussian.__repr__  = lambda s: f'𝒩(μ={s[0]:.3f}, 𝜎²={s[1]:.3f})'
gaussian.__str__   = lambda s: f'N(mean={s[0]:.3f}, var={s[1]:.3f})'

def gaussian_multiply(g1, g2):
    mean = (g1.var * g2.mean + g2.var * g1.mean) / (g1.var + g2.var)
    variance = (g1.var * g2.var) / (g1.var + g2.var)
    return gaussian(mean, variance)

def update(prior, likelihood):
    posterior = gaussian_multiply(likelihood, prior)
    return posterior

# test the update function
prior      = gaussian(10., 1**2)
likelihood = gaussian(11., 1**2)
estimated  = update(prior, likelihood)
print(estimated.__repr__())

dprior = stats.norm(loc=prior.mean, scale=prior.var)
dlikelihood  = stats.norm(loc=likelihood.mean, scale=likelihood.var)
destimated = stats.norm(loc=estimated.mean, scale=estimated.var)
x      = np.linspace(0,estimated.mean *2, N)
y_prior  = dprior.pdf(x)
y_likelihood = dlikelihood.pdf(x)
y_estimated= destimated.pdf(x)


plt.figure(figsize=(16,9))
plt.plot(x, y_prior, linestyle='--', linewidth=1.5, label=f'Prior : {prior}')
plt.plot(x, y_likelihood, linestyle='--',  linewidth=1.5,label=f'Likelihood:{likelihood}')
plt.plot(x, y_estimated, linewidth=1.5, label=f'Estimated: {estimated}')
plt.title('Update Distributions')
plt.xlabel('Position')
plt.ylabel('Probability')
plt.legend()
plt.show()
