'''
Created on Dec 15, 2018

@author: DPain
'''

import os
from collections import namedtuple

PatchEntry = namedtuple('PatchEntry', 'index value')


class Patcher:
    
    ROOT_DIR = os.path.join(os.path.split(os.path.abspath(__file__))[0], '../../')
    
    def __init__(self, old_dir, new_dir):
        self.old_dir = old_dir
        self.new_dir = new_dir
        
    def generate_patch(self):
        # Generating patch file
        print("TODO Implement")
    
    def apply_patch(self, game_dir):
        # Applying patch file
        print("TODO Implement")
        
    def test_apply(self):
        entry1 = PatchEntry(index=0x1f, value=0x43)  # b'C' = 0x43
        entry2 = PatchEntry(index=0x20, value=0x6f)  # b'o' = 0x6f
        
        entry_list = list()
        entry_list.append(entry1)
        entry_list.append(entry2)
        
        try:
            with open(os.path.join(self.ROOT_DIR, 'rsc/broken_File.docx'), "rb+") as music_file:
                for e in entry_list:
                    index = e.index if type(e.index) == int else hex(e.index)
                    music_file.seek(index)
                    orig_val = music_file.read(len(e.value) if type(e.value) == bytes else 1)
                    music_file.seek(index)
                    new_val = bytes([e.value]) if type(e.value) == int else e.value
                    music_file.write(new_val)
                    
                    print("%x" % e.index, orig_val, new_val)
                
        except FileNotFoundError:
            print("File does not exist!")
            exit(1)
        
        print("End!")
