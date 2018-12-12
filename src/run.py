'''
Created on Dec 12, 2018

@author: DPain
'''

import sys
import os
import hashlib
from functools import partial
import shutil

WORKSPACE_NAME = "LOSTARK"

ctr = 0

"""
How to run:
python run.py "D:\Games\Games\LOSTARK" "C:\LOSTARK1.0.3.4,46.md5"
"""


def main():
    if len(sys.argv) != 2:
        print("Incorrect number of parameters!")
        exit(1)

    game_dir = sys.argv[0]
    checksum_dir = sys.argv[1]

    if game_dir[-1] in ["/", "\\"]:
        game_dir = game_dir[:-1]
        print("Removed trailing slash from game directory")

    print("LOSTARK directory: %s" % game_dir)
    print("MD5 checksum directory: %s" % checksum_dir)

    if not os.path.exists(checksum_dir):
        print("MD5 checksum file does not exist: %s" % checksum_dir)
        exit(1)

    try:
        # Create folder where updated files will go to
        os.mkdir(WORKSPACE_NAME)
    except FileExistsError:
        print(WORKSPACE_NAME + " folder already exists")

    # Comparing MD5s now
    with open(checksum_dir, 'r') as file:
        first_line = file.readline()
        print(first_line)
        index = first_line.find("LOSTARK") + len("LOSTARK")
        if index < 34:
            # 34 = len(32bit MD5 hash) + len(" *")
            print("Possibly a corrupted MD5 hash file from hashcheck!")
            exit(1)
        file.seek(0)

        for line in file:
            hash_val = line[:32]
            relative_dir = line[index:-1]
            print(hash_val, relative_dir)
            # print(os.path.dirname(WORKSPACE_NAME + relative_dir))
            print(os.path.abspath(game_dir + relative_dir))

            comparing_file_dir = game_dir + relative_dir
            if os.path.exists(comparing_file_dir):
                your_hash = md5sum(comparing_file_dir)
                if your_hash.lower() != hash_val.lower():
                    copy_file(game_dir, relative_dir)
    print("Copied over %d files!" % ctr)


def md5sum(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()


def copy_file(game_dir, relative_dir):
    global ctr
    ctr += 1
    os.makedirs(os.path.dirname(WORKSPACE_NAME + relative_dir), exist_ok=True)

    shutil.copy2(os.path.abspath(game_dir + relative_dir),
                 os.path.abspath(WORKSPACE_NAME + relative_dir))
    print("Copied file: " + os.path.basename(relative_dir))


main()
