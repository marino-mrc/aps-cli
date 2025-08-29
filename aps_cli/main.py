import typer
from typing_extensions import Annotated
from dataclasses import dataclass
from aps_cli import utils, g_vars, config, aps_port, aps_module
from rich.table import Table

app = typer.Typer(rich_help_panel=False)
#app = typer.Typer(rich_help_panel=False, no_args_is_help=False)
app.add_typer(aps_port.app, name="port")
app.add_typer(aps_module.app, name="module")
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

@app.command(name="status")
def status(ctx: typer.Context):

    error, res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['status']['url']), 
        username=ctx.obj.username, password=ctx.obj.password, debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    
    if not error:
        try:
            response = res.json()
            if response['status'] == "OK":
                table = Table("Param", "Value")
                data = response['details']                
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


if __name__ == "__main__":
    app()
