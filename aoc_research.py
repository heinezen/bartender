#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_research.py: researches """ 
from pymemory import pymemory as pm
from aoc_time import GTime

class Research(object):
    """
    Attributes
        public
            owner           `Player` struct
            ptr_times       Pointer to timers
            length          Length of research struct (should be constant to all players)
            ptr_researches  Pointer to researches # common to all players
            id_list         Currently researched techs - id list
            progression     Currently researched techs
            done            Technologies done
        method
            __init__        Construcotr, requires owner (`Player` struct) as argument
            add             Adds an research into the id_list ((called in file `aoc_object_building_research.py`))
            update          Updates times

    """
    def __init__(self, owner):
        super(Research, self).__init__()
        self.owner = owner
        ptr = pm.pointer(owner.ptr + 0x1ae8)
        self.ptr_times = pm.pointer(ptr) # struct size: 0x10 
        self.length = pm.int32(ptr + 0x4)
        self.ptr_researches  = pm.pointer(pm.pointer(ptr + 0x8))   # struct size: 0x54 
        self.id_list = []
        self.progression = []
        self.done = []
        # self.ptr_researches should be the same address for each plaeyr

    def add(self, id):
        if id not in self.id_list:
            self.id_list.append(id)
            

    def update(self):
        self.progression.clear()
        delete = []
        for id in self.id_list:
            time = pm.float(self.ptr_times + 0x10 * id)
            total_time = pm.int16(self.ptr_researches + 0x54*id + 0x26)
            icon = pm.int16(self.ptr_researches  + 0x54*id + 0x2C)
            cooldown = total_time - time
            if time == 0.0:
                delete.append(id)
            elif total_time > time:
                self.progression.append([id, icon, time, total_time, cooldown])
            else:
                self.done.append([id, icon, GTime.time])
                delete.append(id)
        for id in delete: 
            self.id_list.remove(id)

if __name__ == '__main__':
    import bartender
    exit(1)
    from aoc_game import Game 
    proc_name = "AoK HD.exe"
    pm.load_process(proc_name)
    with pm:
        game = Game()
        game.update()



        