import asyncio
import logging
from sys import argv

from growattRS232 import GrowattRS232

# defaults
# USB port of RS232 converter
DEFAULT_PORT = "/dev/ttyUSB0"
# Growatt modbus address
DEFAULT_ADDRESS = 0x1

logging.basicConfig(level=logging.DEBUG)


async def main():
    port = str(argv[1]) if len(argv) > 1 else DEFAULT_PORT
    address = int(argv[2]) if len(argv) > 2 else DEFAULT_ADDRESS
    growattRS232 = GrowattRS232(port, address)
    try:
        await growattRS232.async_update()
        print(
            (
                f"Model: {growattRS232.model_number} "
                f"Serial = {growattRS232.serial_number} "
                f"firmware = {growattRS232.firmware}"
            )
        )
        print(f"Sensors data: {growattRS232.data}")
        print(f"Last update: {growattRS232.last_update}")
    except Exception as error:
        print("Error: " + repr(error))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
