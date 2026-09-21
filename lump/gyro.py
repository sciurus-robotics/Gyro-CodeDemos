"""Gyro on an extension port of a FloorPro, read over LUMP (LEGO hubs, Pybricks).

Over LUMP the FloorPro reports its extension ports inside its mode-0 message:
one 5-byte pack per port (bytes 6..10 for EXT1, 11..15 for EXT2), each
``[data:4][status:1]``. For the gyro the data bytes hold the heading as a
signed 16-bit little-endian value in centi-degrees; the status byte carries the
sensor type in bits 0-1 (2 = gyro), an error flag in bit 3 and "calibration
running" in bit 7.

This driver talks to the FloorPro directly as a ``PUPDevice``, so no other code
is needed next to it. If your program also uses the FloorPro line-sensor driver
on the same port, both objects address the same device; the reads retry on the
occasional ``OSError`` that concurrent access to one PUPDevice can raise.
"""

from pybricks.iodevices import PUPDevice
from pybricks.tools import wait


class Gyro(PUPDevice):
    EXT1 = 1
    EXT2 = 2

    _TYPE_MASK = 0b11
    _TYPE_GYRO = 0b10
    _ERR_MASK = 1 << 3
    _CALIB_MASK = 1 << 7
    _HEADING_SCALE = 100  # centi-degrees

    def __init__(self, port, ext_port=EXT2):
        """Gyro(port, ext_port=Gyro.EXT2)

        port: hub port of the FloorPro; ext_port: the extension port the gyro
        is plugged into (1 or 2). Raises ValueError if that port does not report
        a gyro.
        """
        super().__init__(port)
        if ext_port not in (self.EXT1, self.EXT2):
            raise ValueError("ext_port must be 1 or 2")
        self.ext_port = ext_port
        self._mode0_len = self.info()["modes"][0][1]

    # --- low level ---------------------------------------------------------

    async def _read_mode0(self):
        for attempt in range(10):
            try:
                return await self.read(0)
            except OSError:
                if attempt == 9:
                    raise
                await wait(10)

    async def _send_cmd(self, msg):
        data = [ord(c) for c in msg]
        if len(data) > self._mode0_len:
            raise ValueError("command too long")
        data += [0] * (self._mode0_len - len(data))
        for attempt in range(10):
            try:
                await self.write(0, data)
                return
            except OSError:
                if attempt == 9:
                    raise
                await wait(10)

    async def data(self):
        """The 5-byte extension pack ``(b0, b1, b2, b3, status)`` of the gyro's port."""
        end = 16 - 5 if self.ext_port == self.EXT1 else 16
        raw = (await self._read_mode0())[end - 5:end]
        pack = tuple(b & 0xFF for b in raw)
        if (pack[4] & self._TYPE_MASK) != self._TYPE_GYRO:
            raise ValueError("extension port %d does not report a gyro" % self.ext_port)
        return pack

    # --- readings ------------------------------------------------------------

    async def heading(self):
        """Heading in degrees, (-180.0, 180.0]."""
        pack = await self.data()
        raw = pack[0] | (pack[1] << 8)
        if raw & 0x8000:
            raw -= 0x10000
        return raw / self._HEADING_SCALE

    async def error(self):
        """True while the gyro reports no valid data."""
        return bool((await self.data())[4] & self._ERR_MASK)

    async def calibrating(self):
        """True while the heading-scale calibration is running."""
        return bool((await self.data())[4] & self._CALIB_MASK)

    # --- commands ------------------------------------------------------------

    async def reset_heading(self, angle=0.0):
        """Make the current heading read as ``angle`` (session only, not
        persisted). Resends until the sensor confirms."""
        target = ((angle + 180.0) % 360.0) - 180.0
        if target == -180.0:
            target = 180.0
        while True:
            await self._send_cmd("HEADING=%s" % angle)
            await wait(50)
            diff = abs(((await self.heading()) - target + 180.0) % 360.0 - 180.0)
            if diff < 0.5:
                return

    async def calibration_start(self):
        """Start the heading-scale calibration: turn the sensor exactly one full
        360 degree turn, then call calibration_stop()."""
        while not await self.calibrating():
            await self._send_cmd("IMUCALIBSTART")
            await wait(50)

    async def calibration_stop(self):
        """Stop the calibration; the sensor computes the per-revolution scale
        error from the measured turn and stores it persistently."""
        while await self.calibrating():
            await self._send_cmd("IMUCALIBSTOP")
            await wait(50)
