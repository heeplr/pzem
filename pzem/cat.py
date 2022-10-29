"""read read from PZEM-0xx Energy Meter Modules and output as json"""

import click
import json
import time

from pzem import PZEM_017



# ----------------------------------------------------------------------
@click.command(
    context_settings={
        "help_option_names": ["-h", "--help"],
        "auto_envvar_prefix": "VOTRONIC",
    }
)
@click.option(
    "--port",
    "-p",
    default="/dev/ttyUSB0",
    show_default=True,
    show_envvar=True,
    help="serial port",
)
@click.option(
    "--baudrate",
    "-b",
    default=9600,
    show_default=True,
    show_envvar=True,
    help="serial baudrate",
)
@click.option(
    "--address",
    "-a",
    default=1,
    show_default=True,
    show_envvar=True,
    help="modbus address"
)
@click.option(
    "--exclude",
    "-e",
    type=click.Choice(
        [ "voltage", "current", "power", "energy", "voltage_alarm", "current_range" ],
        case_sensitive=False
    ),
    default=[],
    multiple=True,
    show_default=True,
    show_envvar=True,
    help="exclude those fields in output (repeat for multiple fields)",
)
@click.option(
    "--interval",
    "-i",
    default=1.0,
    show_default=True,
    show_envvar=True,
    help="output values every n seconds"
)
@click.option(
    "--reset-energy",
    "-r",
    default=False,
    flag_value=True,
    show_envvar=True,
    help="reset energy counter to zero"
)
@click.option(
    "--current-range",
    "-c",
    type=click.Choice(["100A", "50A", "200A", "300A"], case_sensitive=False),
    show_envvar=True,
    help="set energy range to permanent storage"
)
def read_pzem(port, baudrate, address, exclude, interval, reset_energy, current_range):
    """read from PZEM-0xx Energy Meter Modules and output as json"""

    # initialize sensor
    pzem = PZEM_017(serial_port=port, baudrate=baudrate, slave_addr=address)

    # reset energy counter?
    if reset_energy:
        pzem.energy_reset()

    # set current range?
    if current_range:
        pzem.current_range = current_range

    while True:
        # create json dict
        datagram = {
            "voltage": pzem.voltage,
            "current": pzem.current,
            "power": pzem.power,
            "energy": pzem.energy,
            "voltage_alarm": pzem.voltage_alarm,
            "current_range": pzem.current_range
        }
        # filter excluded fields
        result = { k:v for k,v in datagram.items() if k not in exclude }
        # output values
        click.echo(json.dumps(result))
        # delay
        time.sleep(interval)

# ---------------------------------------------------------------------
if __name__ == "__main__":
    read_pzem()
