# LP-Gyro-Extension

Driver and demos for a BNO086 IMU connected to a LEGO Powered Up port via the
[LP-FloorPro-V3](https://github.com/sciurus-robotics/LP-FloorPro-V3-CodeDemos)
extension connector.

## Overview

`GyroSensorExt` reads yaw (heading) data from a BNO086 IMU plugged into one of
the two extension slots on the LP-FloorPro-V3 sensor. It runs on a LEGO
Inventor or SPIKE Prime hub using [Pybricks](https://pybricks.com).

The firmware packs yaw as a signed 16-bit integer in centi-degrees
(range −180.00 ° … +180.00 °) inside the 5-byte extension slot pack. The
driver decodes this and exposes a simple async API.

## Hardware setup

- LP-FloorPro-V3 sensor connected to a hub port (default: `Port.D`)
- BNO086 IMU plugged into extension slot 1 or 2 (default: `EXT2`)

## Files

| File | Description |
|------|-------------|
| `sr_lp_gyro_ext.py` | `GyroSensorExt` driver |
| `floor_pro_v3.py` | Symlink into the LP-FloorPro-V3-CodeDemos submodule |
| `demo.py` | Heading display — left/right button resets heading to 0 |
| `demo_calibration.py` | Yaw-scale calibration procedure |

## API

```python
from floor_pro_v3 import FloorProV3
from sr_lp_gyro_ext import GyroSensorExt

floor_pro = FloorProV3(port=Port.D)
gyro = GyroSensorExt(pup_device=floor_pro, ext_port=FloorProV3.EXT2)
```

### `await gyro.yaw() -> float`
Returns the current heading in degrees, normalized to (−180.0, +180.0].

### `await gyro.error() -> bool`
Returns `True` when the IMU reports no valid data.

### `await gyro.set_heading(target_deg: float)`
Resets the reported heading to `target_deg`. Any real number is accepted;
subsequent readings track the sensor from there and are normalized to
(−180.0, +180.0]. Session-only — not persisted across reboots.

### `await gyro.calibration_start()`
Starts the yaw-scale calibration procedure. After calling this, turn the IMU
exactly one full 360 ° turn, then call `calibration_stop()`.

### `await gyro.calibration_stop()`
Ends calibration, computes the per-revolution gain correction, and persists it
to the firmware's NVS storage.

## Demos

### `demo.py` — heading reset

Displays the current yaw on the hub's 5×5 matrix. Press **left** or **right**
to zero the heading at any time.

### `demo_calibration.py` — yaw-scale calibration

Press **right** to start calibration, turn the robot exactly one full
360 ° turn, then press **left** to stop. The corrected scale factor is saved
and applied automatically on every subsequent boot.

## Submodule

`LP-FloorPro-V3-CodeDemos` is a git submodule. After cloning, run:

```sh
git submodule update --init
```
