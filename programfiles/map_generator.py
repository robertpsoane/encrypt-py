# Python script to generate dictionaries of encoding mapping.
# This mapping is used to encode any message into an integer

# Function to generate mapping dictionary
def generateMaps():
    symbols = ['`','1','2','3','4','5','6','7','8','9','0','-','=','q','w','e','r','t','y','u','i','o','p','[',']','a','s','d','f','g','h','j','k','l',';','\'','#','\\','z','x','c','v','b','n','m',',','.','/','¬','!','"','£','$','%','^','&','*','(',')','_','+','Q','W','E','R','T','Y,','U','I','O','P','{','}','A','S','D','F','G','H','J','K','L',':','@','~','|','Z','X','C','V','B','N','M','<','>','?','¦','€',' ']

    nums = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', 
    '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97','98']

    symbol2num = {}
    num2symbol = {}

    for k in range(len(symbols)):
        symbol = symbols[k]
        num = nums[k]
        symbol2num[symbol] = num
        num2symbol[num] = symbol
    return symbol2num, num2symbol




'''
######################################
# Function to test mapping           #
######################################
symbol2num, num2symbol = generateMaps()
# Function to test mappings and prove they are one to one
def testMaps(M1, M2):
    mapping_works = True
    # Iterating through each element in M1 and ensuring its ouput maps to itself in M2
    for input in M1:
        M1_out = M1[input]
        M2_out = M2[M1_out]
        if M2_out == input:
            print('Mapping 1 maps {} to {}. Mapping 2 maps {} to {}.  Mapping Works.'.format(input, M1_out, M1_out, M2_out))
        else:
            print('Mapping 1 maps {} to {}. Mapping 2 maps {} to {}.  Mapping Fails.'.format(input, M1_out, M1_out, M2_out))
            mapping_works = False
    if mapping_works == True:
        print('Test Successful')
    else:
        print('Test Failed')

testMaps(symbol2num, num2symbol)
'''