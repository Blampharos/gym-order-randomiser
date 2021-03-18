#!/usr/bin/env python3
from struct import pack, unpack
from hmrandomiser import opener_locations, visit_order
from encounter_generator import locations
from io import BytesIO

template_file = open("rubygort.gba", "rb")
output_file = open("rubyranded.gba", "wb")
give_item = (b'\x1a\x00\x80', b'\x1a\x01\x80\x01\x00\x09\x00\x03')
item_ids = (
            b'\x59\x01', # Waterfall
            b'\x56\x01', # Strength
            b'\x58\x01', # Rock Smash
            b'\x03\x01', # Mach Bike
            b'\x53\x01', # Cut
            b'\x10\x01', # Acro Bike
            b'\x55\x01', # Surf
            b'\x5a\x01', # Dive
    )

template = template_file.read()
template_file.close()

# Cross reference data/randable_data.s in the template repo
read_pos = template.find(b"GymFormatStart")
if(read_pos < 0):
    exit()
read_pos += len("GymFormatStart")

version_number = unpack("i", template[read_pos:read_pos + 4])[0]
print("Template revision {}".format(version_number))
if(version_number != 1):
    print("Version number not valid, exiting.")
    exit()
read_pos += 4
gym_format_start = read_pos

opener_scripts = bytearray(b'')
for index in opener_locations:
    opener_scripts.extend(give_item[0])
    opener_scripts.extend(item_ids[index])
    opener_scripts.extend(give_item[1])

#print(opener_scripts)

read_pos += len(opener_scripts)
gym_format_end = read_pos

read_pos = template.find(b"EncounterFormatStart")
enc_format_start = read_pos + len (b"EncounterFormatStart") + 4
print(hex(enc_format_start))

enc_format_end = template.find(b"EncounterFormatEnd")
# this gets us about 2000 extra bytes but whatever
enc_format_length = enc_format_end - enc_format_start

enc_format = BytesIO(template[enc_format_start:enc_format_end])

for location in locations:
    enc_format.seek(location[1])
    #print(location[1])
    if "Route110_WaterMons" == location[0]:
        #print(location)
        pass
    #print(len(location))
    if len(location) == 5:
        #print(location[4])
        for encounter in location[4]:
            enc_format.write(pack("BBH", *encounter))

output_file.write(template[:gym_format_start])
output_file.write(bytes(opener_scripts))
output_file.write(template[gym_format_end:enc_format_start])
output_file.write(enc_format.getvalue())
output_file.write(template[enc_format_end:])

#print(locations)
