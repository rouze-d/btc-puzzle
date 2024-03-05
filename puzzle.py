#!/usr/bin/env python3

# just crack and show compress address
from bit import *
from bit.format import bytes_to_wif
import random
from multiprocessing import Event, Process, Queue, Value, cpu_count

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

print("Total Bitcoin Address Loaded    :",str (line_count))
#x=int(input("Start range Min BITs 0 or Higher (Puzzle StartNumber) -> "))
#a = 2**x
y=int(input("BitCoin Puzzle Bits ( exp: 66 ) : "))
b = 2**y
a = 2**(y-1)
print("Starting search... Please Wait")
print("Min range: " + str(a))
print("Max range: " + str(b))
print("==========================================================")

count=0
total=0
while True:
    ran = random.randrange(a,b)
    seed = str(ran)
    key = Key.from_int(ran)


    wifc = bytes_to_wif(key.to_bytes(), compressed=True) # Compressed WIF
    #wifu = bytes_to_wif(key.to_bytes(), compressed=False) # Uncompressed WIF
    #keyu = Key(wifu)


    caddr = key.address
    #uaddr = keyu.address


    count+=1
    total+=1
    #print ('Total= ',total, key.to_hex(), caddr, end='\n') # ori
    print (total, caddr, key.to_hex(), wifc)#, end='\r')

    if caddr in add:
        print (total, 'Matching Key ==== Found!!!\n PrivateKey DEC: ',seed, '\nMatching Key ==== Found!!!\n PrivateKey HEX: ', key.to_hex(), '\nBitcoin Address Compressed : ', caddr, '\nPrivateKey (wif) Compressed : ', wifc)
        f=open("winner.txt","a")
        f.write('\nPrivateKey (hex): ' + key.to_hex())
        f.write('\nBitcoin Address Compressed : ' + caddr)
        f.write('\nPrivateKey (wif) Compressed : ' + wifc)
        f.close()
        exit()
