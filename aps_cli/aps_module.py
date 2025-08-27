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
    config_file: Annotated[typer.FileText, typer.Option()],
    module_number: Annotated[int, typer.Argument(min=1, max=g_vars.MAX_MODULES, help="Module ID")] = 1):
    
    # Load the json file
    json_data = json.load(config_file)
    # Add the module_id field
    json_data["module_id"] = module_number - 1
    
    # Validate json module configuration data
    is_valid, message = validate_module_config(json_data)
    if not is_valid:
        typer.secho(message, fg=typer.colors.RED)
        raise typer.Exit(code=1)

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


def validate_module_config(json_data: dict) -> tuple[bool, str]:
    MANDATORY_FIELDS = ["module_id"]
    CONFIG_MANDATORY_FIELDS = ["InputVoltage0", "InputVoltage1", "VoltageConversionRatio0", "VoltageConversionRatio1", "InputTolerance0", "InputTolerance1", "PerPortImaxBank0", "PerPortImaxBank1"]
    # Check top-level mandatory fields
    for field in MANDATORY_FIELDS:
        if field not in json_data:
            return False, f"Missing mandatory field: '{field}'"

    # Check nested fields inside "configuration"
    if "configuration" not in json_data:
        return False, "Missing mandatory field: 'configuration'"

    config_data = json_data["configuration"]
    if not isinstance(config_data, dict):
        return False, "'configuration' must be an object"

    for field in CONFIG_MANDATORY_FIELDS:
        if field not in config_data:
            return False, f"Missing mandatory configuration field: '{field}'"

    if json_data["configuration"]["PerPortImaxBank0"] not in [0, 1, 2]:
        return False, (
            f"PerPortImaxBank0: wrong value '{json_data['configuration']['PerPortImaxBank0']}'. "
            "Allowed values: {0 -> 3.5A, 1 -> 6A, 2 -> 10A}"
        )

    if json_data["configuration"]["PerPortImaxBank1"] not in [0, 1, 2]:
        return False, (
            f"PerPortImaxBank1: wrong value '{json_data['configuration']['PerPortImaxBank1']}'. "
            "Allowed values: {0 -> 3.5A, 1 -> 6A, 2 -> 10A}"
        )

    return True, "OK"