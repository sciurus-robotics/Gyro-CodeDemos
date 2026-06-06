from pybricks.hubs import InventorHub
from pybricks.parameters import Port, Button
from pybricks.tools import wait, run_task, multitask
from floor_pro_v3 import FloorProV3
from sr_lp_gyro_ext import GyroSensorExt

PORT = Port.D
EXT_PORT = FloorProV3.EXT2

floor_pro = FloorProV3(port=PORT)
lp_gyro_ext = GyroSensorExt(pup_device=floor_pro, ext_port=EXT_PORT)

hub = InventorHub()


async def display_loop():
    while True:
        heading = await lp_gyro_ext.heading()
        v = int(heading)
        hub.display.number(v % 100 if v >= 0 else -((-v) % 100))
        await wait(100)


async def button_loop():
    while True:
        pressed = hub.buttons.pressed()
        if Button.LEFT in pressed or Button.RIGHT in pressed:
            await lp_gyro_ext.set_heading(0.0)
            while hub.buttons.pressed():
                await wait(20)
        await wait(50)


run_task(multitask(display_loop(), button_loop()))
