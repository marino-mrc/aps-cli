import typer
from aps_cli import utils, g_vars
app = typer.Typer()
from rich.table import Table
#from rich.console import Console
#from aps_cli import API_DICT

@app.command(name="net-show")
def net_print(ctx: typer.Context):
    """
    Print the current network configuration
    """
    utils.print_msg(f'Login with the user \'{ctx.obj.username}\' to url {ctx.obj.url}', True, ctx.obj.debug)
    utils.print_msg(f'Retrieving Info from all ports', True, ctx.obj.debug)
    res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['net-show']['url']), username=ctx.obj.username, password=ctx.obj.password)
    table = Table("Param", "Value")
    response = res.json()
    if response['status'] == "OK":
        for r in response:
            if r not in ['status', 'error']:
                table.add_row(r, response[r])
        g_vars.console.print(table)
    else:
        print(response)

@app.command(name="net-change")
def net_change():
    print(f"Changing network config")

@app.command(name="pw-change")
def pw_change():
    print(f"Changing the password")