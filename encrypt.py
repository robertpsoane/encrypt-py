# Main classes for encrypt-py
# Importing PrimeGenerator - Up to date can be found at https://github.com/robertpsoane/py-generators
# Only uses Prime generator which is unlikely to be updated
from pygenerators.generators import PrimeGenerator
from map_generator import generateMaps
import math
from math import gcd

# RSA Encryption Algorithm as described on this website:
# https://brilliant.org/wiki/rsa-encryption/#the-algorithm
class RSAEncryptor:
    def __init__(self):
        self.PrimeGenerator = PrimeGenerator()
        self.encoder = NumericalEncoder()
        self.e = 65537
        self.has_keys = False

    def generateKeys(self, size = 2048):
        valid_primes = False
        while valid_primes == False:
            e = self.e
            p = self.PrimeGenerator.generate(size)
            q = self.PrimeGenerator.generate(size)
            n = p * q
            phi_n = self.phi(p,q)
            if gcd(self.e,phi_n) == 1:
                # We have primes p and q such that (p-1)(q-1) is relatively prime to e
                valid_primes = True
        
        public = {'n':n,'e':e}
        d = self.modInv(e, phi_n)
        private = d
        self.private = private
        self.public = public
        output_string = '####################\nNew Keys Generated\nThe public key will be stored with your encrypted message, you do not need to remember it.\nPlease remember the Private key, as it will be deleted when this application is closed.  YOU WILL NEED IT TO DECRYPT YOUR DATA\nPublic Key: \n - n = {}\n - e = {}\nPrivate Key: {}\n####################'
        print(output_string.format(public['n'],public['e'],private))
        return private, public

    '''
    functions egcd and modInv are from 
    https://brilliant.org/wiki/modular-arithmetic/#modular-arithmetic-as-remainders 
    on modular inverse
    '''
    def egcd(self, a, b):
        x,y, u,v = 0,1, 1,0
        while a != 0:
            q, r = b//a, b%a
            m, n = x-u*q, y-v*q
            b,a, x,y, u,v = a,r, u,v, m,n
        gd = b
        return gd, x, y
    
    def modInv(self, a, m):
        gd, x, y = self.egcd(a, m)
        if gd != 1:
            return None  # modular inverse does not exist
        else:
            return x % m

    def phi(self, p, q):
        return (p - 1) * (q - 1)

    def countBits(self, n):
        # Code from https://www.geeksforgeeks.org/count-total-bits-number/
        # log function in base 2  
        # take only integer part
        return int((math.log(n) / math.log(2)) + 1)

    def inputKeys():
        pass

    # Encrypt Input Function.  Checks if object has keys stored.  If object has no keys stored, 
    # this means first time using object, and will generate new keys to encrypt message.  If the
    # instance has keys stored, this means it has already been given keys to encrypt and decrypt 
    # with and so will just apply the encryption algorithm using those keys.
    def encryptInput(self, message):
        if self.has_keys == False:
            self.message = message
            self.encoded_message = self.encoder.encode(message)
            message_size = self.countBits(self.encoded_message)
            private, public = self.generateKeys(message_size)
            self.private, self.public = private, public
            self.has_keys = True
        
        # Extracting 2 parts to public key
        n = public['n']
        e = public['e']
        print(self.countBits(n))

        # Encoding message using encoder map
        num_message = self.encoder.encode(message)

        encrypted_message = self.powerCongruentModulo(num_message, e, n)
        return encrypted_message

    def decryptStoredKeys(self, ciphertext):
        text_message = self.decrypt(ciphertext, self.private, self.public)
        return text_message

    def decrypt(self, ciphertext, private_key, public_key):
        n = public_key['n']
        e = public_key['e']
        d = private_key

        num_message = self.powerCongruentModulo(ciphertext, d, n)
        text_message = self.encoder.decode(num_message)
        return text_message
    
    def powerCongruentModulo(self, c, d, n):
        # Calculates c^d (mod n) algorithmically
        '''
        This should be a simple problem to solve, simply naively calculate c^d and find c^d (mod n)
        However an example encryption of the message 'Hello World' gives:
         - c = 113802741945749942451993818349977846361705410
         - d = 12092238851321026228006973769204664881579833
         - n = 154120781330032301809611393368946908224360193
        Calculating:
         M = 113802741945749942451993818349977846361705410 ^ (12092238851321026228006973769204664881579833) 
            (mod 154120781330032301809611393368946908224360193)
        Takes a significant amount of time.  Instead we are required to undergo 'Fast Modular Exponentiation'.

        Fast Modular Exponentiation Algorithm
        We let d = d_0 + 2*d_1 + ... + 2^k * d_k, with d_k = 1.
        let a = b = c
        For each i = n-1, n-2, ..., 0:
            if k_i = 1:
                let b = a * b^2 (mod p)
            else:
                let b = b^2 (mod p)
                       
        '''
        # Calculating d expansion
        d_expansion = self.binaryExpansion(d)
        
        d_expansion = d_expansion[1:]
        
        
        a, b = c, c

        for k in d_expansion:
            if k == 1:
                b = (a * pow(b,2)) % n
            else:
                b = pow(b,2) % n
        
        return b     

    def binaryExpansion(self, K):
        # Binary Expansion on k.
        # Returns a list of coefficients K_0, K_1, ..., K_n of 2^0, 2^1, ..., 2^n
        # ie returns number in binary
        can_expand = True
        K_expansion = []
        K_previous = K
        while can_expand == True:
            if K_previous == 1:
                K_expansion.append(1)
                can_expand = False
            else:
                K_i = K_previous % 2
                K_expansion.append(K_i)
                K_previous = K_previous // 2 # Floor division
        binary = K_expansion[::-1]
        return binary
    
    def inverseExpansion(self, expansion, base):
        # Inverts an expansion.  Used to test the binary expansion function
        n = 0
        for k in range(len(expansion)):
            n += expansion[k] * pow(base,k)
        return n


class NumericalEncoder:
    def __init__(self):
        self.letter2num, self.num2letter = generateMaps()

    # Function to encode text message into numerical string using mapping dictionary
    def encode(self,text):
        # Adds a prefix of '1' so that zeros arent lost
        numerical_output_string = '1'
        for character in text:
            numerical_output_string += self.letter2num[character]
        return int(numerical_output_string)

    # Function to decode numerical string using mapping.
    def decode(self,num):
        num = str(num)
        # Removes prefix of 1
        num = num[1:]
        num_chars = int(len(num) / 2)
        
        output_string = ''

        for k in range(num_chars):
            number = num[2*k:2*k+2]
            character = self.num2letter[number]
            output_string += character
        return output_string


RSA = RSAEncryptor()


string_to_encrypt = "Hello World"
print('Encrypting \'{}\''.format(string_to_encrypt))
ciphertext = RSA.encryptInput(string_to_encrypt)
print('Encrypted Message: {}'.format(ciphertext))
private_key = RSA.private
public_key = RSA.public
return_text = RSA.decryptStoredKeys(ciphertext)
print('Decrypted Message: {}'.format(return_text))