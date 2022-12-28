"""pzem interface"""

import minimalmodbus


class PZEM_017(minimalmodbus.Instrument):
    VOLT_MULTIPLICATOR = 0.1
    CURRENT_MULTIPLICATOR = 0.1
    POWER_MULTIPLICATOR = 10
    ENERGY_MULTIPLICATOR = 10
    CURRENT_RANGES = {
        "100A": 0,
         "50A": 1,
        "200A": 2,
        "300A": 3,
        0: "100A",
        1: "50A",
        2: "200A",
        3: "300A"
    }

    def __init__(self, serial_port, baudrate, slave_addr=1):
        minimalmodbus.Instrument.__init__(self, serial_port, slave_addr)

        self.serial.baudrate = baudrate
        self.serial.bytesize = minimalmodbus.serial.EIGHTBITS
        self.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.serial.stopbits = minimalmodbus.serial.STOPBITS_TWO
        self.serial.timeout = 0.1
        self.mode = minimalmodbus.MODE_RTU
        self.close_port_after_each_call = False
        #self.debug = True

    def __repr__(self):
        return f"{self.voltage}V, {self.current}A, {self.power}W, {self.energy}Wh"

    @property
    def voltage(self):
        """V"""
        return self.read_register(
            registeraddress = 0x00,
            number_of_decimals = 1,
            functioncode = 4,
            signed=False
        ) * self.VOLT_MULTIPLICATOR

    @property
    def current(self):
        """A"""
        return self.read_register(
            registeraddress = 0x01,
            number_of_decimals = 1,
            functioncode = 4,
            signed=False
        ) * self.CURRENT_MULTIPLICATOR

    @property
    def power(self):
        """W"""
        return self.read_register(
            registeraddress = 0x02,
            number_of_decimals = 2,
            functioncode = 4,
            signed=False
        ) * self.POWER_MULTIPLICATOR

    @property
    def energy(self):
        """Wh"""
        return (self.read_register(
            registeraddress = 0x04,
            number_of_decimals = 2,
            functioncode = 4,
            signed=False
        ) * self.ENERGY_MULTIPLICATOR)

    @property
    def voltage_alarm(self):
        high = bool(self.read_register(
            registeraddress = 0x06,
            number_of_decimals = 1,
            functioncode = 4
        ))
        low = bool(self.read_register(
            registeraddress = 0x07,
            number_of_decimals = 1,
            functioncode = 4
        ))
        return { "low": low, "high": high }

    @property
    def current_range(self):
        """get currently configured current range according to CURRENT_RANGES"""
        r = self.read_register(
            registeraddress = 0x03,
            number_of_decimals = 0,
            functioncode = 3
        )

        try:
            return self.CURRENT_RANGES[r]
        except KeyError:
            raise ValueError(f"PZEM-17 returned invalid current range code: {r}")

    @current_range.setter
    def current_range(self, value):
        """set currently configured current range according to CURRENT_RANGES"""

        try:
            v = self.CURRENT_RANGES[value]
        except KeyError:
            raise ValueError(f"valid values are: {self.CURRENT_RANGES.keys()}")

        self.write_register(
            registeraddress = 0x03,
            number_of_decimals = 0,
            functioncode = 6,
            value = int(v)
        )

    def energy_reset(self):
        """reset energy counter"""
        try:
            self._perform_command(functioncode=0x42, payload_to_slave="")
        except minimalmodbus.NoResponseError:
            pass
