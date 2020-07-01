[![PyPI][pypi-releases-shield]][pypi-releases]
[![GitHub issues](https://img.shields.io/github/issues/ArdescoConsulting/growattRS232.svg)](https://GitHub.com/ArdescoConsulting/growattRS232/issues/)

# growattRS232

Python wrapper for getting data asynchonously from Growatt inverters via serial usb RS232 connection and modbus RTU protocol.

The Growatt inverted must support the modbus protocol (some older inverters only support propriatary serial communication)
Connect the RS232 DB9 usb adapter to the RS232 port on the underside of the inverter (you might have to remove a cover plate).

# Attributes
Depending on the firmware version of your inverter, not all attributes might be available

Inverter properties
- serial_number
- model_number
- firmware

DC input PV
- input_power
- input_energy_today

DC input string 1 PV
- input_1_amperage
- input_1_voltage
- input_1_power
- input_1_energy_today
- input_1_energy_total

DC input string 2 PV
- input_2_amperage
- input_2_voltage"
- input_2_power"
- input_2_energy_today"
- input_2_energy_total"

AC output grid
- output_power
- output_energy_today
- output_energy_total
- power_factor
- output_reactive_power
- output_reactive_energy_today
- output_reactive_energy_total

AC output phase 1 grid
- output_1_voltage
- output_1_amperage
- output_1_power

AC output phase 2 grid
- output_2_voltage
- output_2_amperage
- output_2_power

AC output phase 3 grid
- output_3_voltage
- output_3_amperage
- output_3_power

Miscelanuous information
- operation_hours
- frequency
- temperature
- ipm_temperature
- p_bus_voltage
- n_bus_voltage
- derating_mode
- derating

Status, faults & warnings
- status
- status_code
- fault_code
- fault
- warning_code
- warning_value
- warning


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

[pypi-releases]: https://pypi.org/project/growattRS232
[pypi-releases-shield]: https://img.shields.io/pypi/v/growattRS232
