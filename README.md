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

# verification algorithm

2 is always a primitive root (2^power is only congruent to 1 mod n when power is a multiple of phi(n)) mod a power of 3.
See the first post and the linked lifting lemma https://math.stackexchange.com/questions/594782/2-is-a-primitive-root-mod-3h-for-any-positive-integer-h 
The implication of this is that 4^n/3 is congruent to 1 mod n when n is a power of 3. Normally this power would be 2/3n since that’s phi(n) but 4 is the square of the primitive root 2. 
For a given power of 3 modulus this means that there will be 3 possible candidates for the power of 4 that maps to index 0 under 5n+1. These will be 4^(exponent that maps to 0 in the modulus/3), 4^that exponent + the modulus/3, and 4^that exponent + 2*modulus/3) since these all share the congruence to 0 under 5n+1 in modulus/3. This property lets us represent this exponent as a base 3 number. 
For example, the sequence 2,0,0,1 tells us that the exponent of the power of 4 congruent to 0 after 5n+1 mod 3^5 is 2*3^0 + 0* 3^1 + 0*3^2 + 1*3^3 = 29. Every power of 4 that becomes divisible by 243 by doing 5n+1 must have an exponent congruent to 29 mod 243.


A similar property applies for powers of 3 and their divisibility by powers of 2 after 5n+1.
2 is not like the other primes, its powers don’t have primitive roots (except for 4, which has just 3, but should have 2 roots). But the lifting lemma still applies (despite it saying it doesn’t work).
We know that 3^2 is congruent to 1 mod 8 but not 16. 
If 3^n is congruent to 1 mod 2^k, and not congruent to 1 mod 2^(k+1), we can write 3^n as 2^k * a +1, where a is not divisible by 2 (otherwise condition 2 is not true). If we square this we get a number of the form (2^(2k) * a^2) + 2*2^k *a +1. Looking at this number mod 2^(k+1) we get remainder 1, and looking at it mod 2^(k+2) we do not get remainder 1 since a is not divisible by 2.

This serves to inductively prove that 3^n/4 is congruent to 1 mod n where n is a power of 2. 
This means a similar string to the one above can specify the power of 3 that maps to 0 under 5n+1 mod each power of 2. But since 2 has that slightly strange divisibility property the string starts with the powers of 8. For example, the string 1 means that 3^1 maps to 0 mod 8, the string 101 means that 3^5 maps to 0 mod 32, etc…

If you can show that every number in a collatz-like problem descends below itself, that inductively means that every number converges. This, along with these strings lets us make an algorithm for confirming the 5n+1 holdout problem. If the exponent represented by the strings is greater then the number of digits (might be a +1 in here, +2 in the case of 2) (also a ratio of logs adjustment between the bases of 4 and 3) that means that the number in question, and any other number mapping to the same power of the other base descends below itself in the next step. Numbers that don’t descend below themselves are very rare, in my first example with the base 3 string, we can see that it starts with 200, so 4^2 ends up being divisible by 3^4, so it didn’t shrink because there was a sufficiently long string of zeros. But long enough strings of zeros will become super rare the further you go, since the exponent on 4 will grow by orders of magnitude, and the exponent on the next power of 3 will grow linearly. Should one of these cases be encountered, you would have to trace the trajectory of that number, which could be done by looking up the other string and finding the congruence of the new exponent. 

checking for powers skipped over like the case of 4^5 leading to 3^3 when 4^2 skips right to divisibility by 3^4 is not required, since if you encounter the long string of zeros, it can only continue for one or 2 more digits past the passing point, since otherwise the growth would be so high as to not be attainable by doing 5n+1. Since this limit is so tight, advancing one of the digits by a multiple like going from 4^2 to 4^5 to make sure everything going to 3^3 shrinks to do so is unnecessary, since whatever you're adding will be larger than 1 or 2.

The majority of the work for confirming the numbers will be in getting these strings, which can be done by using fast modular exponentiation taking log(log(n)) time for every element in the string you generate, but there are log(log(n)) elements, bringing the time up to log(log(n))^2. The size of the numbers in each modulus also grows logarithmically with the size of the exponent, bringing the runtime to log(log(n))^3. 

#proof

1. numbers without 2 or 3 in their prime factorization converge immediately by the definition.
2. numbers with both 2 and 3 in their prime factorization will not be divisible by either after applying 5n+1, and will then converge.
3. odd powers of 2 converge since the remainders of the powers of 2 cycle between 2 and 4 mod 6 (2 is 2, 2 * 2 is 4, 4 * 2 is 8 which is congruent to 2 again), applying 5n+1 to the numbers of the form 6n+2 converts them into the form 30n + 11, these numbers cannot be divisible by 2 or 3 since 2 and 3 divide 30 and neither divides 11. by point 1 they must then converge
4. even powers of 3 converge since the remainders of the powers of 3 cycle between 1 and 3 mod 4 (3 is 3, 3 * 3 is 1), applying 5n+1 to the numbers with remainder 1 converts them into the form 4n+2, which is divisible by 2 exactly once, and therefore converges by point 3
5. any division in between 5n+1's will cause the number to shrink. 2 and 3 are preserved not divided out, and 5n+1 can never create a number divisible by 5, so the minimum prime factor removed must be 7, and for all natural numbers (5n+1)/7 <n
6. any power of 4 must go below itself within 2 steps. By point 5, if there is a division after the first 5n+1, then the number will have decreased. If not, then applying the second 5n+1 will put the number into the form 25 * 4^n +6. the highest power of 2  dividing this is 1, so it will then fall to 2 after division and will converges shortly after by point 3. (We will show later that these numbers are also not part of a two-loop, and thus must converge.)
7. the range of numbers between 3^n and 5 * 3^n+1 contains only 1 power of 3. the next power of 3 above 3^n is 3 * 3^n, which is less than 5 * 3^n +1. the next power up will be 9 * 3^n which is greater than 5 * 3^n +1
8. any power of 3 that does not create a 2-loop must go below itself in 4 steps.  The first possibility is that after 5n+1 the number is able to divide. this is lower than it started because of point 5. a second possibility is that it 5n+1's to a larger number (a power of 4) and then it grows larger again, by point 6, this number then divides to 2. The third possibility is that the number grows, and then shrinks, but not below the starting point. By point 7, this new number must be 3^{n+1}. n must be odd, since otherwise we would have converged immediately by point 4 therefore n+1 is even, and we fall to an odd power of 2 in the next step and converge shortly thereafter.
9. the 5n+1 problem cannot diverge. each power of 3 and 4 must fall below themselves in a small number of steps by points 6 and 8, therefore you can always inductively trace any trajectory to either the trivial cycle (the one that contains 1) or to some other loop if one exists.
10. no odd loops exist. if a loop is odd it must feature back to back powers of either 4 or 3, which cannot happen since the +1 of 5n+1 breaks the previous divisibilities. (JY: Can we say simply because we must alternate between powers of two and three?)
11. loops must be of size 2. powers of 4 that do not have a 2-loop fall to 2 in 2 steps by point 6, so larger loops with powers of 4 as the lowest element cannot exist. by point 8, powers of 3 at the start of a growing trajectory fall to 2 at the max step length of 4, so this cannot support a loop. there are also no odd loops since by point 10. this means that a loop must be of size 2.
12. no loops of size 2 exist. let n be the smallest element of the loop, after the first 5n+1 there can be no divisions since by point 5 that produces a contradiction of n not being the smallest element. this means the divisions must occur on step 2. this gives us the equation 5 * (5 * n+1)+1 = c * n. Simplify this to 25 * n+6=c * n. and this equation can only produce the trivial cycle becasue if n is a power of 4, or a power of 3 greater than 3^1, then n divides one side but not the other. and if n is 3, then 27 * n = c * n so c = 27, but c cannot be 27 becuase powers of 3 do not get divided out. this leaves us with only the trivial cycle as a solution. n = 1 and c = 31. 1 cycles to 6, 5 * 6 +1 = 31, then we descend back to 1.
13. since the process cannot diverge (point 9) and contains no nontrivial loops (points 10 and 11) all integers must return to 1.

 Some Max Thoughts on finding lower bounds
 Ratio of exponent bigness is log(p1)/log(p2)
P1 string can append zeros up until the index representing a power of p2 where the power equals the floor of the bigness ratio times the power it represents. In the worst case the power of p2 is 1 above the power of p1, so the upper limit on the number of additional zeros is however many powers of p2 * the starting number +1 fit under n*_+1. This should be the ceiling of logp2(n)

In the case of the 4 string in the 5n+1 problem, this happened with 2001. 4^2 encompasses floor 1.26 *2 = 2 powers of 3. There are then 2 = ceiling of log4(5) available places to grow by appending 0

A similar thing applies to the p2 string to bound the maximum number of zeros it can append but invert the bigness ratio. The minimum is bounded by the need to stay above the initial number.

Now we want to show that the minimum number of zeroes appended to the first string encompasses all powers represented in the range of growing maximally for 2 steps and staying barely above the starting point
In the case of 2 primes we can look at the floor of log base p1(n^2 +n +1) for the number of powers contained in 2 steps of growth, this will tell us that p1^s + that log thing is the maximum power of p1 attainable in 2 steps
we need to look at the ceiling of log base p2 of that first log thing, this is the most (since the bits will likely be of greater significance) number of base p2 bits needed to hold that range of powers
then we take the log p2 ceiling again of that number of p2 bits to find the number of bits needed to store the number that would necessitate that many bits to be zeroed to grow, that will serve as the p1 exponent for the lower bound.
P1 and p2 only need be prime powers. Also that means the bigness ratios will be different for each string.
This is only needed for conjectures where both primes have powers that lead to each other. For example, 7n+1 {5,11} none of this is necessary since remainder 11 and all its powers =1 mod 5, and 7*1+1 is never 0. The more mathy condition is that this is needed for conjectures where the modulus that maps to 0 in each prime is one of the other prime’s powers less than or equal that which is needed to return to 1. Furthermore that power must form strings like it does for 5n+1 since the lifting thing kicks in when congruent to 1 mod p^n and not mod p^n+1. That power remains constant, so eventually p^n+whatever will grow big enough that it is not 1, that is then the starting index of your string.

An example of the bound being found with 4^n mod powers of 3 using 1000000007 n +1 is log4(big2 + big +1) floor is 29 as floor. To span 29 numbers takes at most ceiling log3(29) = 4 bits. To require zeroing out the next 4 string positions takes a number that’s log3(4) ceiling = 2 big. We can just ignore the bigness ratio since its >1 So the lower bound can be put at 4^9. Not the tightest but it works.

 
A general 2 prime algorithm
 
 the goal of the algorithm is to construct (almost but not quite) base p2 numbers whose successive indicies track what powers of p1 map to p2^index
 
 Step 1 (for primes that aren't 2):
 for both primes:
 find the index that goes to 0 under the *n +1 mapping
 calculate the remainders of powers of each prime mod the other. track which one goes to the index that maps to 0.
 if: either prime cannot lead to powers of the other terminate algorithm return true
 
 example: 7n+1{5,11} remainder 2 mod 5 goes to 0, remainder 3 mod 11 goes to 0
 the powers of 3 mod 11 are: 5, 3... the powers of 11 are 1,1,1,1,1 and cannot conatin 2
 
 else: check if p1^power that makes 1 mod p2 is also congruent to 1 mod p2^2, if it is, check p2^3 etc... until it is not. keep track of this number.
 p2^n grows so the condition eventually is met. each time you do this, check the power that you found mapped to 0 again, if it stops being zero under the mapping, check for a loop, return false if loop, else you can return True. Do this for other prime as well. this condition forms the basis of a useful lemma for lifiting congruences to higher prime powers. 
  Special case: 2 has odd behavior since it forms an edge case in the congruence lifting lemma. the fix is to start finding powers at 4.
 now it is time to begin constructing the strings
 Step 2:
 
 in the simplest case, 2 is not p2, and p1^(p2-1) is not congruent to 1 mod p2^2.
 
 in this case the digits in the string are (mostly) base p2. the first digit will be between 0 (inclusive) and ord(p1) mod p2 (exclusive). the next digits will be normal base p2 digits. the first digit will be the 1's place, the second will be the ord(p1)'s place, the third will be the p2*ord(p1)'s place etc...
 these digits represent the powers p1 must be raised to for the mapping to send it to p2^index. the first digit tells you what goes to p2, the next is p2^2, etc...
 the maximum value of these weird number representations is the normal phi function of the powers of p2 but with the one p-1 factor replaced by ord(p1) mod p2
 
 this is very weird, so heres an example. 5n+1{2,7} 2^3 is congruent to 1, a primitive root would take 6. 4 is the index that goes to 1 under the 5n+1 mapping, so 2^2 is the number you want. the first few digits of the string look like: 2, 3, 6, 4. the 2 tells you that 2^2 -> 7. the next tells you that 2^(2*1 + 3*3) -> 49. the third tells you that 2^(2*1 + 3*3 + 6*21) -> 7^3, and the fourth tells you that adding 4*(3*49) to the exponent will give you divisibility by 7^4 
 
now we address the shift for problems that have cleared the initial checks. for each time p1^x was congruent to 1 in both mod p2^n and p2^n+1, you shift the power of p2 that you map to when you raise p1 to the number in the string by 1. the first bit used to mean p2, it now means p2^number of falied conditions+1. interestingly, in this case there are a few powers of p2 that p1 can never map to since it has a divisibility minimum.
 
 now to deal with 2.
 2^1 is the only case where the lifting lemma fails. since squaring a 2n+1 number = 4n^2 +4n +1, the coefficient on n^2 always big enough to be 0 mod p^n+2, but not in this one case. This means that when 2 is p2, there's a completely different set of rules. 
 
 the initial checks have to be done starting on 4 instead of 2 since every number automatically gets divisible by 2 after doing *n+1. if your number is 1 mod 4, it might not be able to make multpiles of 4 under the map. if this is the case, return true if 2 does not loop to it, else false.
 now we have to check the lifting lemma criteria again but starting at 4. as with last time keep making sure that one of the remainders can map to 0, and if not check that the last power you could make doesn't form a loop.
 
 your string will be a regular binary string this time, the first bit represents the power needed to get divisibility by the last power of 2
 for which ord(p1) = 2
 
Step 3:
 
 now we generate the strings. for each string there will be p2 choices for which power of p1 maps to the next power of p2. to test which choice it is we use fast modular exponentiation to generate all p2 of the candidates, and then test if they map to 0, setting the next digit according to the answer.
 
 Step 4:
 
 once we have the strings we need to look for loops. for each number represented by the first n digits of the first string, look up n in the second string, if it goes back to the first number, you have a loop.
 
 
Proof of why the strings work.
 
 1. every relatively prime number to a prime power p has some index mod p^power that maps to zero under *n +1. for any 2 distinct indexes, we know that p^power does not divide i1-i2 becuase i1-i2 is not congruent to 0 mod n. now we will produce a contradiction, assume that the *n +1 mapping sends two of the original indexes to the same new index. this means that n*i1+1 = n*i2+1 mod p^power. manipulating the algebra gives n*(i1-i2) = 0 mod p^power. but this is not possible since p^power is relatively prime to n, and does not divide i1-i2, therefore the *n+1 mapping reshuffles the indicies without collision.
 
 2. for prime p1 and prime power p2^n, let o be the order of p1 mod p2^n. if p1^o is not congruent to 1 mod p2^n+1, then the order of p1 mod p2^(n+1) is p2*o and p1^p2*o is not congruent to 1 mod p2^(n+2). we know from the conditions that p1^o is of the form c*p2^n +1, and that p2 does not divide c, p1^o would be 1 mod p2^(n+1). if we raise this number to the p2th power, the binomial expansion will be 1 + p2*c*p2^n + other terms. the extra p2 comes from the binomial coefficient. if we take this number mod p2^(n+1) we will get 1 since p2^(n+1) divides every term but 1. But mod p2^(n+2), it will not be congruent to 1 since the second term is only divisible by p2^(n+1). all of the other terms drop out since they are necessarily divisible by higher then n+2 powers of p2. the only exceptio to this proof occurs when p2 = 2^1. the binomial expension of squaring 2c+1 is 4c^2 +4c +1 in which the highest term does not drop out mod 8. squaring is too small of an expansion and 1 is too small of an exponent. if the exponent were any higher, doubling it would be greater or equal compared to adding 2 to it, and if p2 were at least 3, the binomial coefficient of 3 for cubing would be able to boost that term to p2^n+2. which is why there's that special ruleset with 4 in the algorithm
 
