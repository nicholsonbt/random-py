#####################################
from normal_distribution import *  ##
from l2_rls import *               ##
#####################################


import matplotlib.pyplot as plt
import numpy as np
import random
import math


def CalculateSkewAndSD(minimum, maximum, mean):
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
    
    return skew, sd


def CalculateActualMean(desired_mean, sd, skew):
    n = 10000
    
    # Given the desired mean, standard deviation and skew, return the actual mean of the skewed,
    # normally distributed, random numbers found using these values.
    return sum([RandomNormalSkewed(desired_mean, sd, skew) for i in range(n)]) / n


def GetBetterMean(minimum, maximum, desired_mean, mean, accuracy):
    # Calculate skew and sd.
    skew, sd = CalculateSkewAndSD(minimum, maximum, mean)

    # Calculate the actual mean for the given mean.
    actual_mean = CalculateActualMean(mean, sd, skew)

    # Calculate the range.
    r = maximum - minimum

    # Calculate the maximum offset.
    offset = r * accuracy

    # If the actual mean is close enough to the desired mean, return the mean.
    if (actual_mean < desired_mean + offset and actual_mean > desired_mean - offset):
        return mean

    # Calculate a new mean by subtracting the offset.
    new_mean = mean + (desired_mean - actual_mean)

    # Use the new mean to find an even closer one.
    return GetBetterMean(minimum, maximum, desired_mean, new_mean, accuracy)


def RandomValues(lower, upper):
    # Calculate three random values in a given range.
    a = random.randint(lower, upper)
    b = random.randint(lower, upper)
    c = random.randint(lower, upper)

    # Sort the values so that a minimum, mean and maximum can be found in that order.
    values = [a, b, c]
    values.sort()

    # Return the values.
    return values


def NewRow(lower, upper):
    # Calculate random values.
    minimum, base_mean, maximum = RandomValues(lower, upper)

    # Calculate the median value between minimum and maximum.
    median = (maximum + minimum) / 2

    # Calculate the offset of the mean from the median.
    offset = median - base_mean

    # Calculate the SD by dividing the range by 2pi.
    # From my experiments, this gives a very good SD that gives samples covering the entire range
    # but results in only ~0.1 being outside the bounds.
    sd = (maximum - minimum) / (2 * math.pi)

    # I derived this from the Fisher-Pearson coefficient of skewness.
    skew = math.pow(offset, 3) / math.pow(sd, 3)

    # Calculate the actual mean given the above values.
    actual_mean =  CalculateActualMean(base_mean, sd, skew)
    
    # Calculate a mean that gives a value closer to the the desired mean when averaged.
    derived_mean = GetBetterMean(minimum, maximum, base_mean, base_mean, 0.0001)
    
    return np.array([minimum, maximum, base_mean, median, offset, skew, actual_mean]), derived_mean


def GetNSamples(lower, upper, n):
    # Initialise numpy ndarrays to hold values for data and labels.
    X = np.zeros((n,7))
    y = np.zeros((n,1))
    
    for i in range(n):
        # Get a random new row.
        Xi, yi= NewRow(lower, upper)

        # Add the new row data to the next row.
        X[i, 0] = Xi[0]
        X[i, 1] = Xi[1]
        X[i, 2] = Xi[2]
        X[i, 3] = Xi[3]
        X[i, 4] = Xi[4]
        X[i, 5] = Xi[5]
        X[i, 6] = Xi[6]

        # Add the new row label to the next index.
        y[i] = yi

        print(i + 1, "out of", n)

    return X, y


def MeanExperiment():
    train_samples = 1000
    test_samples = 100

    lower = -1000
    upper = 1000

    # Get training data and labels.
    print("Generating Training Data:")
    train_X, train_y = GetNSamples(lower, upper, train_samples)

    # Get testing data and labels.
    print("Generating Testing Data:")
    test_X, test_y = GetNSamples(lower, upper, test_samples)

    # Train the model using the training data.
    w = train(train_X, train_y)

    # Test the model using the testing data.
    y_hat = predict(w, test_X)

    # Initialise an accuracy value.
    acc = 0

    for i in range(test_samples):
        
        # Calculate the range (maximum - minimum).
        r = test_X[i, 1] - test_X[i, 0]

        # Calculate the accuracy of the current test sample.
        a = (abs(test_y[i] - y_hat[i]) / r)[0]

        # Add the current accuracy to the sum of accuracies.
        acc += a

    # Output the average accuracy.
    print("\n\nAverage Percentage Offset from Actual: (smaller = better, maximum is 1)")
    print(a / test_samples)

    # Output the coefficients found.
    print("\n\nW Values:")
    print(w)

    # Return the coefficients found.
    return w


# Only run the experiment if this is the main script.
if __name__ == "__main__":
    MeanExperiment()














