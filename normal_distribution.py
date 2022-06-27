import matplotlib.pyplot as plt
import random, math

def BoxMullerTransform():
    u0 = 0
    u1 = 0

    # Generate random u0 and u1 from the set { x | 0 < x < 1 }.
    while (u0 == 0): u0 = random.random()
    while (u1 == 0): u1 = random.random()

    # Calculate a magnitude.
    magnitude = math.sqrt(-2.0 * math.log(u0))

    # Calculate a theta.
    theta = 2.0 * math.pi * u1

    return (magnitude * math.cos(theta), magnitude * math.sin(theta))

def RandomNormalSkewed(mean, sd, skew=0):
    u0, u1 = BoxMullerTransform()

    # If skew is 0, we don't need to account for skew.
    if (skew == 0):
        return mean + sd * u0

    # If skew isn't 0, calculate the correlation coefficient (coeff).
    coeff = skew / math.sqrt(1 + skew ** 2)

    # Use coeff to get a correlated pair of random numbers.
    u1 = coeff * u0 + math.sqrt(1 - coeff ** 2) * u1

    # Return the skewed, normally distributed, random number.
    return mean + sd * (u1 if u0 >= 0 else -u1)

def RandomNormalSkewedBound(mean, sd, minimum, maximum, skew=0):
    # Generate a skewed, normally distributed, random number.
    r = RandomNormalSkewed(mean, sd, skew)

    # If the generated number is out of bounds, generate a new one.
    if (r < minimum or r > maximum):
        return RandomNormalSkewedBound(mean, sd, minimum, maximum, skew)

    # Return the number if within the bounds.
    return r

def RandomNormalSkewedSimplified(mean, minimum, maximum):
    # Calculate the median value between minimum and maximum.
    median = (maximum + minimum) / 2

    # Calculate the offset of the mean from the median.
    offset = median - mean

    # Calculate the SD by dividing the range by 2pi.
    # From my experiments, this gives a very good SD that gives samples covering the entire range
    # but results in only ~0.1 being outside the bounds.
    sd = (maximum - minimum) / (2 * math.pi)

    # I derived this from the Fisher-Pearson coefficient of skewness.
    skew = math.pow(offset, 3) / math.pow(sd, 3)

    # Generate and return a random number using the above calculations to estimate reasonable SD
    # and skew values.
    return RandomNormalSkewedBound(mean, sd, minimum, maximum, skew)

def Experiment(minimum, maximum, mean):
    # Get 10000 data samples.
    data = [RandomNormalSkewedSimplified(mean, minimum, maximum) for i in range(10000)]

    # Plot the samples on the histogram with 100 bins.
    plt.hist(data, 100)

    # Show the histogram.
    plt.show()

# Only run the experiment if this is the main script.
if __name__ == "__main__":
    Experiment(5, 15, 7)
















