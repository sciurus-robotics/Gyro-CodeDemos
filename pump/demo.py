"""Heading on the PeakHub display; LEFT or RIGHT button resets it to 0.
Roll, pitch and yaw are printed once a second.

Run: scirodev run ble demo.py   (FloorPro on Port.A, gyro on EXT2)
"""

from pybricks.tools import multitask, run_task, wait

from sciro.hubs import PeakHub
from sciro.parameters import Button, ExtPort, Port
from sciro.pump import Gyro

hub = PeakHub()
# The gyro is addressed by hub port and extension port; it does not matter
# which PUMP device carries the extension port.
gyro: Gyro = Gyro(Port.A, ExtPort.EXT2)


async def display_loop():
    while True:
        heading = await gyro.heading()
        v = int(heading)
        # The 5x5 display shows two digits: the last two of the heading.
        hub.display.number(v % 100 if v >= 0 else -((-v) % 100))
        await wait(100)


async def print_loop():
    while True:
        roll, pitch, yaw, status = await gyro.read()
        print("roll %7.2f  pitch %7.2f  yaw %7.2f  status 0x%02x" % (roll, pitch, yaw, status))
        await wait(1000)


async def button_loop():
    while True:
        pressed = hub.buttons.pressed()
        if Button.LEFT in pressed or Button.RIGHT in pressed:
            await gyro.reset_heading(0)
            while hub.buttons.pressed():
                await wait(20)
        await wait(50)


async def main():
    await multitask(display_loop(), print_loop(), button_loop())


run_task(main())
