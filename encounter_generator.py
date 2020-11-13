#!/usr/bin/env python3

from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2)

default_unlocks = (
    "default",
    ( "Route101Land", set(()) ),
    ( "Route102Land", set(()) ),
)

waterfall_unlocks = (
    "waterfall",
    ("VictoryRoadLand", set(()) ),
)

rock_smash_unlocks = (
    "rock_smash",
    ("Route110Land", set(()) ),
    ("Route117Land", set(()) ),
    ("Route118Land", set(("acro_bike",)) ),
)

acro_bike_unlocks = (
    "acro_bike",
    ("Route110Land", set(()) ),
    ("Route118Land", set(("rock_smash",)) ),
    ("Route121Land", set(()) ),
)

surf_unlocks = (
    "surf",
    ("Route110Land", set(()) ),
    ("Route110Water", set(("rock_smash",)) ),
    ("Route120Water", set(("acro_bike",)) ),
)

unlock_tables = (
    #default_unlocks,
    waterfall_unlocks,
    rock_smash_unlocks,
    acro_bike_unlocks,
    surf_unlocks,
)

visit_order = [1, 2, 3, 0]

location_tiers = []
unlockers_added = set()

for i in range(len(visit_order)):
    location_tiers.append([])
    unlockers_added.add( unlock_tables[visit_order[i]][0] )

    for location in unlock_tables[visit_order[i]][1:]:
        if location[1].issubset(unlockers_added):
            location_tiers[i].append(location[0])
    pass

pp.pprint(location_tiers)

