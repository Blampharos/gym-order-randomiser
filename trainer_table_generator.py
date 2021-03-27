#!/usr/bin/env python3

from pycparser import c_parser, c_ast, parse_file
from json import dump

ast = parse_file("../pokeruby/src/data/trainer_parties.h")
#ast.show()

trainers = []

default_moves_mon_size = 8
custom_moves_mon_size = 16
offset = 0

for trainer_party in ast.children():
    # A trainer_party represents the abstract syntax tree of an array
    # of structs, each struct representing a mon in the trainer's party.
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
    trainer.append(type_declaration.declname)
    #print(trainer)
    trainers.append(trainer)

trainer_table_file = open("trainer_table_generated.json", "wt")
dump(trainers, trainer_table_file, indent="  ")
