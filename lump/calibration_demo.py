"""Heading-scale calibration: RIGHT starts, turn exactly one full 360 degree
turn, LEFT stops. The corrected scale is stored on the sensor.

Run: pybricksdev run ble calibration_demo.py   (FloorPro on Port.D, gyro on EXT2)
"""

from pybricks.hubs import InventorHub
from pybricks.parameters import Button, Port
from pybricks.tools import multitask, run_task, wait

from gyro import Gyro

hub = InventorHub()
gyro = Gyro(Port.D, Gyro.EXT2)


async def show_data_loop():
    while True:
        pack = await gyro.data()
        print("pack:", pack, "heading %.2f" % (await gyro.heading()), "status %08b" % pack[4])
        await wait(400)


async def wait_for(button):
    while button not in hub.buttons.pressed():
        await wait(50)
    while hub.buttons.pressed():
        await wait(50)


async def calibration_loop():
    while True:
        print("Press RIGHT to start the heading-scale calibration.")
        await wait_for(Button.RIGHT)
        await gyro.calibration_start()
        print("Calibrating: turn the sensor exactly one full 360 degree turn, then press LEFT.")
        await wait_for(Button.LEFT)
        await gyro.calibration_stop()
        print("Calibration stored.")
        await gyro.reset_heading(0.0)


run_task(multitask(calibration_loop(), show_data_loop(), race=True))
