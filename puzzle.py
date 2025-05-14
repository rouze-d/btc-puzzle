#!/usr/bin/env python3
# https://github.com/rouze-d

import os
import random
import multiprocessing as mp
import time
from secp256k1 import (
    N, privatekey_to_address, privatekey_to_h160,
    check_collision, Load_data_to_memory
)
from termcolor import colored  # For colorful output

# Load target hash160s into memory
Load_data_to_memory("1-160_sorted.bin", verbose=True)

def get_puzzle_bits():
    try:
        y = int(input("Bitcoin Puzzle Bits 1 - 160 (e.g., 71): "))
        if 1 <= y <= 160:
            start = 2 ** (y - 1)
            end = 2 ** y
            print(f"\n{colored(f'Starting search for {y}-bit puzzle (range: {start} to {end-1})', 'green')}")
            print("=" * 60)
            return start, end
        else:
            print(colored("Please enter a value between 1 and 160", 'red'))
    except ValueError:
        print(colored("Invalid input. Please enter a number between 1 and 160", 'red'))
    exit()

# Private key search range (default to full range if no input)
START, END = get_puzzle_bits()

# Multiprocessing config
NUM_PROCESSES = os.cpu_count()
BATCH_SIZE = 100000
PRINT_INTERVAL = 10000

def generate_private_keys(batch_size):
    return [random.randint(START, END - 1) for _ in range(batch_size)]

def worker_proc(shared_data):
    attempts, lock, start_time = shared_data
    keys = generate_private_keys(BATCH_SIZE)

    for pvk in keys:
        h160 = privatekey_to_h160(0, True, pvk)  # addr_type=0, compressed=True
        if check_collision(h160):
            address = privatekey_to_address(0, True, pvk)
            return colored(f"\n[+] MATCH FOUND!\nPrivate Key: {hex(pvk)[2:].zfill(64)}\nAddress: {address}", 'green')

    with lock:
        attempts.value += BATCH_SIZE
        elapsed_time = time.time() - start_time
        speed = attempts.value / elapsed_time if elapsed_time > 0 else 0
        if attempts.value % PRINT_INTERVAL == 0:
            # Show last key and address from batch
            last_key = keys[-1]
            last_address = privatekey_to_address(0, True, last_key)
            print(f"[=] {colored(f'{attempts.value:,}', 'blue')} | Speed: {colored(f'{speed:,.0f} keys/s', 'yellow')} {colored(last_address, 'cyan')} {colored(hex(last_key)[2:].zfill(64), 'magenta')} ", end="\n")

    return None

def main():
    print(f"{colored('[*] Starting', 'green')} {NUM_PROCESSES} processes — Random Brute Force Mode")

    with mp.Manager() as manager:
        attempts = manager.Value('i', 0)
        lock = manager.Lock()
        start_time = time.time()
        shared_data = (attempts, lock, start_time)

        with mp.Pool(NUM_PROCESSES) as pool:
            while True:
                results = pool.map(worker_proc, [shared_data] * NUM_PROCESSES)
                for result in results:
                    if result:
                        print(result)
                        return

if __name__ == "__main__":
    main()
