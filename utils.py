import hashlib
import os
import time
from random import randint


def sha256_hashfile(filename):
    block_size = 65536  # The size of each read from the file

    file_hash = hashlib.sha256()  # Create the hash object, can use something other than `.sha256()` if you wish
    with open(filename, 'rb') as f:  # Open the file to read its bytes
        fb = f.read(block_size)  # Read from the file. Take in the amount declared above
        while len(fb) > 0:  # While there is still data being read from the file
            file_hash.update(fb)  # Update the hash
            fb = f.read(block_size)  # Read the next block from the file

    return file_hash.hexdigest()  # Get the hexadecimal digest of the hash


def sha256(s):
    if not isinstance(s, bytes):
        s = s.encode('ascii')
    m = hashlib.sha256()
    m.update(s)
    return m.hexdigest()


def create_key():
    return sha256(f"{str(randint(1000000000, 9999999999))}{str(randint(1000000000, 9999999999))}"
                  f"{os.getppid()}{os.getpid()}{time.time_ns()}")


def append(filename, _stuff):
    # Open the file in append & read mode ('a+')
    with open(filename, "a+") as file_object:

        appendEOL = False
        # Move read cursor to the start of file.
        file_object.seek(0)
        # Check if file is not empty
        data = file_object.read(100)
        if len(data) > 0:
            appendEOL = True
        # Iterate over each string in the list
        if appendEOL:
            file_object.write("\n")

        file_object.write(_stuff)


def write(filename, _stuff):
    with open(filename, "w") as file_object:
        file_object.write(_stuff)
