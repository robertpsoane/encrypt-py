# Main classes for encrypt-py
# Importing PrimeGenerator - Up to date can be found at https://github.com/robertpsoane/py-generators
# Only uses Prime generator which is unlikely to be updated
from pygenerators.generators import PrimeGenerator
from programfiles.map_generator import generateMaps
import math
from math import gcd

# RSA Encryption Algorithm as described on this website:
# https://brilliant.org/wiki/rsa-encryption/#the-algorithm
class RSAEncryptor:
    def __init__(self):
        self.PrimeGenerator = PrimeGenerator()
        self.encoder = NumericalEncoder()
        self.e = 65537
        
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

    # Main message encryption functions.  
    # Aims: Break message into K letter strings, encrypt each string with Public
    # key, return fill message encrypted 
    def getPQSize(self, block_size = 10):
        # Used to find a suitable size for p and q
        str_num = ''
        for k in range(block_size+1):
            str_num = str_num + '99'
        max_bits = self.countBits(int(str_num))
        return (max_bits // 2) + 1

    def encryptInBlocks(self, message, public_key, block_size = 10):
        '''
        encryptInBlocks(self, message, block_size = 10, public_key)
        Encrypts message in blocks of size block_size.  Larger block sizes make a 
        harder code to decrypt but take longer to encrypt or decrypt
        public_key = {"n":n, "e":e}
        '''
        split_string = self.splitString(message, block_size)
        encrypted_message = str(public_key['n'])+'#'+str(public_key['e'])+'#'
        for string in split_string:
            encoded_string = self.encoder.encode(string)
            encrypted_string = self.encrypt(public_key['e'], public_key['n'], encoded_string)
            encrypted_message = encrypted_message + str(encrypted_string) + '#'
        
        # Removing extra # from end of message
        encrypted_message = encrypted_message[:-1]
        return encrypted_message
    
    def decryptFromBlocks(self, encrypted_message, private_key):
        split_message = encrypted_message.split('#')
        n, e = int(split_message[0]), int(split_message[1])
        public_key = {'n':n,'e':e}
        split_message = split_message[2:]
        output_text = ''

        # Decrypting in blocks
        for block in split_message:
            block = int(block)
            decrypted_block = self.decrypt(block, private_key, public_key)
            
            output_text = output_text + decrypted_block
        
        return output_text

    def splitString(self, input_string, K):
        # Function to split a string into list of strings of K chars
        string_length = len(input_string)
        if string_length % K == 0:
            n_strings = string_length / K
        else:
            n_strings = (string_length // K) + 1
        split_string = []
        for j in range(n_strings):
            start = j*K
            end = (j+1)*K
            split_string.append(input_string[start:end])
        return split_string
     
    def encrypt(self, e, n, encoded_text):
        encrypted = self.powerCongruentModulo(encoded_text, e, n)
        return encrypted

    def decrypt(self, ciphertext, private_key, public_key):
        n = public_key['n']
        e = public_key['e']
        d = private_key

        num_message = self.powerCongruentModulo(ciphertext, d, n)
        text_message = self.encoder.decode(num_message)
        return text_message
    
    # Mathematical Operation Functions #
    
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


## Testing ##

def testEncryptDecrypt():
    RSA = RSAEncryptor()
    test_secret_message = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In interdum egestas sapien, in vulputate mauris auctor vel. Integer faucibus lacus et justo tempor, sodales vehicula magna laoreet. Phasellus ut consectetur nisl, sit amet congue quam. Proin suscipit ut lacus ut porttitor. Morbi nec interdum nisl. Integer turpis lorem, porttitor egestas quam quis, pulvinar porta tellus. In rutrum nisi mi. Donec luctus, lorem et elementum pharetra, dui erat mollis erat, in ullamcorper ligula nunc ultricies ex. Nullam eu nisi ut nibh vulputate scelerisque sit amet ultrices orci. Vestibulum fermentum ac orci nec interdum. Pellentesque a porta diam, non luctus ipsum. Vestibulum sed nisl tempus, commodo sem at, finibus orci. Nunc in egestas risus, in ultricies mauris. Nam consequat ornare leo, vitae consectetur erat vehicula at. Curabitur purus neque, gravida vitae porttitor id, suscipit sit amet nibh. In accumsan augue sit amet tempor scelerisque. Vestibulum posuere lectus sit amet ligula tristique, quis hendrerit orci placerat. Curabitur laoreet interdum nulla, at commodo quam fermentum eget. Duis sit amet mi eros. Praesent iaculis, velit ac semper porta, nulla risus sodales purus, non porttitor neque velit eget felis. Suspendisse quis varius sapien. Nullam tellus ipsum, elementum ac purus et, ullamcorper euismod elit. Duis mollis efficitur augue quis consectetur. Aliquam vestibulum mauris laoreet lobortis tempus. Maecenas justo justo, placerat non fermentum vel, lacinia sit amet arcu. Nullam eget finibus mauris. Morbi sed suscipit quam, et semper orci. Maecenas et condimentum ligula. Pellentesque felis mi, malesuada ut lacus sed, rhoncus rutrum turpis. Vivamus congue lacinia tempus. Maecenas dictum non nisl at rutrum. Donec nisl arcu, accumsan eget pellentesque eu, molestie sit amet nunc. Donec ligula lectus, laoreet a porttitor sit amet, rutrum ut urna. Aliquam id diam porta, lobortis risus vel, mattis lorem. Praesent imperdiet ligula non mi placerat accumsan. Maecenas lacinia blandit tortor id imperdiet. In risus velit, interdum eget facilisis in, imperdiet ut leo. Cras vestibulum, arcu at aliquet tincidunt, neque nisi lacinia velit, in semper massa sapien eu sapien. Sed vulputate sit amet magna ac pulvinar. Phasellus vitae pulvinar metus. Suspendisse eu faucibus nisi, eu tincidunt nibh. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce tempor ante vel metus tristique, commodo euismod odio congue. In iaculis tincidunt tellus, sed consequat ligula accumsan at. Nulla ultrices felis augue, eget sodales leo venenatis a. Nam eu sapien at justo pretium rutrum aliquam ac tortor. Etiam quis molestie neque. Maecenas eu felis mollis, vehicula eros sed, egestas sem. Aliquam a sem ultrices eros commodo pellentesque. Quisque ut turpis auctor, vulputate justo non, porta velit. Pellentesque euismod dui ex, ac ullamcorper augue pharetra finibus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Morbi varius dolor consequat euismod tincidunt. Morbi maximus imperdiet lorem. Integer lacinia gravida urna eget interdum. Sed eget lacinia tortor. Vestibulum vestibulum, nisl ut egestas lacinia, mauris lacus blandit tellus, ullamcorper pellentesque risus dolor sed turpis. Aliquam in dolor id massa auctor ultricies. Ut id suscipit erat. Sed eleifend commodo nunc sed consectetur. Sed vitae tincidunt velit. Proin finibus nunc eget elementum maximus. Aliquam vehicula convallis turpis, vel ultrices risus dictum et. Pellentesque a nisi eu justo eleifend pulvinar non non felis. Phasellus suscipit mauris sit amet accumsan elementum. Praesent vestibulum, velit vel gravida tempor, ex ante molestie nisi, sed aliquet elit orci in tortor. Suspendisse dapibus eleifend faucibus. Integer nec nibh id mi mattis hendrerit. Morbi eget nunc eu leo egestas finibus. Aliquam vitae sem pretium, porttitor arcu cursus, luctus nulla. Ut placerat, turpis ac imperdiet convallis, odio sem vehicula tortor, quis tempus est urna et ante. Nunc congue varius nisi ut fringilla. Nullam eget ipsum quis arcu gravida facilisis. Nunc pharetra justo in consequat cursus. Nam sit amet imperdiet magna. Integer ornare tellus purus, vel dignissim nunc interdum in. Nunc varius pellentesque metus. Suspendisse potenti. Cras eget euismod lorem. Proin porttitor arcu neque, eget consequat libero posuere eu. Suspendisse urna lacus, tristique efficitur laoreet eu, sodales maximus massa. Sed sodales turpis eget mauris blandit, nec venenatis leo eleifend. Sed velit turpis, efficitur eget libero eget, sollicitudin venenatis tortor. Aliquam convallis rhoncus leo a faucibus. Maecenas viverra quam vel scelerisque ultrices. Duis quis faucibus velit, a accumsan massa. Fusce in arcu id erat volutpat posuere. Nam dignissim metus ut est lobortis scelerisque. Integer euismod sapien elementum ipsum tincidunt molestie. Nam est magna, mattis sit amet tortor sed, dignissim porttitor elit. Pellentesque sed ligula porta, mollis nulla ac, tincidunt leo. Sed at dolor velit. Ut quis dictum urna. Maecenas ex erat, condimentum a suscipit eget, mollis sit amet orci. Cras rhoncus dolor velit. Praesent condimentum et sem id bibendum. Maecenas quis ipsum eget felis egestas accumsan. Donec faucibus nibh sed blandit viverra. Duis a fermentum arcu. Quisque varius non massa sit amet vulputate. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Etiam eget egestas neque. Aliquam erat volutpat. Etiam non augue mauris. Fusce egestas dui in massa efficitur pellentesque gravida quis tortor. Praesent consequat eros et tincidunt egestas. Cras consequat mollis tortor in pretium. Pellentesque mollis condimentum mi, sit amet finibus lacus molestie eu. Vivamus consequat tincidunt faucibus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Quisque a ex ut nisl ullamcorper tempor vel a purus. Aliquam ex metus, eleifend in eleifend id, aliquam et nisl. Integer id sapien eget dui feugiat lobortis. Proin congue, erat vitae commodo vehicula, ex diam vestibulum odio, tincidunt congue purus elit nec diam. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas ut cursus ante. Morbi et lectus eget nisi eleifend laoreet. Aenean consequat accumsan dapibus. Maecenas mattis facilisis nisi nec accumsan. Mauris magna leo, molestie ut nunc in, sollicitudin ultrices eros. Maecenas et est id lacus convallis fermentum sit amet ac diam. Quisque imperdiet tincidunt facilisis. Nullam consectetur convallis placerat. Integer auctor odio quis lacinia malesuada. Praesent fermentum felis blandit ante sodales, et euismod augue ullamcorper. Cras volutpat enim velit, sed molestie lorem varius non. Donec gravida nisl turpis. Cras placerat a magna.'
    key_size = RSA.getPQSize(100)
    private, public = RSA.generateKeys(key_size)
    encrypted_message = RSA.encryptInBlocks(test_secret_message, public, 100)
    decrypted_message = RSA.decryptFromBlocks(encrypted_message, private)
    successful = (decrypted_message == test_secret_message)
    output_string = 'Encryption and Decryption of 1000 words success: {}'.format(successful)
    return output_string, successful

def tests():
    string, boolean = testEncryptDecrypt()
    print(string)


# Uncomment below to run test
# tests()