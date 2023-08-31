import typer
from typing_extensions import Annotated
from dataclasses import dataclass
#load_dotenv()
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

@app.callback()
def common(ctx: typer.Context,
        url: Annotated[str, typer.Option(envvar='APS_URL', help='URL')],
        username: Annotated[str, typer.Option(envvar='APS_USERNAME', help='Username')],
        password: Annotated[str, typer.Option(envvar='APS_PASSWORD', help='Password')],
        debug: Annotated[bool, typer.Option(envvar='APS_DEBUG', help='Debug mode')] = False):
    """Common Entry Point"""
    ctx.obj = Common(url, username, password, debug)

def port_status_validation_callback(value: str):
    value = value.upper()
    if value != "ON" and value != "OFF":
        raise typer.BadParameter("Only 'ON' or 'OFF' are allowed")
    return value

def port_number_validation_callback(value: int):
    if value is not None and (value > 15 or value < 0):
        raise typer.BadParameter("Only values between 0 and 15 are allowed")
    return value

def mandatory_port_validation_callback(value: int):
    if (value > 15 or value < 0):
        raise typer.BadParameter("Only values between 0 and 15 are allowed")
    return value    

@app.command(name="port-set")
def set_port(ctx: typer.Context, port_number: Annotated[int, typer.Argument(callback=port_number_validation_callback)], 
        port_status: Annotated[str, typer.Argument(callback=port_status_validation_callback)]):
    """
    Set the status of a given port to ON or OFF
    """
    utils.print_msg("Setting port {} to {}".format(port_number, port_status), True, ctx.obj.debug)
    res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['port-set']['url']),
        username=ctx.obj.username, password=ctx.obj.password, params={'port': port_number, 'status': port_status})
    #print(res.json())
    response = res.json()
    if response['status'] == "OK":
        message = typer.style("Status: {}".format(port_status), fg=typer.colors.GREEN, bold=True)
    else:
        message = typer.style("Error: {}".format(response['error']), fg=typer.colors.WHITE, bg=typer.colors.RED)
    utils.print_msg(message, False, ctx.obj.debug)


@app.command(name="port-status")
def port_status(ctx: typer.Context, port_number: Annotated[int, typer.Argument(callback=port_number_validation_callback)] = None):
    """
    Check the status of all ports or of a single port
    """
    utils.print_msg(f'Login with the user \'{ctx.obj.username}\' to url {ctx.obj.url}', True, ctx.obj.debug)
    if port_number == None:
        utils.print_msg(f'Retrieving Info from all ports', True, ctx.obj.debug)
        res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['port-status']['url']), username=ctx.obj.username, password=ctx.obj.password)
    else:
        utils.print_msg(f'Retrieving Port {port_number} info', True, ctx.obj.debug)
        res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['port-status']['url']), 
            username=ctx.obj.username, password=ctx.obj.password, params={'port': port_number})
    response = res.json()
    #print("response = {}".format(response))
    if response['status'] == "OK":
        ports = response['ports']
        table = Table("Port", "Status")
        for r in ports:
            table.add_row(r, ports[r])
        g_vars.console.print(table)
    else:
        message = typer.style("Error: {}".format(response['error']), fg=typer.colors.WHITE, bg=typer.colors.RED)
        utils.print_msg(message, False, ctx.obj.debug)


@app.command(name="port-show")
def port_status(ctx: typer.Context, port_number: Annotated[int, typer.Argument(callback=mandatory_port_validation_callback)]):
    """
    Show details for a single port (power consumption)
    """
    utils.print_msg(f'Login with the user \'{ctx.obj.username}\' to url {ctx.obj.url}', True, ctx.obj.debug)
    utils.print_msg(f'Retrieving Port {port_number} details', True, ctx.obj.debug)
    res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['port-show']['url']), 
        username=ctx.obj.username, password=ctx.obj.password, params={'port': port_number})
    response = res.json()
    if response['status'] == "OK":
        ports = response['details']
        table = Table("Param", "Value")
        for r in ports:
            table.add_row(r, ports[r])
        g_vars.console.print(table)
    else:
        message = typer.style("Error: {}".format(response['error']), fg=typer.colors.WHITE, bg=typer.colors.RED)
        utils.print_msg(message, False, ctx.obj.debug)