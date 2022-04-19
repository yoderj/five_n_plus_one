import math

def bits_in_weird_number_system(n,first_base,p2):
    bits = 1
    if n<first_base:
        return bits
    n//=first_base
    while n>0:
        bits+=1
        n //=p2
    return bits

"""
n is the exponent on p1
first_base is the weird digit at the beginning's base
c is c in c*n+1
p1 is the prime whose powers are being generated
p2 is the prime whose divisiblity after cn+1 is being checked
shift1 is the shift in the powers of p2 for p1

this bound works by induction. once both conditions are true, they will be true of the next digit trying to grow
the first condition calculates the maximum power of p1 attainable in 2 steps of growth without division
it then finds the number of weird-base bits it takes up, and adds the shift. this gives the largest power of p2
attainable after the 2 steps staying above the start that doesn't loop
if the log-ratio adjustment of this power is less than n, all of these 3rd elements of the trajectory fall within
n's sphere of zeros (the area in which n produces the highest divisibility by p2) this sphere of zeros is required for 
n to have grown at all, this means that they go to a power of p2 less than the one n went to, and when paired with the 
other condition must go back to a power of p1 less than n. But this other condition isn't necessary anymore since
n being greater than the power of p2 indicated by 2 steps of max growth gives you a number less than n by the third step

the first condition inductions as follows, assuming the condition became true, we know that the the value of "pow"
can only have increased by 1, since the portion of the two_step_growth_limit that fit within the same bit as n
will also fit into whatever n doesn't take up of the next bit since the last increment of that bit represents as many
numbers as all previous bits combined, then we can just assume whatever spilled over into further bits still takes up 1
bit. this caps the increase on the quantity "pow*r" to be r. since a minimum digit of 1 has been put in the next bit
n must have at least doubled, so the right hand side gains pow*r >r so the condition remains true.
this applies even if there's a long chain of zeros appended to the string, since the first nonzero bit after it
will still do the doubling thing.

once we have this condition, it also frees us from having to worry about the digits that get zeroed out by n's growth
and the numbers that are offset from n by the order function. since the above induction guarantees that n is greater
than the power of p2 that can be attained after 2 steps of growth, it also guarantees that n is greater than the power
of p2 indicated by its position.


"""

def bound(n, first_base,c,p1,p2,shift1):
    r = math.log(p2,p1)
    two_step_growth_limit = math.floor(math.log(c ** 2 + c + 1, p1))
    pow = bits_in_weird_number_system(n+two_step_growth_limit,first_base,p2)+shift1
    return pow*r<n

print(bound(4,1,5,4,3,1))
