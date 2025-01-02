import typer
import ipaddress
from typing_extensions import Annotated
from aps_cli import utils, g_vars
app = typer.Typer()
from rich.table import Table
from enum import Enum

@app.command(name="net-show")
def net_show(ctx: typer.Context):
    """
    Print the current network configuration
    """    
    error, res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['net-show']['url']),
        username=ctx.obj.username, password=ctx.obj.password, debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    if not error:
        try:
            response = res.json()
            table = Table("Param", "Value")
            if response['status'] == "OK":
                table = Table("Param", "Value")
                data = response['net_config']
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
            message = typer.style("Error: {}".format(e), fg=typer.colors.RED)
            utils.print_msg(message)
    else:
        message = typer.style(res, fg=typer.colors.RED)
        utils.print_msg(message)

@app.command(name="pw-change")
def pw_change(ctx: typer.Context,
            user: Annotated[str, typer.Option(help='Username')],
            password: Annotated[str, typer.Option(prompt=True, confirmation_prompt=True, hide_input=True)]):
    """
    Change the password for a user
    """
    utils.print_msg("Not yet implemented")
    """if user is None:
        user = ctx.obj.username
    d = {}
    d['user'] = user
    d['pw'] = password
    error, res = utils.do_post("{}/{}".format(ctx.obj.url, g_vars.API_DICT['pw-change']['url']), username=ctx.obj.username,
        password=ctx.obj.password, data=d, debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    if not error:
        try:
            response = res.json()
            if response['status'] == "OK":
                message = typer.style("Status: OK", fg=typer.colors.GREEN, bold=True)
            else:
                message = typer.style("Error: {}".format(response['error']), fg=typer.colors.RED)
            utils.print_msg(message, False, ctx.obj.debug)
        except Exception as e:
            message = typer.style("Error: {}".format(e), fg=typer.colors.RED)
            utils.print_msg(message)
    else:
        message = typer.style(res, fg=typer.colors.RED)
        utils.print_msg(message)"""