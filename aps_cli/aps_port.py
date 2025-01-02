import typer
import ipaddress
from typing_extensions import Annotated
from aps_cli import utils, g_vars
app = typer.Typer()
from rich.table import Table
from enum import Enum

class PortStatus(str, Enum):
    on = "on"
    off = "off"

@app.command(name="status")
def port_status(ctx: typer.Context, 
    module_number: Annotated[int, typer.Option(min=1, max=g_vars.MAX_MODULES)] = 1,
    port_number: Annotated[int, typer.Argument(min=1, max=g_vars.MAX_OUTPUT_PORTS)] = None):
    """
    Check the status of all ports or of a single port
    """
    if port_number == None:
        error, res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['port-status']['url']),
            username=ctx.obj.username, password=ctx.obj.password, debug=ctx.obj.debug, verify=(not ctx.obj.insecure), params={'module': module_number - 1})
    else:
        error, res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['port-status']['url']), 
            username=ctx.obj.username, password=ctx.obj.password, params={'module': module_number - 1, 'port': port_number - 1},
            debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    if not error:
        try:
            response = res.json()
            if response['status'] == "OK":
                module_section = "module%d" % (module_number - 1)
                ports = response[module_section]
                table = Table("Module" + str(module_number) + " Ports", "Status")
                for r in ports:
                    table.add_row("Port" + str(int(r[-1]) + 1), ports[r])
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


@app.command(name="show")
def port_show(ctx: typer.Context,
	port_number: Annotated[int, typer.Argument(min=1, max=g_vars.MAX_OUTPUT_PORTS)],
    module_number: Annotated[int, typer.Option(min=1, max=g_vars.MAX_MODULES)] = 1):
    """
    Show details for a single port (power consumption)
    """
    error, res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['port-show']['url']), 
        username=ctx.obj.username, password=ctx.obj.password, params={'module': module_number - 1, 'port': port_number - 1},
        debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    if not error:
        try:
            response = res.json()
            if response['status'] == "OK":
                details = response['details']
                table = Table("Param", "Value")
                data = {}
                data['module'] = module_number
                data['port'] = port_number
                data['enabled'] = utils.is_bit_set(int(details['status_bitmap']), 0)
                data['voltage'] = details['voltage']
                data['current'] = details["current"]
                data['openCircuit'] = utils.is_bit_set(int(details['status_bitmap']), 1)
                data['shortCircuit'] = utils.is_bit_set(int(details['status_bitmap']), 2)
                data['sensorError'] = utils.is_bit_set(int(details['status_bitmap']), 3)
                data['adcError'] = utils.is_bit_set(int(details['status_bitmap']), 4)
                
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


@app.command(name="set")
def port_set(ctx: typer.Context, 
	port_number: Annotated[int, typer.Argument(min=1, max=g_vars.MAX_OUTPUT_PORTS)], 
    port_status: Annotated[PortStatus, typer.Argument()],
    module_number: Annotated[int, typer.Option(min=1, max=g_vars.MAX_MODULES)] = 1):
    """
    Set the status of a given port to ON or OFF
    """
    error, res = utils.do_post("{}/{}".format(ctx.obj.url, g_vars.API_DICT['port-set']['url']),
        username=ctx.obj.username, password=ctx.obj.password, data={'module': module_number - 1, 'port': port_number - 1, 'state': port_status},
        debug=ctx.obj.debug, verify=(not ctx.obj.insecure))

    if not error:
        try:
            response = res.json()
            if response['status'] == "OK":
                message = typer.style("{}".format(response['message']), fg=typer.colors.GREEN, bold=True)
            else:
                message = typer.style("Error: {}".format(response['error']), fg=typer.colors.RED)
            utils.print_msg(message, False, ctx.obj.debug)
        except Exception as e:
            message = typer.style("Error: {}".format(e), fg=typer.colors.RED)
            utils.print_msg(message)
    else:
        message = typer.style(res, fg=typer.colors.RED)
        utils.print_msg(message)