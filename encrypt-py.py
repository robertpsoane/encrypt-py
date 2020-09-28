# Main classes for encrypt-py
# Importing PrimeGenerator - Up to date can be found at https://github.com/robertpsoane/py-generators
# Only uses Prime generator which is unlikely to be updated
from pygenerators.generators import PrimeGenerator
from map_generator import generateMaps
import math

# RSA Encryption Algorithm as described on this website:
# https://brilliant.org/wiki/rsa-encryption/#the-algorithm
class RSAEncryptor:
    def __init__(self):
        self.PrimeGenerator = PrimeGenerator()

    def generateKeys(self, size):
        self.PrimeGenerator.generate(size)
        private = 5
        print('Private Key = {}.  Please write this down as it will not be stored once this script is closed.'.format(private))
        self.private = private
        self.public = public
        return private, public
    
    def countBits(self, n):
        # Code from https://www.geeksforgeeks.org/count-total-bits-number/
        # log function in base 2  
        # take only integer part
         
        return int((math.log(n) / math.log(2)) + 1)

    def encrypt(self, message):
        pass

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
        print(num_chars)
        
        output_string = ''

        for k in range(num_chars):
            number = num[2*k:2*k+2]
            character = self.num2letter[number]
            output_string += character
        return output_string


