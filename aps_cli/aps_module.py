import typer
import ipaddress
import json
from typing_extensions import Annotated
from aps_cli import utils, g_vars
app = typer.Typer()
from rich.table import Table
from enum import Enum

class ApsModuleStatus(str, Enum):
    enabled = "on"
    disabled = "off"

@app.command(name="status")
def module_status(ctx: typer.Context,
    module_number: Annotated[int, typer.Argument(min=1, max=g_vars.MAX_MODULES, help="Module ID")] = 1):

    error, res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['module-status']['url']), 
        username=ctx.obj.username, password=ctx.obj.password, params={'module': module_number - 1},
        debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    
    if not error:
        try:
            response = res.json()
            if response['status'] == "OK":
                table = Table("Param", "Value")
                data = response['module_status']
                for key in data:
                    if key in g_vars.MODULE_DICT:
                        table.add_row(key, str(g_vars.MODULE_DICT[key][str(data[key])]))
                    else:
                        table.add_row(key, str(data[key]))
                g_vars.console.print(table)
            else:
                message = typer.style("AError: {}".format(response['error']), fg=typer.colors.RED)
                utils.print_msg(message, False, ctx.obj.debug)
        except Exception as e:
            message = typer.style("BError: {}".format(e), fg=typer.colors.RED)
            utils.print_msg(message)
    else:
        message = typer.style(res, fg=typer.colors.RED)
        utils.print_msg(message)

@app.command(name="config-show")
def module_show(ctx: typer.Context,
    module_number: Annotated[int, typer.Argument(min=1, max=g_vars.MAX_MODULES, help="Module ID")] = 1):

    error, res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['module-show']['url']), 
        username=ctx.obj.username, password=ctx.obj.password, params={'module': module_number - 1},
        debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    
    if not error:
        try:
            response = res.json()
            if response['status'] == "OK":
                table = Table("Param", "Value")
                data = response['module_details']
                for key in data:
                    if key in g_vars.MODULE_DICT:
                        table.add_row(key, str(g_vars.MODULE_DICT[key][str(data[key])]))
                    else:
                        table.add_row(key, str(data[key]))
                g_vars.console.print(table)
            else:
                message = typer.style("Error: {}".format(response['error']), fg=typer.colors.RED)
                utils.print_msg(message, False, ctx.obj.debug)
        except Exception as e:
            message = typer.style("BError: {}".format(e), fg=typer.colors.RED)
            utils.print_msg(message)
    else:
        message = typer.style(res, fg=typer.colors.RED)
        utils.print_msg(message)

@app.command(name="set")
def module_set(ctx: typer.Context,
    module_state: Annotated[ApsModuleStatus, typer.Option()],
    module_number: Annotated[int, typer.Argument(min=1, max=g_vars.MAX_MODULES, help="Module ID")] = 1):

    error, res = utils.do_post("{}/{}".format(ctx.obj.url, g_vars.API_DICT['module-set']['url']), 
        username=ctx.obj.username, password=ctx.obj.password, data={'module': module_number - 1, 'state': module_state},
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
            message = typer.style("BError: {}".format(e), fg=typer.colors.RED)
            utils.print_msg(message)
    else:
        message = typer.style(res, fg=typer.colors.RED)
        utils.print_msg(message)

@app.command(name="configure")
def module_configure(ctx: typer.Context,
    config_file: Annotated[typer.FileText, typer.Option()]):
    
    json_data = json.load(config_file)
    #d = json.loads(config_file)
    error, res = utils.do_post("{}/{}".format(ctx.obj.url, g_vars.API_DICT['module-configure']['url']), 
        username=ctx.obj.username, password=ctx.obj.password, json=json_data,
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
            message = typer.style("BError: {}".format(e), fg=typer.colors.RED)
            utils.print_msg(message)
    else:
        message = typer.style(res, fg=typer.colors.RED)
        utils.print_msg(message)