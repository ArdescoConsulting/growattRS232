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
