#!/usr/bin/env python3

from pprint import PrettyPrinter
from collections import namedtuple
from json import load

pp = PrettyPrinter(indent=2)

Location = namedtuple("Location", "name extrareq")
UnlockTable = namedtuple("UnlockTable", "opener locations")

def as_unlock_table(dict_):
    """Object hook for JSON decoder

    Example UnlockTable produced:
    UnlockTable(
        "rock_smash",
        (
            Location("Route110Land, set() ),
            Location("Route118Land, set(("acro_bike",)) )
        )
    )
    """
    if "opener" in dict_:
        return UnlockTable(
            dict_["opener"],
            tuple(dict_["locations"])
        )
    elif "extrareq" in dict_:
        return Location( dict_["name"], set( dict_["extrareq"] ) )
    return dict_

unlock_tables_file = open("unlock_tables.json")
json_unlock_tables = load(unlock_tables_file, object_hook=as_unlock_table)

#pp.pprint(json_unlock_tables["rock_smash_unlocks"])

unlock_tables = (
    #json_unlock_tables["default_unlocks"],
    json_unlock_tables["waterfall_unlocks"],
    json_unlock_tables["rock_smash_unlocks"],
    json_unlock_tables["acro_bike_unlocks"],
    json_unlock_tables["surf_unlocks"],
)

visit_order = [1, 2, 3, 0]

location_tiers = []
unlockers_added = set()

for i in range(len(visit_order)):
    location_tiers.append([])

    unlock_table = unlock_tables[visit_order[i]]
    unlockers_added.add( unlock_table.opener )

    for location in unlock_table.locations:
        #pp.pprint(location)
        if location.extrareq.issubset(unlockers_added):
            location_tiers[i].append(location.name)
    pass

pp.pprint(location_tiers)

