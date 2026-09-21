# Gyro — Code Demos

Driver code and demo programs for the **Gyro** by Sciurus Robotics: a BNO086
inertial measurement unit reporting roll, pitch and yaw (heading), plugged into
an extension port of the [FloorPro](https://github.com/sciurus-robotics/FloorPro-CodeDemos)
line sensor.

Product information, documentation and firmware downloads: **https://sciro.ch**

## Which folder is yours?

| Your hub | Protocol | Folder |
|---|---|---|
| LEGO Prime / Inventor hub with Pybricks | LUMP (LEGO UART sensor protocol) | [`lump/`](lump/) |
| PeakHub | PUMP (Power UART Multiplex Protocol) | [`pump/`](pump/) |

Over LUMP the gyro's heading rides inside the FloorPro's sensor message; over
PUMP it is a stream of its own with roll, pitch and yaw. The demos in both
folders cover the same ground: heading on the hub display with a button reset,
plus the heading-scale calibration on the LUMP side.

## Requirements

- `lump/`: [Pybricks](https://pybricks.com) firmware on the LEGO hub and
  [`pybricksdev`](https://github.com/pybricks/pybricksdev) to run scripts.
- `pump/`: a PeakHub and the [`scirodev`](https://pypi.org/project/scirodev/)
  package (`pip install scirodev`).

## License

MIT, see [LICENSE](LICENSE).
