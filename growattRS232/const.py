"""Constants for growattRS232 library."""

# Defaults
DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_ADDRESS = 0x1

# ATTRIBUTES
ATTR_SERIAL_NUMBER = "serial_number"
ATTR_MODEL_NUMBER = "model_number"
ATTR_FIRMWARE = "firmware"

ATTR_STATUS = "status"
ATTR_STATUS_CODE = "status_code"

ATTR_INPUT_POWER = "input_power"  # W
ATTR_INPUT_ENERGY_TOTAL = "input_energy_total"  # kWh

ATTR_INPUT_1_VOLTAGE = "input_1_voltage"  # V
ATTR_INPUT_1_AMPERAGE = "input_1_amperage"  # A
ATTR_INPUT_1_POWER = "input_1_power"  # W
ATTR_INPUT_1_ENERGY_TODAY = "input_1_energy_today"  # kWh
ATTR_INPUT_1_ENERGY_TOTAL = "input_1_energy_total"  # kWh

ATTR_INPUT_2_VOLTAGE = "input_2_voltage"  # V
ATTR_INPUT_2_AMPERAGE = "input_2_amperage"  # A
ATTR_INPUT_2_POWER = "input_2_power"  # W
ATTR_INPUT_2_ENERGY_TODAY = "input_2_energy_today"  # kWh
ATTR_INPUT_2_ENERGY_TOTAL = "input_2_energy_total"  # kWh

ATTR_OUTPUT_POWER = "output_power"  # W
ATTR_OUTPUT_ENERGY_TODAY = "output_energy_today"  # kWh
ATTR_OUTPUT_ENERGY_TOTAL = "output_energy_total"  # kWh

ATTR_OUTPUT_REACTIVE_POWER = "output_reactive_power"  # Var
ATTR_OUTPUT_REACTIVE_ENERGY_TODAY = "output_reactive_energy_today"  # kVarh
ATTR_OUTPUT_REACTIVE_ENERGY_TOTAL = "output_reactive_energy_total"  # kVarh

ATTR_OUTPUT_1_VOLTAGE = "output_1_voltage"  # V
ATTR_OUTPUT_1_AMPERAGE = "output_1_amperage"  # A
ATTR_OUTPUT_1_POWER = "output_1_power"  # W

ATTR_OUTPUT_2_VOLTAGE = "output_2_voltage"  # V
ATTR_OUTPUT_2_AMPERAGE = "output_2_amperage"  # A
ATTR_OUTPUT_2_POWER = "output_2_power"  # W

ATTR_OUTPUT_3_VOLTAGE = "output_3_voltage"  # V
ATTR_OUTPUT_3_AMPERAGE = "output_3_amperage"  # A
ATTR_OUTPUT_3_POWER = "output_3_power"  # W

ATTR_OPERATION_HOURS = "operation_hours"  # s

ATTR_FREQUENCY = "frequency"  # Hz

ATTR_TEMPERATURE = "temperature"  # C
ATTR_IPM_TEMPERATURE = "ipm_temperature"  # C

ATTR_P_BUS_VOLTAGE = "p_bus_voltage"  # V
ATTR_N_BUS_VOLTAGE = "n_bus_voltage"  # V

ATTR_DERATING_MODE = "derating_mode"
ATTR_DERATING = "derating"

ATTR_FAULT_CODE = "fault_code"
ATTR_FAULT = "fault"

ATTR_WARNING_CODE = "warning_code"
ATTR_WARNING_VALUE = "warning_value"
ATTR_WARNING = "warning"

# Codes
STATUSCODES = {0: "Waiting", 1: "Normal", 3: "Fault"}

FAULTCODES = {
    0: "None",
    24: "Auto Test Failed",
    25: "No AC Connection",
    26: "PV Isolation Low",
    27: "Residual I High",
    28: "Output High DCI",
    29: "PV Voltage High",
    30: "AC V Outrange",
    31: "AC F Outrange",
    32: "Module Hot",
}
for i in range(1, 24):
    FAULTCODES[i] = "Generic Error Code: %s" % str(99 + i)

WARNINGCODES = {
    0x0000: "None",
    0x0001: "Fan warning",
    0x0002: "String communication abnormal",
    0x0004: "StrPID config Warning",
    0x0008: "Fail to read EEPROM",
    0x0010: "DSP and COM firmware unmatch",
    0x0020: "Fail to write EEPROM",
    0x0040: "SPD abnormal",
    0x0080: "GND and N connect abnormal",
    0x0100: "PV1 or PV2 circuit short",
    0x0200: "PV1 or PV2 boost driver broken",
    0x0400: "",
    0x0800: "",
    0x1000: "",
    0x2000: "",
    0x4000: "",
    0x8000: "",
}

DERATINGMODES = {
    0: "No Deratring",
    1: "PV",
    2: "",
    3: "Vac",
    4: "Fac",
    5: "Tboost",
    6: "Tinv",
    7: "Control",
    8: "*LoadSpeed",
    9: "*OverBackByTime",
}


# Unit of measurement
ELECTRICAL_POTENTIAL_VOLT = "V"
ELECTRICAL_CURRENT_AMPERE = "A"
POWER_WATT = "W"
REACTIVE_POWER_VAR = "var"
TIME_HOURS = "h"
ENERGY_KILO_WATT_HOUR = "kWh"
REACTIVE_ENERGY_KILO_VAR_HOUR = "kvarh"
FREQUENCY_HERTZ = "Hz"
TEMP_CELSIUS = "°C"

# Provided attributes and their associated unit of measurement
ATTRIBUTES = {
    ATTR_SERIAL_NUMBER: None,
    ATTR_MODEL_NUMBER: None,
    ATTR_FIRMWARE: None,
    ATTR_STATUS: None,
    ATTR_STATUS_CODE: None,
    ATTR_INPUT_POWER: POWER_WATT,
    ATTR_INPUT_ENERGY_TOTAL: ENERGY_KILO_WATT_HOUR,
    ATTR_INPUT_1_VOLTAGE: ELECTRICAL_POTENTIAL_VOLT,
    ATTR_INPUT_1_AMPERAGE: ELECTRICAL_CURRENT_AMPERE,
    ATTR_INPUT_1_POWER: POWER_WATT,
    ATTR_INPUT_1_ENERGY_TODAY: ENERGY_KILO_WATT_HOUR,
    ATTR_INPUT_1_ENERGY_TOTAL: ENERGY_KILO_WATT_HOUR,
    ATTR_INPUT_2_VOLTAGE: ELECTRICAL_POTENTIAL_VOLT,
    ATTR_INPUT_2_AMPERAGE: ELECTRICAL_CURRENT_AMPERE,
    ATTR_INPUT_2_POWER: POWER_WATT,
    ATTR_INPUT_2_ENERGY_TODAY: ENERGY_KILO_WATT_HOUR,
    ATTR_INPUT_2_ENERGY_TOTAL: ENERGY_KILO_WATT_HOUR,
    ATTR_OUTPUT_POWER: POWER_WATT,
    ATTR_OUTPUT_ENERGY_TODAY: ENERGY_KILO_WATT_HOUR,
    ATTR_OUTPUT_ENERGY_TOTAL: ENERGY_KILO_WATT_HOUR,
    ATTR_OUTPUT_REACTIVE_POWER: REACTIVE_POWER_VAR,
    ATTR_OUTPUT_REACTIVE_ENERGY_TODAY: REACTIVE_ENERGY_KILO_VAR_HOUR,
    ATTR_OUTPUT_REACTIVE_ENERGY_TOTAL: REACTIVE_ENERGY_KILO_VAR_HOUR,
    ATTR_OUTPUT_1_VOLTAGE: ELECTRICAL_POTENTIAL_VOLT,
    ATTR_OUTPUT_1_AMPERAGE: ELECTRICAL_CURRENT_AMPERE,
    ATTR_OUTPUT_1_POWER: POWER_WATT,
    ATTR_OUTPUT_2_VOLTAGE: ELECTRICAL_POTENTIAL_VOLT,
    ATTR_OUTPUT_2_AMPERAGE: ELECTRICAL_CURRENT_AMPERE,
    ATTR_OUTPUT_2_POWER: POWER_WATT,
    ATTR_OUTPUT_3_VOLTAGE: ELECTRICAL_POTENTIAL_VOLT,
    ATTR_OUTPUT_3_AMPERAGE: ELECTRICAL_CURRENT_AMPERE,
    ATTR_OUTPUT_3_POWER: POWER_WATT,
    ATTR_OPERATION_HOURS: TIME_HOURS,
    ATTR_FREQUENCY: FREQUENCY_HERTZ,
    ATTR_TEMPERATURE: TEMP_CELSIUS,
    ATTR_IPM_TEMPERATURE: TEMP_CELSIUS,
    ATTR_P_BUS_VOLTAGE: ELECTRICAL_POTENTIAL_VOLT,
    ATTR_N_BUS_VOLTAGE: ELECTRICAL_POTENTIAL_VOLT,
    ATTR_DERATING_MODE: None,
    ATTR_DERATING: None,
    ATTR_FAULT_CODE: None,
    ATTR_FAULT: None,
    ATTR_WARNING_CODE: None,
    ATTR_WARNING_VALUE: None,
    ATTR_WARNING: None,
}
