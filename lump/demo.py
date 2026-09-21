"""Heading on the hub display; LEFT or RIGHT button resets it to 0.

Run: pybricksdev run ble demo.py   (FloorPro on Port.D, gyro on EXT2)
"""

from pybricks.hubs import InventorHub
from pybricks.parameters import Button, Port
from pybricks.tools import multitask, run_task, wait

from gyro import Gyro

hub = InventorHub()
gyro = Gyro(Port.D, Gyro.EXT2)


async def display_loop():
    while True:
        heading = await gyro.heading()
        v = int(heading)
        # The 5x5 display shows two digits: the last two of the heading.
        hub.display.number(v % 100 if v >= 0 else -((-v) % 100))
        await wait(100)


async def button_loop():
    while True:
        pressed = hub.buttons.pressed()
        if Button.LEFT in pressed or Button.RIGHT in pressed:
            await gyro.reset_heading(0.0)
            while hub.buttons.pressed():
                await wait(20)
        await wait(50)


run_task(multitask(display_loop(), button_loop()))
