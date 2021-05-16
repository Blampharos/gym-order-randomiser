#!/usr/bin/env python3

from pycparser import c_parser, c_ast, parse_file
from json import dump
from glob import glob
from re import sub
from string import digits

ast = parse_file("../pokeruby/src/data/trainer_parties.h")
#ast = parse_file("trainer_parties_trimmed.h")
#ast.show()

map_script_paths = glob('../pokeruby/data/maps/*/scripts.inc')
map_scripts = []
for path in map_script_paths:
    with open(path) as f:
        map_name = path.split("/")[-2] # Probably only works on Unix-likes
        map_scripts.append(( map_name, f.read() ))

#print(map_scripts)
trainers = []

default_moves_mon_size = 8
custom_moves_mon_size = 16
offset = 0

for trainer_party in ast.children():
    # A trainer_party is the abstract syntax tree of an array of structs,
    # each struct representing a mon in the trainer's party.
    trainer = []
    trainer.append(offset)
    type_declaration = trainer_party[1].children()[0][1].children()[0][1]
    # type_declaration holds just the tree for the struct type and the name
    # of the array.

    party_member_count = len(trainer_party[1].children()[1][1].children())
    trainer.append(party_member_count)

    if("Custom" in type_declaration.children()[0][1].name):
        offset += custom_moves_mon_size * party_member_count
        trainer.append(True)
    else:
        offset += default_moves_mon_size * party_member_count
        trainer.append(False)
    if("MonItem" in type_declaration.children()[0][1].name):
        # i.e. has held item
        trainer.append(True)
    else:
        trainer.append(False)

    # Automatically determine some of the trainer locations, better than nothing
    declaration_name = type_declaration.declname[14:]
    trainer.append(declaration_name.rstrip(digits))
    trainer_ssc = sub(r'(?<!^)(?=[A-Z])', '_', trainer[-1]).upper()
    # Arcane regex magic that turns CamelCase into SCREAMING_SNAKE_CASE
    if trainer[-1] != declaration_name:
        trainer_ssc += "_1"
    #print(trainer_ssc)
    for map_tuple in map_scripts:
        map_name = map_tuple[0]
        map_script = map_tuple[1]
        if("TRAINER_{},".format(trainer_ssc) in map_script):
            trainer.append(map_name)
    if(len(trainer) < 6):
        trainer.append("")
    #print(trainer)
    trainers.append(trainer)

trainer_table_file = open("trainer_table_generated.json", "wt")
dump(trainers, trainer_table_file, indent="  ")
