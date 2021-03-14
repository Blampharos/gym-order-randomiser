#!/usr/bin/env python3

from pprint import PrettyPrinter
from collections import namedtuple
from json import load

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

visit_order = [6, 7, 3, 1, 2, 5, 4, 0]

#location_tiers = []
unlockers_added = set()

locations_file = open("unlock_tables_generated.json", "rt")
locations = load(locations_file)

current_tier = 0
for i in range(len(visit_order)):
    #print( unlockers[visit_order[i]] )
    #print()
    #print( unlockers_added )
    #print()
    for location in locations:
        #print(location)
        if(len(location) == 3):
            for lock in location[2]:
                #print(unlockers_added)
                if set(lock).issubset(unlockers_added):
                    location.append(current_tier)
    unlockers_added.add( unlockers[visit_order[i]] )
    current_tier += 1

#print()
#print(unlockers_added)
#print()
#pp.pprint(locations)
#print(len(locations))
