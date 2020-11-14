#!/usr/bin/env python3

from pprint import PrettyPrinter
from collections import namedtuple

pp = PrettyPrinter(indent=2)

Location = namedtuple("Location", "name extrareq")
UnlockTable = namedtuple("UnlockTable", "opener locations")

default_unlocks = UnlockTable(
    "default",
    (
        Location( "Route101Land", set(()) ),
        Location( "Route102Land", set(()) ),
    )
)

waterfall_unlocks = UnlockTable(
    "waterfall",
    (
        Location("VictoryRoadLand", set(()) ),
    )
)

rock_smash_unlocks = UnlockTable(
    "rock_smash",
    (
        Location("Route110Land", set(()) ),
        Location("Route117Land", set(()) ),
        Location("Route118Land", set(("acro_bike",)) ),
    )
)

acro_bike_unlocks = UnlockTable(
    "acro_bike",
    (
        Location("Route110Land", set(()) ),
        Location("Route118Land", set(("rock_smash",)) ),
        Location("Route121Land", set(()) ),
    )
)

surf_unlocks = UnlockTable(
    "surf",
    (
        Location("Route110Land", set(()) ),
        Location("Route110Water", set(("rock_smash",)) ),
        Location("Route120Water", set(("acro_bike",)) ),
    )
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

#pp.pprint(default_unlocks[1])
#pp.pprint(rock_smash_unlocks[1:])

pp.pprint(surf_unlocks.opener)

for i in range(len(visit_order)):
    location_tiers.append([])
    unlockers_added.add( unlock_tables[visit_order[i]].opener )

    for location in unlock_tables[visit_order[i]].locations:
        #pp.pprint(location)
        if location.extrareq.issubset(unlockers_added):
            location_tiers[i].append(location.name)
    pass

#pp.pprint(location_tiers)

