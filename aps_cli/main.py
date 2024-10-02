import typer
from typing_extensions import Annotated
from dataclasses import dataclass
from aps_cli import utils, g_vars, config, aps_port, aps_module
from rich.table import Table

app = typer.Typer()
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