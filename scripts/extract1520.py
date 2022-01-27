#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
extract1520.py: Tool to extract the ROM font of a Commodore 1520 plotter

Font data starts at address 1 in ROM, and is 660 bytes long. Each byte
represents a vertex in an 8x8 coordinate space, with the bits used as follows:

    L  X X X  Y Y Y  D

    XXX and YYY represent the X and Y coordinates of the vertex, (0,0) is at
    the bottom left

    L is set to 1 in the last vertex of the character, and 0 otherwise

    D is set to 1 if a line should be drawn to the vertex, 0 to move without
    drawing

The JSON output by this script is a simple mapping of ASCII characters onto a
corresponding list of vertices, with 'x', 'y', and 'draw' attributes
corresponding to the X, Y and D bits of the vertex list (the L bit is not
necessary).

"""

import argparse
import json


# The 1520 character set is not quite ASCII, if the --remap option is given,
# this dictionary provides a mapping onto approximate UTF-8 equivalents for the
# non-standard characters.
ascii_mapping = {0x5c: ord('£'),
                 0x5e: ord('↑'),
                 0x5f: ord('←'),
                 0x60: ord('—'),
                 0x7b: ord('|'),
                 0x7c: ord('_'),
                 0x7d: ord('△'),
                 0x7e: ord('π'),
                 0x7f: ord('□')}


def main():
    parser = argparse.ArgumentParser(
        description='Tool to extract font data from Commodore 1520 plotter '
                    'firmware')
    parser.add_argument('rom_file', help='Commodore 1520 ROM image')
    parser.add_argument('output_json', help="JSON output")
    parser.add_argument('--remap', action='store_true',
                        help='Remap non-ASCII characters')
    args = parser.parse_args()

    with open(args.rom_file, 'rb') as f:
        # Font data is at start of ROM, 660 bytes long, skip first byte
        f.seek(1)
        data = f.read(660)

    # First character is a space, following chars are in ASCII order
    char = ord(' ')

    glyphs = {}
    current_glyph = []

    for b in data:
        # each vertex is represented by one byte - see docstring above
        last = bool(b & 0b10000000)
        x = (b & 0b01110000) >> 4
        y = (b & 0b00001110) >> 1
        draw = bool(b & 0b00000001)

        current_glyph.append({"x": x, "y": y, "draw": draw})
        if last:
            if len(current_glyph) <= 1:
                # Special case for space (no vertices)
                current_glyph = []

            if args.remap:
                actual_char = ascii_mapping.get(char, char)
            else:
                actual_char = char

            glyphs[chr(actual_char)] = current_glyph
            current_glyph = []
            char += 1

    with open(args.output_json, 'w') as out:
        json.dump(glyphs, out, indent=4)


if __name__ == '__main__':
    main()
