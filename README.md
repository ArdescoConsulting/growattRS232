[![GitHub Release][releases-shield]][releases]
[![PyPI][pypi-releases-shield]][pypi-releases]
[![PyPI - Downloads][pypi-downloads]][pypi-statistics]

# growattRS232

Python wrapper for getting data asynchonously from Growatt inverters via serial usb RS232 connection and modbus RTU protocol.

## How to use package

``` py
import asyncio
import logging
from sys import argv

from growattRS232 import GrowattRS232

# defaults
# USB port of RS232 converter
PORT = "/dev/ttyUSB0"
# Growatt modbus address
ADDRESS = 0x1

logging.basicConfig(level=logging.DEBUG)

async def main():
    port = argv[1] if len(argv) > 1 else PORT
    address = argv[2] if len(argv) > 2 else ADDRESS
    growattRS232 = GrowattRS232(port, address)
    await growattRS232.async_update()
    print(
        f"Model: {growattRS232.model_number}, Serial = {growattRS232.serial_number}, firmware = {growattRS232.firmware}"
    )
    print(f"Sensors data: {growattRS232.data}")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```

[releases]: https://github.com/ArdescoConsulting/growattRS232/releases
[releases-shield]: https://img.shields.io/github/release/ArdescoConsulting/growattRS232.svg?style=popout
[pypi-releases]: https://pypi.org/project/growattRS232
[pypi-statistics]: https://pypistats.org/packages/growattRS232
[pypi-releases-shield]: https://img.shields.io/pypi/v/growattRS232
[pypi-downloads]: https://img.shields.io/pypi/dm/growattRS232
