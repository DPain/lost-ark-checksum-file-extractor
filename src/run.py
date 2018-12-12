'''
Created on Dec 12, 2018

@author: DPain
'''

import sys
import os
import shutil

WORKSPACE_NAME = "LOSTARK"

ctr = 0

"""
How to run:
python run.py "D:\Games\Games\LOSTARK" "C:\LOSTARK1.0.3.4,46.md5" "C:\LOSTARK1.1.0.2,91.md5"
"""


def main():
    global ctr

    if len(sys.argv) != 4:
        print("Incorrect number of parameters!")
        exit(1)

    game_dir = sys.argv[1]
    old_checksum_dir = sys.argv[2]
    new_checksum_dir = sys.argv[3]

    if game_dir[-1] in ["/", "\\"]:
        game_dir = game_dir[:-1]
        print("Removed trailing slash from game directory")

    print("LOSTARK directory: %s" % game_dir)
    print("MD5 checksum directory: %s" % old_checksum_dir)

    if not os.path.exists(old_checksum_dir):
        print("MD5 checksum file does not exist: %s" % old_checksum_dir)
        exit(1)

    if not os.path.exists(new_checksum_dir):
        print("MD5 checksum file does not exist: %s" % new_checksum_dir)
        exit(1)

    try:
        # Create folder where updated files will go to
        os.mkdir(WORKSPACE_NAME)
    except FileExistsError:
        print(WORKSPACE_NAME + " folder already exists")

    old_hash = dict()
    missing_files = list()

    # Storing MD5s of old version
    with open(old_checksum_dir, 'r') as file:
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
            old_hash[relative_dir] = hash_val.lower()

    # Reading new version's MD5s and copying files
    with open(new_checksum_dir, 'r') as file:
        first_line = file.readline()
        print(first_line)
        index = first_line.find("LOSTARK") + len("LOSTARK")
        if index < 34:
            # 34 = len(32bit MD5 hash) + len(" *")
            print("Possibly a corrupted MD5 hash file from hashcheck!")
            exit(1)
        file.seek(0)

        for line in file:
            hash_val = line[:32].lower()
            relative_dir = line[index:-1]
            print(hash_val, relative_dir)

            old_val = old_hash.get(relative_dir)
            if old_val is None or hash_val != old_val:
                if os.path.exists(game_dir + relative_dir):
                    ctr += 1
                    print("Copied file: " + os.path.basename(relative_dir))
                    copy_file(game_dir, relative_dir)
                else:
                    missing_files.append(relative_dir)
                    print("You do not have a file the new MD5 report has!")
    print("Copied over %d files!" % ctr)
    print("Missing files: \n%s" % str(missing_files))


def copy_file(game_dir, relative_dir):
    os.makedirs(os.path.dirname(WORKSPACE_NAME + relative_dir), exist_ok=True)

    shutil.copy2(os.path.abspath(game_dir + relative_dir),
                 os.path.abspath(WORKSPACE_NAME + relative_dir))


main()
