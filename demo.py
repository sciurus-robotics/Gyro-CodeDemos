from pybricks.hubs import InventorHub
from pybricks.parameters import Port, Button
from pybricks.tools import wait, run_task, multitask
from floor_pro_v3 import FloorProV3
from sr_lp_gyro_ext import GyroSensorExt

PORT = Port.D
# Use EXT1 for the extension sensor data (modes 11-15)
EXT_PORT = FloorProV3.EXT1

floor_pro = FloorProV3(port=PORT)
lp_gyro_ext = GyroSensorExt(pup_device=floor_pro, ext_port=EXT_PORT)

hub = InventorHub()


async def show_data_loop():
    while True:
        data = await lp_gyro_ext.data()
        print("Sensor Raw data:", data)
        print("Sensor Values:", await lp_gyro_ext.str())
        await wait(400)


async def calibration_loop():
    while True:
        print(
            f"Press RIGHT to start yaw-scale calibration of extension port {EXT_PORT}.")
        while True:
            if Button.RIGHT in hub.buttons.pressed():
                break
            else:
                await wait(250)
        await lp_gyro_ext.calibration_start()
        print(
            f"Calibration started. Turn the IMU exactly one full 360 deg turn, then press LEFT to stop.")
        while True:
            if Button.LEFT in hub.buttons.pressed():
                break
            else:
                await wait(250)
        await lp_gyro_ext.calibration_stop()
        print("Calibration stopped.")

        # Re-zero the reported heading after calibration so it starts at 0.
        await lp_gyro_ext.set_heading(0.0)


run_task(multitask(calibration_loop(), show_data_loop(), race=True))
