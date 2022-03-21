# five_n_plus_one
Max Milkert, Alex Ruchti, Dr. Josiah Yoder
2021 - 2022 academic year

Explores Max Milkert's 5n+1 problem, a variation on the famous 3n+1 problem in which certain prime factors are retained instead of divided out in between the steps. In this particular case, those prime factors are 2 and 3.

This script explores the 5n+1 problem, first proposed by MSOE student
Max Milkert, to the best of my knowledge.

In terms of the code provided here, the theorem is that i(n) <= 7 for all
positive integers n.  This code was used to prove it numerically up
to n > 5_000_000_000.

## Multiples of six.
For all n of the form n = 6*m, m a positive integer, the 5n + 1 problem
converges instantly.

This is because 5n+1 = 5*6*m + 1 cannot be divisible by either 2 or 3, as the
first term is divisible by both two and three and the second term is not.

Therefore, any number having both 2 and 3 as factors will converge to 1 
immediately, in just one step.

## Powers of 9
All powers of 9 converge in just two steps, stepping immediately to 2, which then converges to 1
in the second step.
 
Let n = 9^k, where k is a positive integer.

Then 5n+1 = 9^k + 1.  This cannot be a power of 3.  We consider here what powers
of 2 might remain that the 5n+1 problem would retain.

For 9^k + 1 to be a power of 2, 9^k = 2^j - 1. (j a non-negative integer).
In other words, 9^k would need to be a Mersenne number.

However, the Mersenne numbers are either prime or are composite numbers
with at least two prime factors. (I (Josiah) don't know how to prove this.)

So 9^k cannot be a Mersenne number, as it has only one prime factor.

But 9^k + 1 might just CONTAIN a power of 2, i.e., in the form
9^k + 1 = m*2^l, where m is an odd number and l is a positive integer.

It is guaranteed that 9^k + 1 is even as both 9^k and 1 are odd. So there 
must be at least one factor of 2.

So we now consider (9^k+1)/2.  This must always be odd.

Consider 9^k mod 4.  If 9^k mod 4 is 3, then 9^k + 1 is a multiple of 4.
But for all other values of 9^k mod 4, it cannot be.

9 mod 4 is 1

81 mod 4 is 1  (4*20 + 1 = 81)

9^3 mod 4 is 1 (9^3 mod 4 = (9^2 mod 4)(9 mod 4) = 1*1 mod 4 = 1)

And from this point out the pattern continues and can easily be proved by 
induction.

So all even powers of 3 lead to 2 in one step.

# Odd powers of 2

Odd powers of two converge to 1 in a single step.

Consider n = 2^2k * 2, where k is a non-negative integer.

Then 5n+1 = 10*2^2k + 1. For this to be a multiple of 3, we must have 
10*2^2k mod 3 = 2.  10 mod 3 = 1, and 4 mod 3 = 1, so 10*2^2k mod 3 = 1 for 
all non-negative k. So the 5n+1 method will simplify this to 1 directly.
