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

def predict(pos, movement):
    return gaussian(pos.mean + movement.mean, pos.var + movement.var)

pos  = gaussian(10, 0.2)
move = gaussian(15, 0.7)
prior= predict(pos, move)

print(prior.__repr__())


dpos   = stats.norm(loc=pos.mean, scale=pos.var)
dmove  = stats.norm(loc=move.mean, scale=move.var)
dprior = stats.norm(loc=prior.mean, scale=prior.var)
x      = np.linspace(0,prior.mean *2, N)
y_pos  = dpos.pdf(x)
y_move = dmove.pdf(x)
y_prior= dprior.pdf(x)


plt.figure(figsize=(16,9))
plt.plot(x, y_pos, linestyle='--', linewidth=1.5, label=f'Pos : {pos}')
plt.plot(x, y_move, linestyle='--',  linewidth=1.5,label=f'Move:{move}')
plt.plot(x, y_prior, linewidth=1.5, label=f'prior: {prior}')
plt.title('Position Distribution')
plt.xlabel('Position')
plt.ylabel('Probability')
plt.legend()
plt.show()