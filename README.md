# random-py

When using my algorithm to generate skewed, normally distributed, random numbers, I found that the actual mean of generated values was (sometimes substantially) different to the mean given.

I also noticed that the offset was not constant and the greater the skew, the greater the offset. As such, I decided to find a way of readjusting this mean.

By calculating the actual mean value, and using it to offset our given mean:

mean = mean + (desired mean - actual mean)

This could then be repeated until the actual mean is within acceptable bounds of the desired mean.
The downsides of this approach are that it can take a while to calculate the best mean value, as you have to generate a large number of random samples to find the mean.

To streamline this therefore, I decided to use L2 Regularised Least-Squares to find coefficients such that an acceptable mean value could be calculated for some given values in a reasonable time.

The features I used were:
 - The minimum bound,
 - The maximum bound,
 - The original mean,
 - The median of the bounds: (maximum + minimum) / 2,
 - The offset: median - original mean,
 - The calculated skew,
 - The actual mean given the skew and SD calculated and the original mean,
 
My labels were the desired mean.

## Results:

I trained my model using 10,000 training samples with minimum, maximum, and desired means in the range of -1000 to 1000.

With 100 testing samples (in the same range), I obtained the coefficients:

 \[ 0.0, 0.27950631, 0.2789222, 1.18077736, 0.27921426, -0.9015631, 1.48811746, -1.01904657 ]
 
With an average offset (offset from desired mean / range) of 0.000012.

In practice however, I've found the above values to give worse averages than the original ones when used with a small range and/or minimum and maximum values of the same sign (both positive or both negative).

In the future, I want to repeat this test using different techniques, and explore how different cases differ (will significantly different coefficients be obtained with a maximum and minimum of the same sign as opposed to different signs, and how will extremely large ranges compare to very small ones.