#!/usr/bin/env python

# Define a filename.
filename = "pres_vice_pres.txt"

# read the contestants line by line
with open(filename) as f:
    content = f.readlines()

print(content)

# create list of contestants & parties as tuples
contestants = []
for line in content:
    # remove the newline
    line = line.strip()
    contestant = tuple(map(str, line.split(", ")))
    print(line)
    print(contestant)
    contestants.append(contestant)

print(contestants)
