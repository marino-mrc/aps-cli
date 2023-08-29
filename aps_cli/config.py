import typer
import ipaddress
from typing_extensions import Annotated
from aps_cli import utils, g_vars
app = typer.Typer()
from rich.table import Table

def ip_validation_callback(value: str):
    try:
        ipaddress.IPv4Address(value)
    except (ValueError, TypeError) as e:
        msg = '%s. Please enter an acceptable IP Address.' % str(e)
        raise typer.BadParameter(msg)
    return value

def dns_validation_callback(value: str):
    if value != "":
        try:
            ipaddress.IPv4Address(value)
        except (ValueError, TypeError) as e:
            msg = '%s. Please enter an acceptable IP Address.' % str(e)
            raise typer.BadParameter(msg)
    return value

def ip_mask_validation_callback(value: str):
    try:
        if "/" not in value:
            raise typer.BadParameter("Please use the following format a.b.c.d/yy")
        ip_str = value.split("/")[0]
        mask = value.split("/")[1]
        ip = ipaddress.ip_address(ip_str)
            # Append to self.hostiplist.
        
        if int(mask) < 0 or int(mask) > 32:
            raise typer.BadParameter("Please use a valid mask!")
    except (ValueError, TypeError) as e:
        msg = '%s. Please enter an acceptable IP Address.' % str(e)
        raise typer.BadParameter(msg)
    return value

def hostname_validation_callback(value: str):
    if len(value) > 16:
        raise typer.BadParameter("Maximum allowed len is 16 characters")
    return value

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
    print(response)
    if response['status'] == "OK":
        for r in response:
            if r not in ['status', 'error']:
                table.add_row(r, response[r])
        g_vars.console.print(table)
    else:
        print(response)

@app.command(name="net-change")
def net_change(ctx: typer.Context,
                ip: Annotated[str, typer.Option(callback=ip_mask_validation_callback, help='New IP format a.b.c.d/yy')],
                gw: Annotated[str, typer.Option(callback=ip_validation_callback, help='New Gateway')],
                dns1: Annotated[str, typer.Option(callback=dns_validation_callback, help='New Primary DNS')] = "",
                dns2: Annotated[str, typer.Option(callback=dns_validation_callback, help='New Secondary DNS')] = "",
                hostname: Annotated[str, typer.Option(callback=hostname_validation_callback, help='New Hostname')] = "",
                dhcp: Annotated[bool, typer.Option(help='DHCP enabled')] = False):
    """
    Change the current network configuration
    """
    utils.print_msg(f'Login with the user \'{ctx.obj.username}\' to url {ctx.obj.url}', True, ctx.obj.debug)
    utils.print_msg(f'Changing network configuration', True, ctx.obj.debug)
    ip_obj = ipaddress.IPv4Interface(ip)
    d = {'ip': str(ip_obj.ip), 'sub': str(ip_obj.netmask), 'gw': gw, 'dns1': dns1, 'dns2': dns2, 'host': hostname, 'dhcp': ('1' if dhcp else '0')}
    #print("Passing d = {}".format(d))
    res = utils.do_post("{}/{}".format(ctx.obj.url, g_vars.API_DICT['net-change']['url']), username=ctx.obj.username, password=ctx.obj.password, data=d)
    print(res.json())

@app.command(name="pw-change")
def pw_change(ctx: typer.Context,
                user: Annotated[str, typer.Option(help='Username')]):
    """
    Change the password for a user
    """
    print(f"Changing the password")