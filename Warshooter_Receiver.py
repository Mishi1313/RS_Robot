#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxServer, TextMailbox

import random


# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

# The server must be started before the client!

ev3 = EV3Brick()
TurnMotor = Motor(Port.D, positive_direction=Direction.CLOCKWISE, gears=None)
LoadMotor = Motor(Port.C, positive_direction=Direction.CLOCKWISE, gears=None)
ChargeMotor1 = Motor(Port.B, positive_direction=Direction.CLOCKWISE, gears=[1,24])
ChargeMotor2 = Motor(Port.A, positive_direction=Direction.CLOCKWISE, gears=[1,24])
MagazinSensor = ColorSensor(Port.S1)
server = BluetoothMailboxServer()
mbox = TextMailbox('greeting', server)
buttButtonsPressdons = []
TurnRight = False
RandomVoiceSounds = ["sounds/ZuEinfach.rsf","sounds/Geschenk.rsf","sounds/KommtSofort.rsf",
"sounds/Grossartig.rsf","sounds/Beschuss.rsf","sounds/DruebenAuto.rsf","sounds/DruebenHaus.rsf",
"sounds/Dekung.rsf","sounds/Sperrfeuer.rsf","sounds/Loslos.rsf"]

ev3.speaker.set_speech_options(language="de", voice="m1", speed=14, pitch=40)
ev3.speaker.set_volume(50, which='_all_')

ev3.screen.print("waiting for")
ev3.screen.print("connection...")
server.wait_for_connection()

def ShootCannon():
    if CheckMagazin() == 0:
        ev3.speaker.play_file("sounds/Leergeschossen.rsf")
    else:
        LoadMotor.run_angle(1000, 180, then=Stop.HOLD, wait=True)
        LoadMotor.run_angle(300, 180, then=Stop.HOLD, wait=False)
        ChargeMotor1.run_angle(500, 360, then=Stop.HOLD, wait=False)
        ChargeMotor2.run_angle(500, 360, then=Stop.HOLD, wait=False)
        ev3.speaker.play_file("./sounds/FeuerSchuss.rsf")
        if CheckMagazin() == 0:
            ev3.speaker.play_file("sounds/Leergeschossen.rsf")

def CheckMagazin():
    Reflection = MagazinSensor.reflection()
    if Reflection > 80:
        return 7
    elif Reflection > 50:
        return 6
    elif Reflection > 24:
        return 5
    elif Reflection > 14:
        return 4
    elif Reflection > 9:
        return 3
    elif Reflection > 7:
        return 2
    elif Reflection > 4:
        return 1
    else:
        return 0


while True:
    mbox.wait()
    mbox.send(CheckMagazin())
    ev3.screen.print(mbox.read())
    print(MagazinSensor.reflection())
    ButtonsPressd = mbox.read()[1:-1].split(", ")
    if "Button.UP" in ButtonsPressd:
        ev3.speaker.play_file(random.choice(RandomVoiceSounds))
    if "Button.DOWN" in ButtonsPressd:
        ev3.speaker.play_file("sounds/cannon.rsf")
    if "Button.CENTER" in ButtonsPressd:
        ShootCannon()
    
    if "Button.LEFT" in ButtonsPressd:
        if TurnRight:
            TurnRight = False
            TurnMotor.run(-50)
            ev3.speaker.play_file("sounds/links.rsf")
        else:
            TurnMotor.run(-50)
    elif "Button.RIGHT" in ButtonsPressd:
        if not TurnRight:
            TurnRight = True
            TurnMotor.run(50)
            ev3.speaker.play_file("sounds/rechts.rsf")
        else:
            TurnMotor.run(50)
    else:
        TurnMotor.hold()
