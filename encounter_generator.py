#!/usr/bin/env python3

from pprint import PrettyPrinter
from collections import namedtuple
from json import load
from random import randint
from hmrandomiser import visit_order
from io import BytesIO
from struct import pack

#print(visit_order)
pp = PrettyPrinter(indent=2)

unlockers = (
    "waterfall",
    "strength",
    "rock_smash",
    "mach_bike",
    "cut",
    "acro_bike",
    "surf",
    "dive",
)

#location_tiers = []
unlockers_added = set()

locations_file = open("unlock_tables_generated.json", "rt")
locations = load(locations_file)

current_tier = 0
for i in range(len(visit_order)):
    for location in locations:
        #print(location)
        if(len(location) == 3):
            for lock in location[2]:
                #print(unlockers_added)
                if set(lock).issubset(unlockers_added):
                    location.append(current_tier)
                    break # otherwise it will add the tier value multiple times
    unlockers_added.add( unlockers[visit_order[i]] )
    current_tier += 1
    unlockers_added.add( "old_rod" )
    if("acro_bike" in unlockers_added or
       "rock_smash" in unlockers_added or
       "surf" in unlockers_added):
        unlockers_added.add("good_rod")
    if("acro_bike" in unlockers_added and
       "rock_smash" in unlockers_added and
       "surf" in unlockers_added):
        unlockers_added.add("super_rod")
    print(unlockers_added)

threetally = 0
fourtally = 0
enc_amt = 0
for location in locations:
    #print(location)
    if len(location) == 4:
        fourtally += 1
        location.append([])
        if("Land" in location[0]):
            enc_amt = 12
        if("Water" in location[0]):
            enc_amt = 5
        if("RockSmash" in location[0]):
            enc_amt = 5
        for i in range(enc_amt):
            location[4].append([])
            location[4][i].append(int(14 + 2.5 * location[3]))
            location[4][i].append(int(16 + 2.5 * location[3]))
            location[4][i].append(randint(1,251))
        #print(location)
    else:
        threetally += 1
    #print(location)

#print(locations)

#print((threetally, fourtally))

#pp.pprint(locations)
#print(len(locations))
