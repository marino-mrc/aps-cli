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
    error, res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['net-show']['url']),
        username=ctx.obj.username, password=ctx.obj.password, debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    if not error:
        try:
            response = res.json()
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
    else:
        message = typer.style(res, fg=typer.colors.RED)
        utils.print_msg(message)

@app.command(name="adc-show")
def net_print(ctx: typer.Context):
    """
    Print the current network configuration
    """    
    error, res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['adc-show']['url']),
        username=ctx.obj.username, password=ctx.obj.password, debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    if not error:
        try:
            response = res.json()
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
    else:
        message = typer.style(res, fg=typer.colors.RED)
        utils.print_msg(message)

@app.command(name="power-show")
def net_print(ctx: typer.Context):
    """
    Print the current network configuration
    """    
    error, res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['power-show']['url']),
        username=ctx.obj.username, password=ctx.obj.password, debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    if not error:
        try:
            response = res.json()
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
    else:
        message = typer.style(res, fg=typer.colors.RED)
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

    error, res = utils.do_post("{}/{}".format(ctx.obj.url, g_vars.API_DICT['net-change']['url']), username=ctx.obj.username,
        password=ctx.obj.password, data=d, debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    if not error:
        print("Good: message = {}".format(res))
    else:
        print("Error! msg = {}".format(res))

@app.command(name="pw-change")
def pw_change(ctx: typer.Context,
            user: Annotated[str, typer.Option(help='Username')],
            password: Annotated[str, typer.Option(prompt=True, confirmation_prompt=True, hide_input=True)]):
    """
    Change the password for a user
    """
    if user is None:
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
        utils.print_msg(message)

@app.command(name="https-change")
def pw_change(ctx: typer.Context,
            enabled: Annotated[bool, typer.Option(help='HTTPS enabled')] = False):
    """
    Enable or disable HTTPS
    """
    d = {}
    if enabled == True:
        d['status'] = "true"
    else:
        print("setting FALSE")
        d['status'] = "false"
    error, res = utils.do_post("{}/{}".format(ctx.obj.url, g_vars.API_DICT['https-change']['url']), 
        username=ctx.obj.username, password=ctx.obj.password, data=d, debug=ctx.obj.debug, 
        verify=(not ctx.obj.insecure))
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
        utils.print_msg(message)


