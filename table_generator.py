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
                           (offset_count, ()) ))
        offset_count += land_mons_count + info_size
    if "water_mons" in ruby_maps[i]:
        locations.append(( "{}_WaterMons".format(base_label),
                           (offset_count, ("surf",)) ))
        offset_count += water_mons_count + info_size
    if "rock_smash_mons" in ruby_maps[i]:
        locations.append(( "{}_RockSmashMons".format(base_label),
                           (offset_count, ("rock_smash",)) ))
        offset_count += rock_smash_mons_count + info_size
    if "fishing_mons" in ruby_maps[i]:
        locations.append(( "{}_OldRodMons".format(base_label),
                           (offset_count, ("old_rod",)) ))
        offset_count += old_rod_mons_count
        locations.append(( "{}_GoodRodMons".format(base_label),
                           (offset_count, ("good_rod",)) ))
        offset_count += good_rod_mons_count
        locations.append(( "{}_SuperRodMons".format(base_label),
                           (offset_count, ("super_rod",)) ))
        offset_count += super_rod_mons_count + info_size

location_file = StringIO()
location_file.write("{\n")
for i in range(len(locations)):
    comma = ","
    if(i == len(locations) - 1):
        comma = ""
    #location_file.write("  {}{}\n".format(dumps(locations[i]), comma))
    location_file.write('  "{}": {}{}\n'.format( locations[i][0],
                                                 dumps(locations[i][1]),
                                                 comma ))
location_file.write("}\n")

print(location_file.getvalue())

location_file.seek(0)
reparsed_locations = load(location_file)

#pp.pprint(locations)
