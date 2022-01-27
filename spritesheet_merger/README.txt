######################################
Merge 2x2 Spritesheets Tool by Buscher
######################################

Version 1.2 (2021-04-03)

#######
Purpose
#######

Put split sprites of 2x2 units together so they fit together with HWP Builder
(https://falkooxc2.pythonanywhere.com/hwpbuild#)

#######
License
#######

MIT for all my stuff.
That means do as you like.
But if the work is going to be credited, that would be appreciated.

############
Requirements
############

This code runs with Python so you obviously need a Python runtime.
(https://www.python.org/downloads/)

You may need to install the PIL (pillow) Python module.


This was tested with Python 2.7.12 and Python 3.5.2


#####
Usage
#####

This is currently a commandline tool without fancy GUI so you have to use it that way for now.
Preferably it would become part of the Falko Tools (https://falkooxc2.pythonanywhere.com)

Put your files into the same folder where the "merge_2x2_spritesheet.py" is. The tool extracts the used palette from the source file. The resulting file will also have the correct size.

- Open your preferred command prompt (cmd or cmder for Windows, any terminal for Linux)
- Path to the directory where the files are (cd)
- Once there run python merge_2x2_spritesheet.py spritesheet.png drawingRoutineNumber
  For example for sentinel_multimelta.png which uses drawingRoutine 5:
        python merge_2x2_spritesheet.py sentinel_multimelta.png 5
- Enjoy your merged spritesheet (in case of the example: merged_sentinel_multimelta.png)


###############
Troubleshooting
###############

There isn't any try catch or any error handling yet. 
Maybe it's not necessary as it should either work or not work.

Please let me know if you run into any issues. Currently I am available in 
the OpenXcom discord (https://discord.gg/HWMYxNHB)
and the OpenXcom 40k discord (https://discord.gg/w8kPJ27R)

Of course I am also interested in any feedback. Thanks!

#######
CREDITS
#######

And the great people who made
- Ufopaedia wiki
- OpenXcom
- OpenXcom Extended

Thanks to all of them!
