# -*- coding: utf-8 -*-
#############################################################
#                          IMPORTS                          #
#############################################################
import time
import board
from digitalio import DigitalInOut, Pull
import storage
import neopixel

#############################################################
#                          CONTENT                          #
#############################################################
## NEOPIXEL
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
pixel.fill((0, 0, 0))

## BUTTON
button = DigitalInOut(board.SWITCH)
button.switch_to_input(pull=Pull.DOWN)

if not button.value :
    storage.disable_usb_drive()
    pixel.fill((255, 0, 0))
    time.sleep(0.5)
else :
    pixel.fill((0, 255, 0))
    time.sleep(0.5)