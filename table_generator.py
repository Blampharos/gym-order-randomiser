#!/usr/bin/env python3
"""Helper module for converting template source into generator data

This is a helper module for converting template data into encounter
format data for the encounter generator, it's not meant to be called
from main or any module imported from main. Rather, it's run directly
from the shell.
"""

from json import load, dump, dumps
from pprint import PrettyPrinter
from io import StringIO

pp = PrettyPrinter(indent=2)

wild_encounters_path = "../pokeruby/src/data/wild_encounters.json"

template_encounters_file = open(wild_encounters_path)
template_encounters = load(template_encounters_file)

encounter_fields = template_encounters["wild_encounter_groups"][0]["fields"]

mon_size = 4
land_mons_count = len(encounter_fields[0]["encounter_rates"])*mon_size
water_mons_count = len(encounter_fields[1]["encounter_rates"])*mon_size
rock_smash_mons_count = len(encounter_fields[2]["encounter_rates"])*mon_size
fishing_mons_count = len(encounter_fields[3]["encounter_rates"]) #unused
old_rod_mons_count = len(encounter_fields[3]["groups"]["old_rod"])*mon_size
good_rod_mons_count = len(encounter_fields[3]["groups"]["good_rod"])*mon_size
super_rod_mons_count = len(encounter_fields[3]["groups"]["super_rod"])*mon_size

# Reads every second encounter table, the odd ones are Sapphire
ruby_maps = template_encounters["wild_encounter_groups"][0]["encounters"][::2]

info_size = 8 # Encounter rate and memory address, we're skipping it
locations = []
offset_count = 0
for i in range(len(ruby_maps)):
    base_label = ruby_maps[i]["base_label"][:-5] # [:-5] Removes "_Ruby"
    if "land_mons" in ruby_maps[i]:
        locations.append(( "{}_LandMons".format(base_label),
                           (offset_count, [[]]) ))
        offset_count += land_mons_count + info_size
    if "water_mons" in ruby_maps[i]:
        locations.append(( "{}_WaterMons".format(base_label),
                           (offset_count, [["surf"]]) ))
        offset_count += water_mons_count + info_size
    if "rock_smash_mons" in ruby_maps[i]:
        locations.append(( "{}_RockSmashMons".format(base_label),
                           (offset_count, [["rock_smash",]]) ))
        offset_count += rock_smash_mons_count + info_size
    if "fishing_mons" in ruby_maps[i]:
        locations.append(( "{}_OldRodMons".format(base_label),
                           (offset_count, [["old_rod",]]) ))
        offset_count += old_rod_mons_count
        locations.append(( "{}_GoodRodMons".format(base_label),
                           (offset_count, [["good_rod",]]) ))
        offset_count += good_rod_mons_count
        locations.append(( "{}_SuperRodMons".format(base_label),
                           (offset_count, [["super_rod",]]) ))
        offset_count += super_rod_mons_count + info_size

mach_bike_locations = ["MeteorFalls",
                       "Route111",
                       "Route112",
                       "Route113",
                       "Route114",
                       "Route115",
                       "JaggedPass",
                       "FieryPath",
]

acro_bike_locations = ["Route118",
                       "Route119",
                       "Route120",
                       "Route121",
                       "Route122",
                       "Route123",
                       "SafariZone",
]

rock_smash_locations = ["Route117",
                        "Route118",
                        "Route119",
                        "Route122",
                        "Route123",
                        "NewMauville",
]

surf_locations = ["Route105",
                  "Route107",
                  "Route108",
                  "Route122",
                  "Route123",
                  "Route124",
                  "Route125",
                  "Route126",
                  "Route127",
                  "Route128",
                  "Route129",
                  "Route130",
                  "Route131",
                  "Route132",
                  "Route133",
                  "Route134",
                  "MtPyre",
                  "ShoalCave",
                  "NewMauville",
                  "AbandonedShip",
                  "Pacifidlog",
                  "Mossdeep",
]

dive_locations = ["Sootopolis",
                  "SeafloorCavern",
]

location_file = StringIO()
location_file.write("{\n")
for i in range(len(locations)):
    location_name, location_info = locations[i][0], locations[i][1]
    openers = location_info[1]

    #if any(["Route111" in location_name, "MeteorFalls" in location_name]):
    if any([locname in location_name for locname in mach_bike_locations]):
        openers[0].append("mach_bike")
    if any([locname in location_name for locname in acro_bike_locations]):
        openers[0].append("acro_bike")
    if (any([locname in location_name for locname in rock_smash_locations]) and
        "rock_smash" not in openers[0]):
        openers[0].append("rock_smash")
    if (any([locname in location_name for locname in surf_locations]) and
        "surf" not in openers[0]):
        openers[0].append("surf")
    if any([locname in location_name for locname in dive_locations]):
        openers[0].append("dive")

    comma = ","
    if(i == len(locations) - 1):
        comma = ""
    #location_file.write("  {}{}\n".format(dumps(locations[i]), comma))
    location_file.write('  "{}": {}{}\n'.format( location_name,
                                                 dumps(location_info),
                                                 comma ))
location_file.write("}\n")

print(location_file.getvalue())
location_output = open("unlock_tables_generated.json", "wt")
location_output.write(location_file.getvalue())

location_file.seek(0)
reparsed_locations = load(location_file)

#pp.pprint(locations)
