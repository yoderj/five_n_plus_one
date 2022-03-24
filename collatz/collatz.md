# Collatz Research

* https://link.springer.com/article/10.1007/s11227-020-03368-x : Barina, David
    * Computationak Verification of the Collatz Conjecture up to 2<sup>68</sup>
    * Uses two branches of the conjecture
        * The fast standard map. 
            T(n) = (3n + 1)/2 if n = 1 (mod 2)
            T(n) = n/2        if n = 0 (mod 2)
        * The auxiliary function that follows the same trajectory but always at n + 1
            T<sub>1</sub>(n) = (n + 1)/2 if n = 1 (mod 2)
            T<sub>1</sub>(n) = 3n/2      if n = 0 (mod 2)
    * We notice we can switch between these two branches freely by adding or subtracting 1 from the current number
    * This allows us to create two hybrid maps from the above maps
        * Original
            T(n) = T<sub>1</sub>(n + 1) - 1 if n = 1 (mod 2)
            T(n) = n/2                      if n = 0 (mod 2)
        * Auxiliary
            T<sub>1</sub>(n) = T(n-1) + 1 if n = 1 (mod 2)
            T<sub>1</sub>(n) = 3n/2       if n = 0 (mod 2)
    * Using this hybrid map, we can ensure that we are always on an n (mod 2) = 0 branch
    * This allows us to drastically reduce the number of operations we need to do
        1. Start at every odd number
        2. Begin looping
        3. Add one to transition to the T<sub>1</sub>(n) map
        4. Count traling zeros to determine the power of two that this number may be divided by
        5. n = n * (3<sup>num trailing zeros</sup>/2<sup>num trailing zeros</sup>)   Note that we typically combine multiple loops of a map in this step
        6. n = n - 1 To switch back to standard map
        7. Count trailing zeros in this number
        8. n = n / 2<sup>num trailing zeros</sup>
        9. Check if number is lower than starting number. If not, loop again
    * This algorithm can be used to verify the Collatz Conjecture. We know that if the trajectory of a number goes below its start, it goes to one
    * A sieve apprach was used in combination with this algorithm. Sieve size of 2<sup>24</sup> was used for the GPU implementation

* https://www.ams.org/journals/mcom/1999-68-225/S0025-5718-99-01031-5/S0025-5718-99-01031-5.pdf : Silva, Tomas
    * Presents a range of observations about properties of the Collatz Conejcture
    * Using the last k binary digits of any n, it can be shown what happens in the first k iterations of T(n) aka T<sup>k</sup>()
        * Convert n to form (2*n<sub>1</sub> + r<sub>0</sub>). r<sub>0</sub> is the last binary digit and n<sub>1</sub> is the remaining number
        * It is clear from this that the branch of T(2*n<sub>1</sub> + r<sub>0</sub>) is determined from r<sub>0</sub>
        * If we rewrite n<sub>1</sub> as n<sub>1</sub> + r<sub>1</sub> (r<sub>1</sub> is the second to last base 2 digit of n) we can see that T<sup>2</sup>(n) is determined by the four possible combinations of r<sub>0</sub> and r<sub>1</sub>
        * From this we get T<sup>k</sup>(n) = 3<sup>num odd branches taken</sup>n<sub>k</sub> + T<sup>k</sup>(m<sub>k</sub>)
            For n in the form n = 2<sup>k</sup>n<sub>k</sub> + m<sub>k</sub> | m<sub>k</sub> = n mod 2<sup>k</sup>
        * This simplifies to T<sup>k</sup>(n) = 2 * 3<sup>num odd branches taken</sup>n<sub>k+1<sub> + T<sup>k<sup>(m<sub>k + 1</sub>)
    * Also presents stopping times for numbers of form 2n (stopping time 1) and 4n + 1 (stopping time 2) and others
    * Presents a verification algorithm that only needs to compute open nodes (type 3) and not closed nodes
        * Type 1: Last iteration when checking T<sup>k</sup> resulted in lower value than the initial value
        * Type 2: The last iteration reached a value equal to the initial value 
        * Type 3: Max tree depth was reached without behavior of Type 1 or 2
    * The larger the tree depth, the lower the density of type 3 nodes.
    * This is the basis of the sieve method.


* Naive Verification Speed Up (https://en.wikipedia.org/wiki/Collatz_conjecture)
    * Simple approach to speeding up Collatz Verification. This is based on the manipulation of bits in a base 2 number
    * We know all even numbers are divided by 2 and thus go to a number below them. They can be ignored
    * Append a 1 to the end of the odd binary number (giving 2n + 1)
    * Multiply by n to get 3n + 1
    * Count trailing zeros and remove from the end of the binary number (divide by the highest power of 2 possible)