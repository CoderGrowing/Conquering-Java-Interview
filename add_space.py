#!/usr/bin/env python3

import os
import sys
import functools


def is_latin(c):
    return ord(c) < 256


# Some characters should not have space on either side.
def allow_space(c):
    return not c.isspace() and not (c in '，。；「」：《》『』、[]（）*_')


def add_space_at_boundry(prefix, next_char):
    if len(prefix) == 0:
        return next_char
    if is_latin(prefix[-1]) != is_latin(next_char) and \
            allow_space(next_char) and allow_space(prefix[-1]):
        return prefix + ' ' + next_char
    else:
        return prefix + next_char


def main():
    base_dir = "."
    md_files = []

    for root, _, files in os.walk(base_dir):
        for name in files:
            if os.path.splitext(name)[1] == ".md":
                md_files.append(os.path.join(root, name))

    for md_file in md_files:
        infile = open(md_file, 'r', encoding="UTF-8")
        instr = infile.read()
        infile.close()

        outstr = functools.reduce(add_space_at_boundry, instr, '')
        print("Add space for: " + os.path.basename(md_file))

        with open(md_file, 'w', encoding="UTF-8") as outfile:
            outfile.write(outstr)

    print("All done.")


if __name__ == '__main__':
    main()