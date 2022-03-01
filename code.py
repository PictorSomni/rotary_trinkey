# -*- coding: utf-8 -*-
#############################################################
#                          IMPORTS                          #
#############################################################
import rotaryio
import board
import usb_hid
import digitalio
import touchio
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import neopixel

#############################################################
#                          CONTENT                          #
#############################################################
print("Rotary Trinkey volume and mute example")

## NEOPIXEL
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
pixel.fill((0, 0, 0))

## ENCODER
encoder = rotaryio.IncrementalEncoder(board.ROTB, board.ROTA)
switch = digitalio.DigitalInOut(board.SWITCH)
switch.switch_to_input(pull=digitalio.Pull.DOWN)
switch_state = None
last_position = encoder.position

## TOUCH
touch = touchio.TouchIn(board.TOUCH)
touch_state = False
counter = 0

## CONSUMER CONTROL
cc = ConsumerControl(usb_hid.devices)

#############################################################
#                         MAIN LOOP                         #
#############################################################
while True:
    current_position = encoder.position
    position_change = current_position - last_position
    if position_change > 0:
        for _ in range(position_change):
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        print(current_position)
    elif position_change < 0:
        for _ in range(-position_change):
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        print(current_position)
    last_position = current_position

    if not switch.value and switch_state is None:
        switch_state = "pressed"

    if switch.value and switch_state == "pressed":
        print("switch pressed.")
        cc.send(ConsumerControlCode.PLAY_PAUSE)
        switch_state = None

    if touch.value and not touch_state:
        touch_state = True
        print("touch")
        pixel.fill((0, 128, 255))
        
        while touch.value :
            if not switch.value and switch_state is None:
                switch_state = "pressed"

            if switch.value and switch_state == "pressed":
                print("switch pressed.")
                counter += 1
                switch_state = None
                
        if counter > 0 :
            print("Counter =  {}".format(counter))
            if counter == 1 :
                print("Next")
                cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)

            elif counter == 2 :
                print("Previous")
                cc.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
                

    if not touch.value and touch_state:
        print("no touch")
        pixel.fill((0, 0, 0))
        touch_state = False
        counter = 0
