import random
import math

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


def UnitVector(n):
    # Pick a random point on the n-dimensional hypersphere of radius 1.
    # I used the method found at:
    # https://mathworld.wolfram.com/HyperspherePointPicking.html

    # Initialise an array of n values representing the magnitude in each of the dimensions.
    values = []

    # The Box-Muller Transform returns 2 values, so add these to the array.
    for i in range(n // 2):
        x, y = BoxMullerTransform()
        values.append(x)
        values.append(y)

    # If there's an odd number of dimensions, add the first Box-Muller Transform value.
    if (n % 2 != 0):
        x, y = BoxMullerTransform()
        values.append(x)

    # Calculate the scale (1 / the magnitude) of the vector.
    scale = 1 / math.sqrt(sum([value ** 2 for value in values]))

    # Multiply each dimension by the scale to obtain a unit vector.
    return [value * scale for value in values]

x = UnitVector(10)
print(x)
