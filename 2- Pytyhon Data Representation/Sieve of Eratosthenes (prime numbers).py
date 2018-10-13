#!/usr/bin/env python3
# Instructors: Dr. Scott Rixner, Dr. Joe Warren
# Course: Python Data Visualization, University of Michigan, Coursera.
#

"""
Sieve of Eratosthenes Algorithm Implementation.
https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
"""
    
def compute_primes(max_integer):
    sieve = [True for _ in range(max_integer + 1)]
    sieve[0:1] = [False, False]
    for start in range(2, max_integer + 1):
        if sieve[start]:
            for i in range(2 * start, max_integer + 1, start):
                sieve[i] = False
    primes = []
    for i in range(2, max_integer + 1):
        if sieve[i]:
            primes.append(i)
    return primes

def compute_primes(bound):
    """
    Return a list of the prime numbers in range(2, bound)
    """
    return [i for i in range(2, bound) if all(0 if i%q == 0 else 1 for q in range(2,i**.5))]


print(len(compute_primes(200)))
print(len(compute_primes(2000)))
