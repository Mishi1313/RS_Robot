#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.media.ev3dev import Font


# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

# The server must be started before the client!

from pybricks.messaging import BluetoothMailboxClient, TextMailbox
ev3 = EV3Brick()

# This is the name of the remote EV3 or PC we are connecting to.
SERVER = 'Franz'
munition = 0
ev3.screen.set_font(Font(size=24, bold=True))

client = BluetoothMailboxClient()
mbox = TextMailbox('greeting', client)

print('establishing connection...')
ev3.screen.print("connecting...")
client.connect(SERVER)
print('connected!')
ev3.screen.clear()
ev3.screen.print("connected!")

while True:
    mbox.send(ev3.buttons.pressed())

    if mbox.read() is None:
        munition = 0
    else:
        munition = int(mbox.read())

    ev3.screen.clear()
    if munition is not 0 and Button.CENTER in ev3.buttons.pressed():
        schuss = "Schuss"
        for x in range(12):
            ev3.screen.draw_text(0, 50, (schuss + (x * ". ") ), text_color=Color.BLACK, background_color=None)
            wait(600)
            ev3.screen.clear()
        ev3.screen.draw_text(20, 50, "BOOM!", text_color=Color.BLACK, background_color=None)
        wait(1000)
    else:
        ev3.screen.print("Munition:")
        ev3.screen.print(munition)
        ev3.screen.draw_text(30, 90, "| " * munition, text_color=Color.BLACK, background_color=None)
        wait(100)