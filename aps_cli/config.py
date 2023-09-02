import typer
import ipaddress
from typing_extensions import Annotated
from aps_cli import utils, g_vars
app = typer.Typer()
from rich.table import Table

def ip_validation_callback(value: str):
    if value is not None:
        try:
            ipaddress.IPv4Address(value)
        except (ValueError, TypeError) as e:
            msg = '%s. Please enter an acceptable IP Address.' % str(e)
            raise typer.BadParameter(msg)
    return value

def dns_validation_callback(value: str):
    if value != None:
        try:
            ipaddress.IPv4Address(value)
        except (ValueError, TypeError) as e:
            msg = '%s. Please enter an acceptable IP Address.' % str(e)
            raise typer.BadParameter(msg)
    return value

def ip_mask_validation_callback(value: str):
    if value is not None:
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
    if value != None and len(value) > 16:
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
    try:
        response = res.json()
        utils.print_msg("response = {}".format(response), True, ctx.obj.debug)
        table = Table("Param", "Value")
        if response['status'] == "OK":
            for r in response:
                if r not in ['status', 'error']:
                    table.add_row(r, response[r])
            g_vars.console.print(table)
        else:
            message = typer.style("Error: {}".format(response['error']), fg=typer.colors.RED)
            utils.print_msg(message, False, ctx.obj.debug)
    except Exception as e:
        message = typer.style("Error: {}".format(e), fg=typer.colors.RED)
        utils.print_msg(message)

@app.command(name="net-change")
def net_change(ctx: typer.Context,
                ip: Annotated[str, typer.Option(callback=ip_mask_validation_callback, help='New IP format a.b.c.d/yy')] = None,
                gw: Annotated[str, typer.Option(callback=ip_validation_callback, help='New Gateway')] = None,
                dns1: Annotated[str, typer.Option(callback=dns_validation_callback, help='New Primary DNS')] = None,
                dns2: Annotated[str, typer.Option(callback=dns_validation_callback, help='New Secondary DNS')] = None,
                hostname: Annotated[str, typer.Option(callback=hostname_validation_callback, help='New Hostname')] = None,
                dhcp: Annotated[bool, typer.Option(help='DHCP enabled')] = False):
    """
    Change the current network configuration
    """
    utils.print_msg(f'Login with the user \'{ctx.obj.username}\' to url {ctx.obj.url}', True, ctx.obj.debug)
    utils.print_msg(f'Changing network configuration', True, ctx.obj.debug)
        
    d = {}
    if dhcp is not None:
        d['dhcp'] = ('1' if dhcp else '0')
    
    if ip is not None:
        ip_obj = ipaddress.IPv4Interface(ip)
        d['ip'] = str(ip_obj.ip)
        d['sub'] = str(ip_obj.netmask)
        # Passing ip/mask means disabling the dhcp
        d['dhcp'] = '0'

    if gw is not None:
        d['gw'] = gw

    if dns1 is not None:
        d['dns1'] = dns1

    if dns2 is not None:
        d['dns2'] = dns2

    if hostname is not None:
        d['host'] = hostname

    print("Passing d = {}".format(d))
    res = utils.do_post("{}/{}".format(ctx.obj.url, g_vars.API_DICT['net-change']['url']), username=ctx.obj.username, password=ctx.obj.password, data=d)
    print(res.json())

@app.command(name="pw-change")
def pw_change(ctx: typer.Context,
            user: Annotated[str, typer.Option(help='Username')],
            password: Annotated[str, typer.Option(prompt=True, confirmation_prompt=True, hide_input=True)]):
    """
    Change the password for a user
    """
    if user is None:
        user = ctx.obj.username
    utils.print_msg(f'Login with the user \'{ctx.obj.username}\' to url {ctx.obj.url}', True, ctx.obj.debug)
    utils.print_msg(f'Changing the password for the user \'{user}\'', True, ctx.obj.debug)
    res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['pw-change']['url']), username=ctx.obj.username, password=ctx.obj.password, params={'user': user, 'pw': password})
    try:
        response = res.json()
        utils.print_msg("response = {}".format(response), True, ctx.obj.debug)
        if response['status'] == "OK":
            message = typer.style("Status: OK", fg=typer.colors.GREEN, bold=True)
        else:
            message = typer.style("Error: {}".format(response['error']), fg=typer.colors.RED)
        utils.print_msg(message, False, ctx.obj.debug)
    except Exception as e:
        message = typer.style("Error: {}".format(e), fg=typer.colors.RED)
        utils.print_msg(message)