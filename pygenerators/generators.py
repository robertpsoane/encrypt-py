# Class for prime generator
from random import randrange, getrandbits

class PrimeGenerator:
    def __init__(self,repeats = False):
        self.repeats = repeats    
        self.primes = []

    def generate(self, size, n_tests = 256):
        # Generating multiple numbers of size until given true
        # Start with a clearly false number to enter loop
        p = 4
        while self.checkPrime(p, n_tests) == False:
            p = self.generateCandidate(size)
            #print('Testing p = {}'.format(p))
        self.primes.append(p)
        return p

    def generateCandidate(self, size):
        # Generating random number of given size.  This is our candidate to be our prime number
        if self.repeats == True:     
            p = getrandbits(size)
            p |= (1<<size-1) | 1
            return p
        else:
            unique = False
            while unique == False:
                p = getrandbits(size)
                p |= (1<<size-1) | 1
                if p in self.primes == False:
                    unique = True
            return p
    
    def checkPrime(self, p, n = 256):
        # Tests whether p is prime by applying k tests
        # Testing 'obvious' cases
        if p == 2 or p == 3:
            return True
        if p <= 1 or p % 2 == 0:
            return False
        
        # Applies Miller-Rabin test
        MR = self.millerRabin(p, n)
        return MR

    def millerRabin(self, p, n):
        # Applies Miller Rabin test n times on p
        # find r and s
        s = 0
        r = p - 1
        while r & 1 == 0:
            s += 1
            r //= 2
        # do n tests
        for _ in range(n):
            a = randrange(2, p - 1)
            x = pow(a, r, p)
            if x != 1 and x != p - 1:
                j = 1
                while j < s and x != p - 1:
                    x = pow(x, 2, p)
                    if x == 1:
                        return False
                    j += 1
                if x != p - 1:
                    return False
        return True

