"""
Python wrapper for getting data asynchonously from Growatt inverters via serial usb RS232 connection and modbus RTU protocol.
"""

import logging
import os

from pymodbus.client.sync import ModbusSerialClient as ModbusClient

from .const import *

_LOGGER = logging.getLogger(__name__)


def read_scale_single_to_float(rr, index, scale=10):
    return float(rr.registers[index]) / scale


def read_scale_double_to_float(rr, index, scale=10):
    return float((rr.registers[index] << 16) + rr.registers[index + 1]) / scale


class GrowattRS232:
    """Main class to communicate with the Growatt inverter."""

    def __init__(self, port=PORT, address=ADDRESS):
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
            f"GrowattRS232 using usb port {self._port} and modbus address {self._unit}"
        )

    async def async_update(self):
        """Read Growatt data."""

        data = {}

        # Modbus rtu information from "Growatt PV Inverter Modbus RS485 RTU Protocol V3.14 2016-09-27" specification.
        # The availability of the attributes depends on the firmware version of your inverter.

        if os.path.exists(self._port) and self._client.connect():
            if self.serial_number == "":
                rhr = self._client.read_holding_registers(0, 30, unit=self._unit)
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
                        f"GrowattRS232 with serial number {self.serial_number} is model {self.model_number} and has firmware {self.firmware}"
                    )
                else:
                    self.firmware = ""
                    self.serial_number = ""
                    self.model_number = ""
                    self._client.close()
                    return None

            rir1 = self._client.read_input_registers(0, 44, unit=self._unit)
            if rir1.isError():
                self._client.close()
                return None

            rir2 = self._client.read_input_registers(45, 21, unit=self._unit)
            if rir2.isError():
                self._client.close()
                return None

            self._client.close()

            # Inverter properties
            data[ATTR_SERIAL_NUMBER] = self.serial_number
            data[ATTR_MODEL_NUMBER] = self.model_number
            data[ATTR_FIRMWARE] = self.firmware

            # DC input PV
            data[ATTR_INPUT_POWER] = read_scale_double_to_float(rir1, 1)
            data[ATTR_INPUT_ENERGY_TODAY] = read_scale_double_to_float(rir2, 11)

            # DC input string 1 PV
            data[ATTR_INPUT_1_VOLTAGE] = read_scale_single_to_float(rir1, 3)
            data[ATTR_INPUT_1_AMPERAGE] = read_scale_single_to_float(rir1, 4)
            data[ATTR_INPUT_1_POWER] = read_scale_double_to_float(rir1, 5)
            data[ATTR_INPUT_1_ENERGY_TODAY] = read_scale_double_to_float(rir2, 3)
            data[ATTR_INPUT_1_ENERGY_TOTAL] = read_scale_double_to_float(rir2, 5)

            # DC input string 2 PV
            data[ATTR_INPUT_2_VOLTAGE] = read_scale_single_to_float(rir1, 7)
            data[ATTR_INPUT_2_AMPERAGE] = read_scale_single_to_float(rir1, 8)
            data[ATTR_INPUT_2_POWER] = read_scale_double_to_float(rir1, 9)
            data[ATTR_INPUT_2_ENERGY_TODAY] = read_scale_double_to_float(rir2, 7)
            data[ATTR_INPUT_2_ENERGY_TOTAL] = read_scale_double_to_float(rir2, 9)

            # AC output grid
            data[ATTR_OUTPUT_POWER] = read_scale_double_to_float(rir1, 11)
            data[ATTR_OUTPUT_ENERGY_TODAY] = read_scale_double_to_float(rir1, 26)
            data[ATTR_OUTPUT_ENERGY_TOTAL] = read_scale_double_to_float(rir1, 28)
            data[ATTR_OUTPUT_POWER_FACTOR] = read_scale_single_to_float(rir2, 0)
            data[ATTR_OUTPUT_REACTIVE_POWER] = read_scale_double_to_float(rir2, 13)
            data[ATTR_OUTPUT_REACTIVE_ENERGY_TODAY] = read_scale_double_to_float(
                rir2, 15
            )
            data[ATTR_OUTPUT_REACTIVE_ENERGY_TOTAL] = read_scale_double_to_float(
                rir2, 17
            )
            data[ATTR_OUTPUT_REACTIVE_ENERGY_TOTAL] = read_scale_double_to_float(
                rir2, 17
            )

            # AC output phase 1 grid
            data[ATTR_OUTPUT_1_VOLTAGE] = read_scale_single_to_float(rir1, 14)
            data[ATTR_OUTPUT_1_AMPERAGE] = read_scale_single_to_float(rir1, 15)
            data[ATTR_OUTPUT_1_POWER] = read_scale_double_to_float(rir1, 16)

            # AC output phase 2 grid (if used)
            data[ATTR_OUTPUT_2_VOLTAGE] = read_scale_single_to_float(rir1, 18)
            data[ATTR_OUTPUT_2_AMPERAGE] = read_scale_single_to_float(rir1, 19)
            data[ATTR_OUTPUT_2_POWER] = read_scale_double_to_float(rir1, 20)

            # AC output phase 3 grid (if used)
            data[ATTR_OUTPUT_3_VOLTAGE] = read_scale_single_to_float(rir1, 22)
            data[ATTR_OUTPUT_3_AMPERAGE] = read_scale_single_to_float(rir1, 23)
            data[ATTR_OUTPUT_3_POWER] = read_scale_double_to_float(rir1, 24)

            # Miscelanuous information
            data[ATTR_OPERATION_HOURS] = read_scale_double_to_float(rir1, 30, 2)
            data[ATTR_FREQUENCY] = read_scale_single_to_float(rir1, 13, 100)
            data[ATTR_TEMPERATURE] = read_scale_single_to_float(rir1, 32)
            data[ATTR_IPM_TEMPERATURE] = read_scale_single_to_float(rir1, 41)
            data[ATTR_P_BUS_VOLTAGE] = read_scale_single_to_float(rir1, 42)
            data[ATTR_N_BUS_VOLTAGE] = read_scale_single_to_float(rir1, 43)
            data[ATTR_DERATING_MODE] = rir2.registers[2]
            data[ATTR_DERATING] = DeratingModes[rir2.registers[2]]

            # Status, faults & warnings
            data[ATTR_STATUS_CODE] = rir1.registers[0]
            data[ATTR_STATUS] = StatusCodes[rir1.registers[0]]
            data[ATTR_FAULT_CODE] = rir1.registers[40]
            data[ATTR_FAULT] = FaultCodes[rir1.registers[40]]
            data[ATTR_WARNING_CODE] = rir2.registers[19]
            data[ATTR_WARNING] = WarningCodes[rir2.registers[19]]
            data[ATTR_WARNING_VALUE] = rir2.registers[20]

            _LOGGER.debug(f"Data: {data}")

            if not data:
                self.data = {}
                return None

            self.data = data

    @property
    def available(self):
        """Return True is data is available."""
        return bool(self.data)
