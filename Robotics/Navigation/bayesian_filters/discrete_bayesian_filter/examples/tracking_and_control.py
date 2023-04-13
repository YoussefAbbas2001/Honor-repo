import numpy as np
import matplotlib.pyplot as plt
import random
plt.style.use("fivethirtyeight")


class Train(object):
    def __init__(self, track_len, kernel=[1.], sensor_accuracy=.9):
        self.track_len = track_len
        self.pos = 0
        self.kernel = kernel
        self.sensor_accuracy = sensor_accuracy

    def move(self, distance=1):
        """ move in the specified direction
        with some small chance of error"""

        self.pos += distance
        # insert random movement error according to kernel
        r = random.random()
        s = 0
        offset = -(len(self.kernel) - 1) / 2
        for k in self.kernel:
            s += k
            if r <= s:
                break
            offset += 1
        self.pos = int((self.pos + offset) % self.track_len)
        return self.pos

    def sense(self):
        pos = self.pos
         # insert random sensor error
        if random.random() > self.sensor_accuracy:
            if random.random() > 0.5:
                pos += 1
            else:
                pos -= 1
        return pos

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

def update(likelhood, prior):
    '''
    Update Step
    get posterior which is the probability after incorporating the measurement
    from prior which is the probability before include the measurement
    using likelihood which is the likely each position was given the measurement
    '''
    posterior = prior * likelhood
    return posterior / sum(posterior)


def plot_belief(positions, belief, show=False):
    # plt.figure(fig)
    plt.bar(positions, belief)
    plt.xticks(positions)
    plt.xlabel("positions")
    if show: plt.show()


def train_filter(track, iterations, kernel, sensor_accuracy, 
             move_distance, do_print=True):
    # track = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    prior = np.array([1] + [0.0]*(len(track)-1))
    posterior = prior[:]
    prior = prior/sum(prior)
    
    robot = Train(len(track), kernel, sensor_accuracy)
    for i in range(iterations):
        # move the robot and
        robot.move(distance=move_distance)

        # peform prediction
        prior = predict(posterior, move_distance, kernel)       

        #  and update the filter
        m = robot.sense()
        likelihood = get_likelihood(track, m, sensor_accuracy)
        posterior = update(likelihood, prior)
        index = np.argmax(posterior)

        if do_print:
            print(f'time {i}: pos {robot.pos}, sensed {m}, at position {track[robot.pos]}')
            conf = posterior[index] * 100
            print(f'        estimated position is {index} with confidence {conf:.4f}%:')            

    
    if do_print:
        print()
        print('final position is', robot.pos)
        index = np.argmax(posterior)
        conf = posterior[index]*100
        print(f'Estimated position is {index} with confidence {conf:.4f}')

    plot_belief(track, posterior, show=False)


random.seed(3)
np.set_printoptions(precision=2, suppress=True, linewidth=60)
track = np.array([0,1,2,3,4,5,6,7,8,9,10])
# train_filter(track,7, kernel=[0.1,0.8,0.1], sensor_accuracy=.7,
#              move_distance=1, do_print=True)

plt.figure(figsize=(12,8))
plt.subplots_adjust(hspace=0.4)
for i in range (4):
    random.seed(3)
    plt.subplot(221+i)
    train_filter(track, 148+i, kernel=[.1, .8, .1], 
                    sensor_accuracy=.8,
                    move_distance=1, do_print=False)
    plt.title (f'iteration {148 + i}')

plt.show()