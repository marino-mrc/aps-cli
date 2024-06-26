import typer
from typing_extensions import Annotated
from dataclasses import dataclass
from aps_cli import utils, g_vars, config
from rich.table import Table

app = typer.Typer()
app.add_typer(config.app, name="config")

@dataclass
class Common:
    url: str
    username: str
    password: str
    debug: bool
    insecure: bool

@app.callback()
def common(ctx: typer.Context,
        url: Annotated[str, typer.Option(envvar='APS_URL', help='URL')],
        username: Annotated[str, typer.Option(envvar='APS_USERNAME', help='Username')],
        password: Annotated[str, typer.Option(envvar='APS_PASSWORD', help='Password')],
        debug: Annotated[bool, typer.Option(envvar='APS_DEBUG', help='Debug mode')] = False,
        insecure: Annotated[bool, typer.Option(envvar='APS_INSECURE', help='Disable SSL certificates verification')] = False):
    """Common Entry Point"""
    ctx.obj = Common(url, username, password, debug, insecure)

def port_status_validation_callback(value: str):
    value = value.lower()
    if value != "on" and value != "off":
        raise typer.BadParameter("Only 'on' or 'off' are allowed")
    return value

def port_number_validation_callback(value: int):
    if value is not None and (value > 16 or value < 1):
        raise typer.BadParameter("Only values between 1 and 16 are allowed")
    return value

def mandatory_port_validation_callback(value: int):
    if (value > 16 or value < 1):
        raise typer.BadParameter("Only values between 1 and 16 are allowed")
    return value    

@app.command(name="port-set")
def set_port(ctx: typer.Context, port_number: Annotated[int, typer.Argument(callback=port_number_validation_callback)], 
        port_status: Annotated[str, typer.Argument(callback=port_status_validation_callback)]):
    """
    Set the status of a given port to ON or OFF
    """
    error, res = utils.do_post("{}/{}".format(ctx.obj.url, g_vars.API_DICT['port-set']['url']),
        username=ctx.obj.username, password=ctx.obj.password, data={'port': port_number - 1, 'state': port_status},
        debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    if not error:
        try:
            response = res.json()
            if response['status'] == port_status:
                message = typer.style("Status: {}".format(port_status), fg=typer.colors.GREEN, bold=True)
            else:
                message = typer.style("Error: {}".format(response['error']), fg=typer.colors.RED)
            utils.print_msg(message, False, ctx.obj.debug)
        except Exception as e:
            message = typer.style("Error: {}".format(e), fg=typer.colors.RED)
            utils.print_msg(message)
    else:
        message = typer.style(res, fg=typer.colors.RED)
        utils.print_msg(message)

@app.command(name="port-status")
def port_status(ctx: typer.Context, 
    port_number: Annotated[int, typer.Argument(callback=port_number_validation_callback)] = None):
    """
    Check the status of all ports or of a single port
    """
    if port_number == None:
        error, res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['port-status']['url']),
            username=ctx.obj.username, password=ctx.obj.password, debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    else:
        error, res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['port-status']['url']), 
            username=ctx.obj.username, password=ctx.obj.password, params={'port': port_number - 1},
            debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    if not error:
        try:
            response = res.json()
            if response['status'] == "OK":
                ports = response['ports']
                table = Table("Port", "Status")
                for r in ports:
                    table.add_row(str(int(r) + 1), ports[r])
                g_vars.console.print(table)
            else:
                message = typer.style("Error: {}".format(response['error']), fg=typer.colors.RED)
                utils.print_msg(message, False, ctx.obj.debug)
        except Exception as e:
            message = typer.style("Error: {}".format(e), fg=typer.colors.RED)
            utils.print_msg(message)
    else:
        message = typer.style(res, fg=typer.colors.RED)
        utils.print_msg(message)


@app.command(name="port-show")
def port_status(ctx: typer.Context, 
    port_number: Annotated[int, typer.Argument(callback=mandatory_port_validation_callback)]):
    """
    Show details for a single port (power consumption)
    """
    #port_number = port_number - 1
    error, res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['port-show']['url']), 
        username=ctx.obj.username, password=ctx.obj.password, params={'port': port_number - 1},
        debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    if not error:
        try:
            response = res.json()
            if response['status'] == "OK":
                details = response['details']
                table = Table("Param", "Value")
                data = {}
                data['port'] = port_number
                data['enabled'] = utils.is_bit_set(int(details['info']), 0)
                data['voltage'] = details['voltage']
                data['current'] = details["current"]
                data['openCircuit'] = utils.is_bit_set(int(details['info']), 1)
                data['shortCircuit'] = utils.is_bit_set(int(details['info']), 2)
                data['sensorError'] = utils.is_bit_set(int(details['info']), 3)
                data['adcError'] = utils.is_bit_set(int(details['info']), 4)
                
                for key in data:
                    table.add_row(key, str(data[key]))
                g_vars.console.print(table)
            else:
                message = typer.style("Error: {}".format(response['error']), fg=typer.colors.RED)
                utils.print_msg(message, False, ctx.obj.debug)
        except Exception as e:
            message = typer.style("Error: {}".format(e), fg=typer.colors.RED)
            utils.print_msg(message)
    else:
        message = typer.style(res, fg=typer.colors.RED)
        utils.print_msg(message)
