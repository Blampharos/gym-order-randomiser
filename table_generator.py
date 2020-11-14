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

land_mons_count = len(encounter_fields[0]["encounter_rates"])
water_mons_count = len(encounter_fields[1]["encounter_rates"])
rock_smash_mons_count = len(encounter_fields[2]["encounter_rates"])
fishing_mons_count = len(encounter_fields[3]["encounter_rates"]) #unused
old_rod_mons_count = len(encounter_fields[3]["groups"]["old_rod"])
good_rod_mons_count = len(encounter_fields[3]["groups"]["good_rod"])
super_rod_mons_count = len(encounter_fields[3]["groups"]["super_rod"])

# Reads every second encounter table, the odd ones are Sapphire
ruby_maps = template_encounters["wild_encounter_groups"][0]["encounters"][::2]

locations = []
for i in range(len(ruby_maps)):
    base_label = ruby_maps[i]["base_label"][:-5] # [:-5] Removes "_Ruby"
    if "land_mons" in ruby_maps[i]:
        locations.append(( "{}_LandMons".format(base_label),
                           land_mons_count, () ))
    if "water_mons" in ruby_maps[i]:
        locations.append(( "{}_WaterMons".format(base_label),
                           water_mons_count, () ))
    if "rock_smash_mons" in ruby_maps[i]:
        locations.append(( "{}_RockSmashMons".format(base_label),
                           rock_smash_mons_count, () ))
    if "fishing_mons" in ruby_maps[i]:
        locations.append(( "{}_OldRodMons".format(base_label),
                           old_rod_mons_count, () ))
        locations.append(( "{}_GoodRodMons".format(base_label),
                           good_rod_mons_count, () ))
        locations.append(( "{}_SuperRodMons".format(base_label),
                           super_rod_mons_count, () ))

location_file = StringIO()
location_file.write("[\n")
for i in range(len(locations)):
    comma = ","
    if(i == len(locations) - 1):
        comma = ""
    location_file.write("  {}{}\n".format(dumps(locations[i]), comma))
location_file.write("]")

print(location_file.getvalue())
