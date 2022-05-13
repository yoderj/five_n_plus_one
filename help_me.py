import math


def euclidean_algorithm(a, b):
    next = a % b
    if next == 0:
        return (0, 1)
    else:
        d = -1 * (a // b)
        m, n = euclidean_algorithm(b, next)
        return (n, n * d + m)


def modular_inverse(mod, n):
    _, inverse = euclidean_algorithm(mod, n)
    if inverse < 0:
        inverse += mod
    return inverse


def bits_in_weird_number_system(n, first_base, p2):
    bits = 1
    if n < first_base:
        return bits
    n //= first_base
    while n > 0:
        bits += 1
        n //= p2
    return bits


"""
n is the exponent on p1
first_base is the weird digit at the beginning's base
c is c in c*n+1
p1 is the prime whose powers are being generated
p2 is the prime whose divisiblity after cn+1 is being checked
shift1 is the shift in the powers of p2 for p1 to go to

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


def bound(n, first_base, c, p1, p2, shift1):
    r = math.log(p2, p1)
    two_step_growth_limit = math.floor(math.log(c ** 2 + c + 1, p1))
    pow = bits_in_weird_number_system(n + two_step_growth_limit, first_base, p2) + shift1
    return pow * r < n


# -1 indicates that powers of p1 never map to powers of p2
# otherwise this gets the smallest power such that p1^n = 1 mod p2
# as well as the power that after doing the linear function is divisible by p2
# order 1 is strange, since it means that 1 maps to divisibility by p2, so pow = 0
# only happens on up to 1 prime, since 1 will always be larger than the other
def get_order(p1, p2, required_remainder):
    pow = -1
    order = 1
    number = p1 % p2
    while not number == 1:
        if number == required_remainder:
            pow = order
        number *= p1
        number %= p2
        order += 1
    if required_remainder == 1:
        pow = 0
    return pow, order


def modular_exponentiation(base, power, mod):
    answer = 1
    while power > 0:
        if power % 2 == 1:
            answer *= base
            answer %= mod
        power >>= 1
        base *= base
        base %= mod
    return answer


# checks for loops when get_shift finds that divisiblity by p2 after the function stops
# I expect that this will terminate faster by finding the first power which isn't divisible rather than
# checking a high power for divisibliity, I could be wrong about that
def loop_check(c, p2, pow_p2, p1, pow_p1, ord_p1):
    mod = p1
    check = 0
    while (c * modular_exponentiation(p2, pow_p2, mod) + 1) % mod == 0:
        mod *= p1
        check += 1
    return not (check%ord_p1 == pow_p1 and not check == 0)


# counts the failures of the lfiting lemma condition for p1^ord
# this will still work like normal for order 1 since it checks ord not pow
def get_shift(c, p1, p2, ord, pow):
    e = 2
    mod = p2 ** e
    n = modular_exponentiation(p1, ord, mod)
    while n == 1:
        # powers of p1 do not make powers of p2, check for loop
        # loop occurs when p2**e-1 -> p1**pow
        if not (c * modular_exponentiation(p1, pow, mod) + 1) % mod == 0:
            return loop_check(c, p2, e - 1, p1, pow,ord)
        e += 1
        mod *= p2
        n = modular_exponentiation(p1, ord, mod)
    return e - 2


# the first digit can sometimes be zero, in this case everything will match it
# but it is a possibliity, occurring when ord is 1 and so is the necessary remiander
# possibly after multiple loops of get_shift
def lookup(first_base, p2, sequence, shift, n):
    if not n % first_base == sequence[0]:
        return 0
    n //= first_base
    i = 1
    if i == len(sequence):
        return -1
    while n % p2 == sequence[i]:
        n //= p2
        i += 1
        if i == len(sequence):
            return -1
    return i + shift


def make_string(c, p1, p2, shift, ord, pow, num_digits):
    sequence = [pow]
    mod = p2 ** (shift + 1)
    for i in range(num_digits - 1):
        mod *= p2
        offset1 = modular_exponentiation(p1, ord, mod)
        power = modular_exponentiation(p1, pow, mod)
        offset = 1
        for j in range(p2):
            if (c * power * offset + 1) % mod == 0:
                sequence.append(j)
                pow += j * ord
                break
            offset *= offset1
            offset %= mod
        ord *= p2
    return sequence


# first digit is in a different base
def interpret_string(first_base, p2, sequence, index):
    number = sequence[0]
    meaning = first_base
    for i in range(1, index + 1):
        number += sequence[i] * meaning
        meaning *= p2
    return number


# checks numbers go to 1 when below bound
def full_trace(p1, p2, ord_p1, ord_p2, sequence1, sequence2, shift1, shift2, number):
    current_string = 1
    seen1 = set()
    seen1.add(number)
    seen2 = set()
    while not number == 0:
        if current_string == 1:
            number = lookup(ord_p1, p2, sequence1, shift1, number)
            if number in seen2:
                return False
            seen2.add(number)
            current_string = 2
        else:
            number = lookup(ord_p2, p1, sequence2, shift2, number)
            if number in seen1:
                return False
            seen1.add(number)
            current_string = 1
    return True

def test(c,p1,p2,ord_p1,ord_p2,shift_p1,shift_p2,string1,string2):
    past_bound = False
    for i in range(len(string1)):
        number = interpret_string(ord_p1, p2, string1, i)
        if not past_bound:
            past_bound = bound(number, ord_p1, c, p1, p2, shift_p1)
        if not past_bound:
            if not full_trace(p1, p2, ord_p1, ord_p2, string1, string2, shift_p1, shift_p2, number):
                return False
        else:
            maps_to = lookup(ord_p1,p2,string1,shift_p1,number)
            if maps_to == -1:
                return str(p1) + " ^ (" + str(ord_p1) + " * " + str(p2) + " ^ " + str(i - 1) + ")"
            loop_flag = lookup(ord_p2, p1, string2, shift_p2, maps_to)
            if loop_flag == number and not number == 0:
                return False
            elif loop_flag == -1:
                return str(p1) + " ^ (" + str(ord_p1) + " * " + str(p2) + " ^ " + str(i - 1) + ")"
    return True
#the confirmed until return value is exclusive, as in it is only confirmed before that point
def ugly_algorithm(c, p1, p2,d):
    if p1 == 2 and p2 % 4 == 3:
        return ugly_algorithm_2(c, p2,d)
    if p2 == 2 and p1 % 4 == 3:
        return ugly_algorithm_2(c, p1,d)
    # remainder that goes to 0 under cn+1 for each prime
    maps_to_0_p1 = (p1 - 1) * modular_inverse(p1, c) % p1
    maps_to_0_p2 = (p2 - 1) * modular_inverse(p2, c) % p2
    # find o where p1^o = 1 mod p2. also determine what p1 power leads to p2. return true if not possible
    pow_p1, ord_p1 = get_order(p1, p2, maps_to_0_p2)
    if pow_p1 == -1:
        return True
    pow_p2, ord_p2 = get_order(p2, p1, maps_to_0_p1)
    if pow_p2 == -1:
        return True
    # compute shifts for each of the strings, another chance to find truth values
    shift_p1 = get_shift(c, p1, p2, ord_p1, pow_p1)
    if type(shift_p1) == bool:
        return shift_p1
    shift_p2 = get_shift(c, p2, p1, ord_p2, pow_p2)
    if type(shift_p2) == bool:
        return shift_p2

    string1 = make_string(c, p1, p2, shift_p1, ord_p1, pow_p1, d)
    string2 = make_string(c, p2, p1, shift_p2, ord_p2, pow_p2, d)
    confirmed_until_1 = str(p1) + " ^ (" + str(ord_p1) + " * " + str(p2) + " ^ " + str(len(string1) - 1) + ")"
    confirmed_until_2 = str(p2) + " ^ (" + str(ord_p2) + " * " + str(p1) + " ^ " + str(len(string2) - 1) + ")"
    """
    print(ord_p1)
    print(shift_p1)
    print(string1)
    print(ord_p2)
    print(shift_p2)
    print(string2)
    """
    r = test(c,p1,p2,ord_p1,ord_p2,shift_p1,shift_p2,string1,string2)
    if type(r) == bool:
        if not r:
            return False
    else:
        confirmed_until_1 = r
    r = test(c,p2,p1,ord_p2,ord_p1,shift_p2,shift_p1,string2,string1)
    if type(r) == bool:
        if not r:
            return False
    else:
        confirmed_until_2 = r
    return (confirmed_until_1, confirmed_until_2)

#the skip of the 3 mod 4 case also skips the check for a loop including 2
#odd is whether the powers that don't lead to higher powers of 2 are odd or even
#if 2 leads to one of these powers then there is a loop
def two_loop(c,p1,odd):
    number = c*2+1
    count = 0
    while number%p1==0:
        number//=p1
        count+=1
    condition = count%2==1
    if condition == odd:
        return not count==0 #we want a true return unless the power is 0
    return False
#starts by examining 8, we will ignore the fact that everything maps to 2 for now when it comes to generating strings
#since it would be really strange to have a base 1 digit representing 2 and then a jump of multiple powers afterwards
def get_shift_2(c, p1, ord, pow):
    #we need to pass if the powers that don't lead to more than 2 are odd
    if two_loop(c,p1,not pow%2==1):
        return False
    e = 3
    mod = 2 ** e
    n = modular_exponentiation(p1, ord, mod)
    while n == 1:
        # powers of p1 do not make powers of p2, check for loop
        # loop occurs when p2**e-1 -> p1**pow
        if not (c * modular_exponentiation(p1, pow, mod) + 1) % mod == 0:
            return loop_check(c, 2, e - 1, p1, pow,ord)
        e += 1
        mod *= 2
        n = modular_exponentiation(p1, ord, mod)
    return e - 2

#special lookup for base 2 string in 3 mod 4 case. no matches is always divisible by 2
#first digit is base 2 instead of base 1 like it would be for all other strings, only way to make this clean
def lookup_2(sequence, shift, n):
    if not n % 2 == sequence[0]:
        return 1 #2 always divides the answer
    n //= 2
    i = 1
    if i == len(sequence):
        return -1
    while n % 2 == sequence[i]:
        n //= 2
        i += 1
        if i == len(sequence):
            return -1
    return i + shift

def full_trace_2(p1, ord_p2, sequence1, sequence2, shift1, shift2, number, current_string):
    seen1 = set()
    seen2=set()
    if current_string == 1:
        seen1.add(number)
    else:
        seen2.add(number)
    while not number == 0:
        if current_string == 1:
            number = lookup_2(sequence1, shift1, number)
            if number in seen2:
                return False
            seen2.add(number)
            current_string = 2
        else:
            number = lookup(ord_p2, p1, sequence2, shift2, number)
            if number in seen1:
                return False
            seen1.add(number)
            current_string = 1
    return True
def test_2(c,p1,p2,ord_p1,ord_p2,shift_p1,shift_p2,string1,string2):
    past_bound = False
    for i in range(len(string1)):
        number = interpret_string(ord_p1, p2, string1, i)
        if not past_bound:
            past_bound = bound(number, ord_p1, c, p1, p2, shift_p1)
        if not past_bound:
            if not full_trace(p1, p2, ord_p1, ord_p2, string1, string2, shift_p1, shift_p2, number):
                return False
        else:
            loop_flag = lookup(ord_p2, p1, string2, shift_p2, i + shift_p1 + 1)
            if loop_flag == number and not number == 0:
                return False
            elif loop_flag == -1:
                return str(p1) + " ^ (" + str(ord_p1) + " * " + str(p2) + " ^ " + str(i - 1) + ")"
    return True

def ugly_algorithm_2(c, p1,d):
    # finds inverse mod 4 for the case with 2
    maps_to_0_p1 = (p1 - 1) * modular_inverse(p1, c) % p1
    maps_to_0_p2 = (4 - 1) * modular_inverse(4, c) % 4
    # uses 4 for this so that we can start the shift search past the weird point
    pow_p1, ord_p1 = get_order(p1, 4, maps_to_0_p2)
    pow_p2, ord_p2 = get_order(2, p1, maps_to_0_p1)
    if pow_p2 == -1:
        return True

    shift_p1 = get_shift_2(c, p1, ord_p1, pow_p1)
    if type(shift_p1) == bool:
        return shift_p1
    shift_p2 = get_shift(c, 2, p1, ord_p2, pow_p2)
    if type(shift_p2) == bool:
        return shift_p2

    string1 = make_string(c, p1, 2, shift_p1, ord_p1, pow_p1, d)
    string2 = make_string(c, 2, p1, shift_p2, ord_p2, pow_p2, d)
    confirmed_until_1 = str(p1) + " ^ (" + str(ord_p1) + " * " + str(2) + " ^ " + str(len(string1) - 1) + ")"
    confirmed_until_2 = str(2) + " ^ (" + str(ord_p2) + " * " + str(p1) + " ^ " + str(len(string2) - 1) + ")"
    """
    print(ord_p1)
    print(shift_p1)
    print(string1)
    print(ord_p2)
    print(shift_p2)
    print(string2)
    """
    past_bound = False
    for i in range(len(string1)):
        number = interpret_string(ord_p1, 2, string1, i)
        if not past_bound:
            past_bound = bound(number, ord_p1, c, p1, 2, shift_p1)
        if not past_bound:
            if not full_trace_2(p1, ord_p2, string1, string2, shift_p1, shift_p2, number, 1):
                return False
        else:
            maps_to = lookup_2(string1, shift_p1, number)
            if maps_to == -1:
                confirmed_until_1=str(p1) + " ^ (" + str(ord_p1) + " * " + str(2) + " ^ " + str(i - 1) + ")"
                break
            loop_flag = lookup(ord_p2, p1, string2, shift_p2, maps_to)
            if loop_flag == number and not number == 0:
                return False
            elif loop_flag == -1:
                confirmed_until_1 = str(p1) + " ^ (" + str(ord_p1) + " * " + str(2) + " ^ " + str(i - 1) + ")"
                break
    past_bound = False
    for i in range(len(string2)):
        number = interpret_string(ord_p2, p1, string2, i)
        if not past_bound:
            past_bound = bound(number, ord_p2, c, 2, p1, shift_p2)
        if not past_bound:
            if full_trace_2(p1, ord_p2, string1, string2, shift_p1, shift_p2, number, 2) == False:
                return False
        else:
            maps_to = lookup(ord_p2, p1, string2, shift_p2, number)
            if maps_to == -1:
                confirmed_until_2= str(2) + " ^ (" + str(ord_p2) + " * " + str(p1) + " ^ " + str(i - 1) + ")"
                break
            loop_flag = lookup_2(string1, shift_p1, maps_to)
            if loop_flag == number and not number == 0:
                return False
            elif loop_flag == -1:
                confirmed_until_2 = str(2) + " ^ (" + str(ord_p2) + " * " + str(p1) + " ^ " + str(i - 1) + ")"
                break
    return (confirmed_until_1, confirmed_until_2)


def brute_force_confirm(c,p1,p2):
    n = 1
    for i in range(0,150):
        seen = set()
        n*=p1
        number = n
        seen.add(number)
        while not number == 1:
            number*=c
            number+=1
            number2=1
            while number%p1==0:
                number//=p1
                number2*=p1
            while number%p2==0:
                number//=p2
                number2*=p2
            number = number2
            if number in seen:
                return False
            else:
                seen.add(number)
    n = 1
    for i in range(1,150):
        seen = set()
        n*=p2
        number = n
        seen.add(number)
        while not number == 1:
            number*=c
            number+=1
            number2 =1
            while number%p1==0:
                number//=p1
                number2*=p1
            while number%p2==0:
                number//=p2
                number2*=p2
            number = number2
            if number in seen:
                return False
            else:
                seen.add(number)
    return True

primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151]
false_count=0
for p1 in primes:
    for p2 in primes:
        for p3 in primes:
            if not(p1==p2 or p2==p3 or p3==p1):
                q = brute_force_confirm(p1, p2, p3)
                w = ugly_algorithm(p1, p2, p3,10)
                if not q:
                    false_count += 1
                if not q and not w == False:
                    print(p1)
                    print(p2)
                    print(p3)

                if q and not w:
                    print(p1)
                    print(p2)
                    print(p3)
print(false_count)

#print(ugly_algorithm(5,2,3,512))







