#!/usr/bin/python3


import random
from bit import *
from bit.format import bytes_to_wif


print('Bitcoin Addresses Loading Please Wait: ')
filename ='puzzle.txt'
with open(filename) as f:
    line_count = 0
    for line in f:
        line != "\n"
        line_count += 1
with open(filename) as file:
    add = file.read().split()
add = set(add)

h1 = input('Start HEX [exp: 40000000000000000 (67 bits)] : ')
d1 = int(h1, base=16)

h2 = input('End HEX   [exp: 7ffffffffffffffff (67 bits)] : ')
d2 = int(h2, base=16)

count=0
total=0

#start_private_key = 73786976294838206464
#end_private_key = 147573952589676412928
print('\nGood Luck !')
while True:
    magic = hex(random.randint(d1, d2))[2:].zfill(64)
    #print(magic)

    key = Key.from_hex(magic)
    wif=bytes_to_wif(key.to_bytes(),compressed=False)
    key1=Key(wif)
    caddr = key.address

    count+=1
    total+=1
    print(total, magic, caddr, end='\r')


    if caddr in add:

        print ('\n\nTHANKS GOD !! i winn !!\nPrivateKey HEX: ', magic, '\nBitcoin Address Compressed : ', caddr)
        f=open("winner.txt","a")
        f.write('\nPrivateKey (hex): ' + magic)
        f.write('\nBitcoin Address Compressed : ' + caddr)
        f.close()
        exit()

#while True:
#    private_key = np.random.rand(start_private_key, end_private_key)
    #private_key_hex = hex(private_key)[2:] 


#    private_key_hex = hex(private_key)[2:].zfill(64)  # Convert to hexadecimal and zero-fill to 64 characters

    #private_key = random2.randint(min_range, max_range)
#    print(private_key_hex)
