## Overview

Assuming a PNG with the correct perspective needs to be cut into a spritesheet
Each tile is 32x40
4 tiles are inside a box of 64x56
- start left: 0x8
- start top: 16x0
- start bottom: 16x16
- start right: 32x8

the next 4 tiles begin x+32 and y+16

test sheet: car_alone_28_1.ase
- red is a box of 4 tiles
- light blue is top and left of a tile
- dark blue is bottom and right of a tile


- start left1: 1x29
- start top1: 17x21
- start bottom1: 17x37
- start right1: 33x29

- start left2: 33x13
- start top2: 49x5
- start bottom2: 49x21
- start right2: 65x13

when moving the red boxes to the left top
then they start at
- box 1 (left): 0x16
- box 2 (right/top): 32x0

a left tile can have a gap in the bottom right
vectors for empty are
from 16x16 to 16x39 and
from 16x16 to 31x9 (2 pixels right then 1 up)

a right tile can have a gap in the bottom left
vectors for empty are
from 15x16 to 15x39 and
from 15x16 to 0x8 (2 pixels left then 1 up)

## What to solve

### Figure out the proportions of the craft

- Draw two lines formed in a triangle to find the bottom part of the image
    - Draw a line from left top to right bottom with 2x/1y
    - Draw a line from top right to left bottom with 2x/1y
    - Do that in an iterate fashion (per single pixel, per 16 pixels?)
    - When there is no intersection/all pixels are empty, then deduce that you found the bottom left/right

- How to draw lines with Pillow? https://pypi.org/project/Pillow/