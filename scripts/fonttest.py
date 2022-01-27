#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import HersheyFonts
import turtle


def drawtext(font, text, x=0, y=0, size=30):
    font.normalize_rendering(size)
    font.render_options.xofs = x
    font.render_options.yofs = y
    lineslist = font.lines_for_text(text)
    for pt1, pt2 in lineslist:
        turtle.penup()
        turtle.goto(pt1)
        turtle.setheading(turtle.towards(pt2))
        turtle.pendown()
        turtle.goto(pt2)
    turtle.penup()


def main():
    font = HersheyFonts.HersheyFonts()
    font.load_font_file('cbm1520.jhf')

    turtle.mode('logo')
    turtle.tracer(1, 0)
    for coord in range(4):
        turtle.forward(200)
        if coord < 2:
            turtle.stamp()
        turtle.back(200)
        turtle.right(90)
    turtle.color('blue')

    drawtext(font, 'CBM 1520', -425, 200, 150)

    drawtext(font, 'The quick brown fox jumps over the lazy dogs.',
             -470, 180, 5)
    drawtext(font, 'The quick brown fox jumps over the lazy dogs.',
             -470, 160, 10)
    drawtext(font, 'The quick brown fox jumps over the lazy', -470, 130, 15)
    drawtext(font, 'dogs.', -470, 115, 15)

    drawtext(font, 'The quick brown fox', -470, 60, 30)
    drawtext(font, 'jumps over the lazy', -470, 30, 30)
    drawtext(font, 'dogs.', -470, 0, 30)

    drawtext(font, '1234567890-=', 15, 150, 30)
    drawtext(font, '!@#$%^&*()_+', 15, 120, 30)

    drawtext(font, 'Special characters:', 15, 60, 30)
    drawtext(font, '\\ ^ _ ` { | } ~ \x7f', 15, 30, 30)

    drawtext(font, ' !"#$%&\'()*+,-./', -355, -60, 30)
    drawtext(font, '0123456789:;<=>?', 15, -60, 30)
    drawtext(font, '@ABCDEFGHIJKLMNO', -355, -90, 30)
    drawtext(font, 'PQRSTUVWXYZ[\\]^_', 15, -90, 30)
    drawtext(font, '`abcdefghijklmno', -355, -120, 30)
    drawtext(font, 'pqrstuvwxyz{|}~\x7f', 15, -120, 30)

    turtle.penup()
    turtle.hideturtle()
    turtle.goto(0, 0)
    turtle.exitonclick()


if __name__ == '__main__':
    main()
