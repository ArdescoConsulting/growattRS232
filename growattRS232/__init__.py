"""
Python wrapper for getting data asynchronously from Growatt inverters
via serial usb RS232 connection and modbus RTU protocol.
"""
import logging
import os

from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ConnectionException, ModbusException
from pymodbus.pdu import ExceptionResponse

from growattRS232.const import (
    ATTR_DERATING,
    ATTR_DERATING_MODE,
    ATTR_FAULT,
    ATTR_FAULT_CODE,
    ATTR_FIRMWARE,
    ATTR_FREQUENCY,
    ATTR_INPUT_1_AMPERAGE,
    ATTR_INPUT_1_ENERGY_TODAY,
    ATTR_INPUT_1_ENERGY_TOTAL,
    ATTR_INPUT_1_POWER,
    ATTR_INPUT_1_VOLTAGE,
    ATTR_INPUT_2_AMPERAGE,
    ATTR_INPUT_2_ENERGY_TODAY,
    ATTR_INPUT_2_ENERGY_TOTAL,
    ATTR_INPUT_2_POWER,
    ATTR_INPUT_2_VOLTAGE,
    ATTR_INPUT_ENERGY_TODAY,
    ATTR_INPUT_POWER,
    ATTR_IPM_TEMPERATURE,
    ATTR_MODEL_NUMBER,
    ATTR_N_BUS_VOLTAGE,
    ATTR_OPERATION_HOURS,
    ATTR_OUTPUT_1_AMPERAGE,
    ATTR_OUTPUT_1_POWER,
    ATTR_OUTPUT_1_VOLTAGE,
    ATTR_OUTPUT_2_AMPERAGE,
    ATTR_OUTPUT_2_POWER,
    ATTR_OUTPUT_2_VOLTAGE,
    ATTR_OUTPUT_3_AMPERAGE,
    ATTR_OUTPUT_3_POWER,
    ATTR_OUTPUT_3_VOLTAGE,
    ATTR_OUTPUT_ENERGY_TODAY,
    ATTR_OUTPUT_ENERGY_TOTAL,
    ATTR_OUTPUT_POWER,
    ATTR_OUTPUT_POWER_FACTOR,
    ATTR_OUTPUT_REACTIVE_ENERGY_TODAY,
    ATTR_OUTPUT_REACTIVE_ENERGY_TOTAL,
    ATTR_OUTPUT_REACTIVE_POWER,
    ATTR_P_BUS_VOLTAGE,
    ATTR_SERIAL_NUMBER,
    ATTR_STATUS,
    ATTR_STATUS_CODE,
    ATTR_TEMPERATURE,
    ATTR_WARNING,
    ATTR_WARNING_CODE,
    ATTR_WARNING_VALUE,
    DEFAULT_ADDRESS,
    DEFAULT_PORT,
    DERATINGMODES,
    FAULTCODES,
    STATUSCODES,
    WARNINGCODES,
)

_LOGGER = logging.getLogger(__name__)


def rssf(rr, index, scale=10):
    # Read and scale single to float
    return float(rr.registers[index]) / scale


def rsdf(rr, index, scale=10):
    # Read and scale double to float
    return float((rr.registers[index] << 16) + rr.registers[index + 1]) / scale


class GrowattRS232:
    """Main class to communicate with the Growatt inverter."""

    def __init__(self, port=DEFAULT_PORT, address=DEFAULT_ADDRESS):
        # Inverter properties
        self.serial_number = ""
        self.model_number = ""
        self.firmware = ""

        # Inverter data
        self.data = {}

        # usb port
        self._port = port
        # Modbus address (1-247)
        self._unit = address
        # Modbus serial rtu communication client
        self._client = ModbusClient(
            method="rtu",
            port=port,
            baudrate=9600,
            stopbits=1,
            parity="N",
            bytesize=8,
            timeout=1,
        )

        _LOGGER.debug(
            f"GrowattRS232 using usb port {self._port} \
            and modbus address {self._unit}"
        )

    async def async_update(self):
        """Read Growatt data."""

        data = {}

        """
        Modbus rtu information from
        "Growatt PV Inverter Modbus RS485 RTU Protocol V3.14 2016-09-27".
        The availability of the attributes depends
        on the firmware version of your inverter.
        """

        if not os.path.exists(self._port):
            self.data = {}
            raise PortError(f"USB port {self._port} is not available")

        self._client.timeout = True
        if not self._client.connect():
            self.data = {}
            raise ModbusError("Modbus connection failed.")

        try:
            if self.serial_number == "":
                rhr = self._client.read_holding_registers(
                    0, 30, unit=self._unit
                )

                if isinstance(rhr, (ModbusException, ExceptionResponse)):
                    raise ModbusError("Modbus read failed")

                if not rhr.isError():
                    self.firmware = str(
                        chr(rhr.registers[9] >> 8)
                        + chr(rhr.registers[9] & 0x000000FF)
                        + chr(rhr.registers[10] >> 8)
                        + chr(rhr.registers[10] & 0x000000FF)
                        + chr(rhr.registers[11] >> 8)
                        + chr(rhr.registers[11] & 0x000000FF)
                    )

                    self.serial_number = str(
                        chr(rhr.registers[23] >> 8)
                        + chr(rhr.registers[23] & 0x000000FF)
                        + chr(rhr.registers[24] >> 8)
                        + chr(rhr.registers[24] & 0x000000FF)
                        + chr(rhr.registers[25] >> 8)
                        + chr(rhr.registers[25] & 0x000000FF)
                        + chr(rhr.registers[26] >> 8)
                        + chr(rhr.registers[26] & 0x000000FF)
                        + chr(rhr.registers[27] >> 8)
                        + chr(rhr.registers[27] & 0x000000FF)
                    )

                    mo = (rhr.registers[28] << 16) + rhr.registers[29]
                    self.model_number = (
                        "T"
                        + str((mo & 0xF00000) >> 20)
                        + " Q"
                        + str((mo & 0x0F0000) >> 16)
                        + " P"
                        + str((mo & 0x00F000) >> 12)
                        + " U"
                        + str((mo & 0x000F00) >> 8)
                        + " M"
                        + str((mo & 0x0000F0) >> 4)
                        + " S"
                        + str((mo & 0x00000F))
                    )

                    _LOGGER.debug(
                        f"GrowattRS232 with serial number {self.serial_number} \
                            is model {self.model_number} \
                            and has firmware {self.firmware}"
                    )
                else:
                    self.data = {}
                    self.firmware = ""
                    self.serial_number = ""
                    self.model_number = ""
                    self._client.close()
                    raise ModbusError("Modbus read failed")

            rir1 = self._client.read_input_registers(0, 44, unit=self._unit)
            if rir1.isError():
                raise ModbusError("Modbus read failed")

            rir2 = self._client.read_input_registers(45, 21, unit=self._unit)
            if rir2.isError():
                raise ModbusError("Modbus read failed")

            # Inverter properties
            data[ATTR_SERIAL_NUMBER] = self.serial_number
            data[ATTR_MODEL_NUMBER] = self.model_number
            data[ATTR_FIRMWARE] = self.firmware

            # DC input PV
            data[ATTR_INPUT_POWER] = rsdf(rir1, 1)
            data[ATTR_INPUT_ENERGY_TODAY] = rsdf(rir2, 11)

            # DC input string 1 PV
            data[ATTR_INPUT_1_VOLTAGE] = rssf(rir1, 3)
            data[ATTR_INPUT_1_AMPERAGE] = rssf(rir1, 4)
            data[ATTR_INPUT_1_POWER] = rsdf(rir1, 5)
            data[ATTR_INPUT_1_ENERGY_TODAY] = rsdf(rir2, 3)
            data[ATTR_INPUT_1_ENERGY_TOTAL] = rsdf(rir2, 5)

            # DC input string 2 PV
            data[ATTR_INPUT_2_VOLTAGE] = rssf(rir1, 7)
            data[ATTR_INPUT_2_AMPERAGE] = rssf(rir1, 8)
            data[ATTR_INPUT_2_POWER] = rsdf(rir1, 9)
            data[ATTR_INPUT_2_ENERGY_TODAY] = rsdf(rir2, 7)
            data[ATTR_INPUT_2_ENERGY_TOTAL] = rsdf(rir2, 9)

            # AC output grid
            data[ATTR_OUTPUT_POWER] = rsdf(rir1, 11)
            data[ATTR_OUTPUT_ENERGY_TODAY] = rsdf(rir1, 26)
            data[ATTR_OUTPUT_ENERGY_TOTAL] = rsdf(rir1, 28)
            data[ATTR_OUTPUT_POWER_FACTOR] = rssf(rir2, 0)
            data[ATTR_OUTPUT_REACTIVE_POWER] = rsdf(rir2, 13)
            data[ATTR_OUTPUT_REACTIVE_ENERGY_TODAY] = rsdf(rir2, 15)
            data[ATTR_OUTPUT_REACTIVE_ENERGY_TOTAL] = rsdf(rir2, 17)
            data[ATTR_OUTPUT_REACTIVE_ENERGY_TOTAL] = rsdf(rir2, 17)

            # AC output phase 1 grid
            data[ATTR_OUTPUT_1_VOLTAGE] = rssf(rir1, 14)
            data[ATTR_OUTPUT_1_AMPERAGE] = rssf(rir1, 15)
            data[ATTR_OUTPUT_1_POWER] = rsdf(rir1, 16)

            # AC output phase 2 grid (if used)
            data[ATTR_OUTPUT_2_VOLTAGE] = rssf(rir1, 18)
            data[ATTR_OUTPUT_2_AMPERAGE] = rssf(rir1, 19)
            data[ATTR_OUTPUT_2_POWER] = rsdf(rir1, 20)

            # AC output phase 3 grid (if used)
            data[ATTR_OUTPUT_3_VOLTAGE] = rssf(rir1, 22)
            data[ATTR_OUTPUT_3_AMPERAGE] = rssf(rir1, 23)
            data[ATTR_OUTPUT_3_POWER] = rsdf(rir1, 24)

            # Miscellaneous information
            data[ATTR_OPERATION_HOURS] = rsdf(rir1, 30, 2)
            data[ATTR_FREQUENCY] = rssf(rir1, 13, 100)
            data[ATTR_TEMPERATURE] = rssf(rir1, 32)
            data[ATTR_IPM_TEMPERATURE] = rssf(rir1, 41)
            data[ATTR_P_BUS_VOLTAGE] = rssf(rir1, 42)
            data[ATTR_N_BUS_VOLTAGE] = rssf(rir1, 43)
            data[ATTR_DERATING_MODE] = rir2.registers[2]
            data[ATTR_DERATING] = DERATINGMODES[rir2.registers[2]]

            # Status, faults & warnings
            data[ATTR_STATUS_CODE] = rir1.registers[0]
            data[ATTR_STATUS] = STATUSCODES[rir1.registers[0]]
            data[ATTR_FAULT_CODE] = rir1.registers[40]
            data[ATTR_FAULT] = FAULTCODES[rir1.registers[40]]
            data[ATTR_WARNING_CODE] = rir2.registers[19]
            data[ATTR_WARNING] = WARNINGCODES[rir2.registers[19]]
            data[ATTR_WARNING_VALUE] = rir2.registers[20]

        except (ConnectionException, ModbusException) as e:
            self.data = {}
            raise ModbusError(e)
        except Exception as e:
            raise Exception(e)
        finally:
            self._client.close()

        _LOGGER.debug(f"Data: {data}")

        if not data:
            self.data = {}
            return

        self.data = data
        return

    @property
    def available(self):
        """Return True is data is available."""
        return bool(self.data)


class PortError(Exception):
    """Raised when the USB port in not available."""

    def __init__(self, status):
        """Initialize."""
        super(PortError, self).__init__(status)
        self.status = status


class ModbusError(Exception):
    """Raised when the Modbus communication has error."""

    def __init__(self, status):
        """Initialize."""
        super(ModbusError, self).__init__(status)
        self.status = status
