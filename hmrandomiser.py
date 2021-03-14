#!/usr/bin/env python

from random import seed, shuffle, randint

visibleseed = randint(0,1000000000)
print(visibleseed)
seed(visibleseed)

opener_locations = [0,0,0,0,0,0,0,0]

openers = [1, 2, 3, 4, 5, 6]

badge_locations = [0,0,0,0,0,0,0,0]

shuffle(openers)

curropener = 0
prevopener = 0
badgeiter = 0

visit_order = []

while openers:
    curropener = openers.pop()
    if curropener == 6:
        openers.append(7)
        shuffle(openers)
    #print(curropener)
    badgeiter += 1
    badge_locations[curropener] = badgeiter
    opener_locations[prevopener] = curropener
    visit_order.append(curropener)
    prevopener = curropener

opener_locations[prevopener] = 0
visit_order.append(0)

print(opener_locations)
#print(badge_locations)
print(visit_order)
#print(openers)
