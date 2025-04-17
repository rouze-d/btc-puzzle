#!/usr/bin/env python3

from bit import Key
from bit.format import bytes_to_wif
import random
import os
from multiprocessing import Process, cpu_count, Event
import time

# Config
ADDRESS_FILE = 'puzzle.txt'
WINNER_FILE = 'winner.txt'
PRINT_INTERVAL = 1000  # Print status every N attempts per worker

# Load address set
def load_addresses(filename):
    with open(filename) as f:
        addresses = set(line.strip() for line in f if line.strip())
    print("Total Bitcoin Addresses Loaded:", len(addresses))
    return addresses

# Worker function
def worker(addresses, a, b, stop_event, worker_id):
    attempts = 0
    while not stop_event.is_set():
        ran = random.randrange(a, b)
        key = Key.from_int(ran)
        wifc = bytes_to_wif(key.to_bytes(), compressed=True)
        caddr = key.address

        if caddr in addresses:
            print(f"[WORKER-{worker_id}] MATCH FOUND!")
            with open(WINNER_FILE, 'a') as f:
                f.write(f'\n[WORKER-{worker_id}] PrivateKey (DEC): {ran}')
                f.write(f'\nPrivateKey (HEX): {key.to_hex()}')
                f.write(f'\nBitcoin Address (Compressed): {caddr}')
                f.write(f'\nPrivateKey (WIF): {wifc}\n\n')
            stop_event.set()
            break

        attempts += 1
        if attempts % PRINT_INTERVAL == 0:
            print(f"[WORKER-{worker_id}] Attempts: {attempts} | Addr: {caddr} | Priv: {key.to_hex()}")

# Main
def main():
    y = int(input("BitCoin Puzzle Bits ( exp: 66 ) : "))
    a = 2**(y - 1)
    b = 2**y

    print("Starting search with multiprocessing...")
    print(f"Range: {a} to {b}")
    print("==========================================================")

    addresses = load_addresses(ADDRESS_FILE)
    stop_event = Event()

    workers = []
    for i in range(cpu_count()):
        p = Process(target=worker, args=(addresses, a, b, stop_event, i))
        p.start()
        workers.append(p)

    try:
        for p in workers:
            p.join()
    except KeyboardInterrupt:
        print("\nStopping all workers...")
        stop_event.set()
        for p in workers:
            p.terminate()

if __name__ == "__main__":
    main()
