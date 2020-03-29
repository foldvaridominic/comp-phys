import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

# Define a function responsible for generating
# a sequence of random numbers.
def lcg(seed=1, a=1229, c=1, mod=2048):
    seed = float(seed)
    a = float(a)
    c = float(c)
    mod = float(mod)
    rand_nums = []
    for i in range(3000):
        seed = (a * seed + c) % mod
        rand_nums.append(seed / mod)

# Split the sequence into 3 parts
# to plot the random numbers inside a cube in 3D.
    x = []
    y = []
    z = []
    for i in range(1000):
        x.append(rand_nums[i*3])
        y.append(rand_nums[i*3+1])
        z.append(rand_nums[i*3+2])

# Bad property: check for Marsaglia effect, i.e. whether unpopulated hyperplanes occur.
# Good property: distribution (histogram)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z)
    plt.show()
    plt.hist(rand_nums, bins=np.arange(0,1,0.1))
    plt.show()

def random_generator():
# II. Generate random numbers with triangular distribution
# PDF: P(x) = 2x = 2 (x-a) / ((b-a)(c-a)) = D'(x) --> b=1, c=1, 0<=x<=1
# CDF: D(x) = x^2, 0<=x<=1
# Inverse of CDF = D^(-1) (x) = sqrt((D(b) - D(a)) * x) = sqrt(x)
    p = [0 for i in range(1001)]
    for i in range(1,1000001):
        x = np.random.random()
        y = math.sqrt(x)
        y = int(round(y, 3) * 1000)
        p[y] += 1000

    p = [float(pp)/1000000 for pp in p]
    xs = [0.001 * xx for xx in range(0,1001)]
    axes = plt.gca()
    axes.set_xlim([0,1])
    plt.plot(xs, p)
    plt.title('Triangular distribution')
    plt.show()

if __name__ == '__main__':
    lcg()
    random_generator()

