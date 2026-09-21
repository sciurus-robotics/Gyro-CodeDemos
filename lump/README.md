# Gyro on LEGO hubs (Pybricks, LUMP)

Driver and demos for the gyro plugged into an extension port of a FloorPro
that is connected to a LEGO Prime / Inventor hub running
[Pybricks](https://pybricks.com). The FloorPro speaks LEGO's UART sensor
protocol (LUMP) there and reports the gyro's heading inside its own sensor
message, which `gyro.py` decodes through `pybricks.iodevices.PUPDevice`.

## Files

- `gyro.py` — `Gyro(port, ext_port)` driver: `heading()`, `error()`,
  `calibrating()`, `reset_heading(angle)`, `calibration_start()` /
  `calibration_stop()`. Self-contained; the FloorPro line-sensor driver is not
  needed (see [FloorPro-CodeDemos](https://github.com/sciurus-robotics/FloorPro-CodeDemos)
  for that).
- `demo.py` — Heading on the 5x5 display, LEFT/RIGHT button zeroes it
- `calibration_demo.py` — Heading-scale calibration: one full turn between
  RIGHT and LEFT

Run with [`pybricksdev`](https://github.com/pybricks/pybricksdev), e.g.
`pybricksdev run ble demo.py` from this folder (the driver module must sit next
to the script).

## Notes

- Over LUMP only the heading (yaw) is available, as a signed value in
  hundredths of a degree, normalised to (-180, 180].
- `reset_heading()` is session-only; the calibration scale is stored on the
  sensor and applied on every boot.
