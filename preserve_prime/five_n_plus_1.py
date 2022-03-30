"""
This script explores the 5n+1 problem, first proposed by MSOE student
Max Milkert, to the best of my knowledge.

In terms of the code provided here, the theorem is that i(n) <= 7 for all
positive integers n.  This code was used to prove it numerically up
to n > 5_000_000_000.

Dr. Josiah Yoder, 2021
"""


def log(n,prime):
    """ Calculate the log considering only powers of prime and
        ignoring other prime factors. """
    power = 0
    while n % prime == 0:
        n//=prime
        power+=1
    return power


def c(n):
    """ Convert a number to its cannonical form: as a tuple
        representing the powers of 2 and 3."""
    return (log(n,2),log(n,3))


def e(n, prime):
    """ Remove all factors except powers of prime from n """
    m = n
    while m % prime == 0:
        m //= prime
    return n // m


def f(n):
    """ Remove all factors except powers of 2 and 3 from n """
    return e(n, 2) * e(n, 3)


def g(n):
    """5n + 1"""
    return 5 * n + 1


def h(n):
    """ A single step of the iterative process. """
    return f(g(n))


def i(n):
    """ Find cycle length when starting with n.
        This is the number of times that h(n) is applied
        to reach 1. """
    count = 0
    while n != 1:
        n = h(n)
        count += 1
    return count


# l = []
# for j in range(0, 5_940_106_666):
#     m = i(j)
#     if m > 7: # Not reached up to 5_940_106_666
#         print(j, m)
#         l.append(m)
#         break
#

h(5_940_106_666)
i(5_940_106_666)

# n must have only powers of 2 or powers of 3 and not both
# or it exits immediately.
#
# In terms of this code, this means that two axis where j = 0 or k = 0
# yield i(n) > 1.
#
# This is shown experimentally by the loop below but easy to prove for all n.
# Adding 1 to a multiple of 6 guarantees that neither 2 nor 3 are factors.
#
l = []
# for j in range(0, 1000):
#     for k in range(0, 1000):
#         n = (2**j) * (3**k)
#         m = i(n)
#         if m > 5:
#             print('2**'+str(j),'3**'+str(k),'i(n):',m)
#             l.append(m)

# Explore powers of 2
k = 0
for j in range(0, 10_000):
    n = (2**j) * (3**k)
    m = i(n)
    if m > 5:
        print('2**'+str(j),'3**'+str(k),'i(n):',m,end=' ')
        while n > 1:
            print(c(n),end=' ')
            n = h(n)
        print()
        l.append(m)

# Explore powers of 3
j = 0
for k in range(0, 1000):
    n = (2**j) * (3**k)
    m = i(n)
    if m > 5:
        print('2**'+str(j),'3**'+str(k),'i(n):',m,end=' ')
        while n > 1:
            print(c(n),end=' ')
            n = h(n)
        print()
        l.append(m)

# Explore powers of 9

j = 0
for k in range(0, 30, 2):
    n = (2**j) * (3**k)
    m = i(n)
    print('2**' + str(j), '3**' + str(k), 'i(n):', m, end=' ')
    while n > 1:
        print(c(n), end=' ')
        n = h(n)
    print()

# Explore odd powers of 2
print('Odd powers of 2')
k = 0
for j in range(1, 10, 2):
    n = (2**j) * (3**k)
    m = i(n)
    print('2**'+str(j),'3**'+str(k),'i(n):',m,end=' ')
    while n > 1:
        print(c(n),end=' ')
        n = h(n)
    print()
