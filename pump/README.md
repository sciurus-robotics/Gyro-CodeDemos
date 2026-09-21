# Gyro on the PeakHub (PUMP)

Demos for the gyro on an extension port of a PUMP device (today: the FloorPro)
connected to a PeakHub. The `sciro.pump.Gyro` class is built into the PeakHub
firmware; no driver file is needed next to the scripts.

## Setup

```
pip install scirodev            # the scirodev command + the sciro API stubs
scirodev run ble demo.py        # runs a script on the hub over Bluetooth
```

## Files

- `demo.py` — Heading on the 5x5 display, LEFT/RIGHT button zeroes it; roll,
  pitch and yaw printed once a second

## API in one look

```python
from sciro.parameters import ExtPort, Port
from sciro.pump import Gyro

gyro = Gyro(Port.A, ExtPort.EXT2)     # or FloorPro(Port.A).gyro(2)
roll, pitch, yaw, status = gyro.read()  # degrees
heading = gyro.heading()              # yaw with the hub-side offset, (-180, 180]
gyro.reset_heading(0)                 # make the current heading read as 0
gyro.subscribe(PUMPDevice.PERIODIC, 50)  # 50 Hz instead of the default 100 Hz
```

Every reading method also works with `await` under `run_task` / `multitask`.

## Notes

- Over PUMP the sensor streams roll, pitch and yaw at 100 Hz by default; the
  heading offset lives on the hub (`reset_heading()`), so it is per program.
- The heading-scale calibration (one full turn) is only available over LUMP for
  now, see [`../lump/`](../lump/); the stored scale applies over PUMP too.
