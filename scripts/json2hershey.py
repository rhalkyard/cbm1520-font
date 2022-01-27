#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json


def encode(val):
    return chr(ord('R') + int(val))


def main():
    parser = argparse.ArgumentParser(
        description='Tool to convert JSON-format Commodore 1520 fonts into '
                    'Hershey JHF')
    parser.add_argument('font_json', help='JSON file with font data')
    parser.add_argument('output', help='JHF output file')
    parser.add_argument('--header', action='store_true',
                        help='Add header with Python HersheyFonts metrics')
    args = parser.parse_args()

    with open(args.font_json) as font:
        glyphs = json.load(font)

    with open(args.output, 'w') as out:
        # Cap line - maximum Y coordinate in all characters
        cap_line = max(max(s['y'] for s in glyphs[glyph])
                       for glyph in glyphs if glyphs[glyph])
        base_line = 1
        bottom_line = 0

        # Left and right margin positions. Since this is a fixed-width font,
        # these are the same for all characters.
        lpos = 0    # since our origin is at the far left
        rpos = 5    # regular chars are all 5 units wide

        if args.header:
            # Write header. Not strictly part of the Hershey font format, but
            # used by the Python HersheyFonts module to define font metrics
            out.write('#{{"define_cap_line": {}, "define_base_line": {}, '
                      '"define_bottom_line": {}}}\n'.format(-cap_line,
                                                            base_line,
                                                            bottom_line))

        for glyph in glyphs:
            glyphnum = ord(glyph)

            output = ''

            for idx, stroke in enumerate(glyphs[glyph]):
                if idx > 0 and not stroke['draw']:
                    # The first vertex is implicitly a travel move. For all
                    # other travel moves, prepend ' R'.
                    output += ' R'

                # Y axis is inverted!
                output += encode(stroke['x']) + encode(-stroke['y'])

            out.write('{: 5}{: 3}{}{}{}\n'.format(glyphnum, len(output)//2,
                                                  encode(lpos), encode(rpos),
                                                  output))


if __name__ == '__main__':
    main()
