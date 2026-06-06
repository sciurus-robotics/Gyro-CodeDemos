from pybricks.tools import wait
from floor_pro_v3 import FloorProV3


class GyroSensorExt:
    IMUCALIBSTART = "IMUCALIBSTART"
    IMUCALIBSTOP = "IMUCALIBSTOP"

    TYPE_MASK = 0b11
    TYPE_IMU = 0b10

    ERR_MASK = 1 << 3

    CALIB_RUNNING_MASK = 1 << 7
    CALIB_RUNNING = 1 << 7

    # Firmware packs heading as int16 centi-degrees (degrees * 100), little-endian.
    HEADING_SCALE = 100

    def __init__(self, pup_device: FloorProV3, ext_port=1):
        # TODO we require FloorProV3 at this time because it is currently the only PUPDevice that supports the necessary ext_port_data() method;
        # this should be more generic or just rely on duck typing entirely
        self.pup_device = pup_device
        if ext_port not in (1, 2):
            raise ValueError("ext_port must be 1 or 2")
        self.ext_port = ext_port

    async def data(self):
        data = await self.pup_device.ext_port_data(self.ext_port)
        if (data[4] & self.TYPE_MASK) != self.TYPE_IMU:
            raise ValueError(
                f"Data from extension port {self.ext_port} does not match expected IMU sensor format.")
        return data

    async def heading(self):
        """ Returns the current heading in degrees as a float in the range (-180.0, 180.0]. """
        data = await self.data()
        raw = data[0] | (data[1] << 8)
        if raw & 0x8000:
            raw -= 0x10000
        return raw / self.HEADING_SCALE

    async def error(self) -> bool:
        """ Returns True if the IMU is reporting an error / no valid data. """
        data = await self.data()
        return (data[4] & self.ERR_MASK) == self.ERR_MASK

    async def str(self):
        data = await self.data()
        heading = await self.heading()
        return f"GyroSensorExt(ext_port={self.ext_port}, heading={heading:.2f} deg, {data[4]:08b})"

    async def set_heading(self, target_deg: float):
        """ Reset the reported heading (yaw) to ``target_deg``. Session-only — not persisted across reboots.

        ``target_deg`` may be any real number; subsequent readings track the sensor
        from there and are normalized into (-180.0, 180.0].

        Retries until confirmed: immediately after the firmware applies the reset
        the reported heading must equal ``target_deg`` (normalized), so a small
        angular deviation is used as confirmation.
        """
        t = ((target_deg + 180.0) % 360.0) - 180.0
        if t == -180.0:
            t = 180.0
        while True:
            await self.pup_device.send_cmd(f"HEADING={target_deg}")
            await wait(50)
            diff = abs(((await self.heading() - t) + 180.0) % 360.0 - 180.0)
            if diff < 0.5:
                break

    async def calibration_start(self):
        """ Start the yaw-scale calibration process. Turn the IMU exactly one full 360 deg turn, then call ``calibration_stop()``. """
        while (await self.data())[4] & self.CALIB_RUNNING_MASK != self.CALIB_RUNNING:
            await self.pup_device.send_cmd(self.IMUCALIBSTART)
            await wait(50)

    async def calibration_stop(self):
        """ Stop the yaw-scale calibration, compute the per-revolution gain error from the measured turn, and persist it. """
        while (await self.data())[4] & self.CALIB_RUNNING_MASK == self.CALIB_RUNNING:
            await self.pup_device.send_cmd(self.IMUCALIBSTOP)
            await wait(50)
