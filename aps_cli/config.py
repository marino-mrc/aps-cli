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
def adc_print(ctx: typer.Context,
            module_id: Annotated[int, typer.Argument(min=1, help="Module ID")]):
    """
    Check the status of all ports or of a single port
    """   
    error, res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['adc-show']['url']), 
        username=ctx.obj.username, password=ctx.obj.password, params={'module': module_id - 1},
        debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    """
    Print the current network configuration
    """    
    if not error:
        try:
            response = res.json()
            if response['status'] == "OK":
                data = response['currentSensorParams']
                table = Table("Param", "Value")
                
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

@app.command(name="input-show")
def input_print(ctx: typer.Context,
            module_id: Annotated[int, typer.Argument(min=1, help="Module ID")]):
    """
    Check the status of all ports or of a single port
    """   
    error, res = utils.do_get("{}/{}".format(ctx.obj.url, g_vars.API_DICT['input-show']['url']), 
        username=ctx.obj.username, password=ctx.obj.password, params={'module': module_id - 1},
        debug=ctx.obj.debug, verify=(not ctx.obj.insecure))
    """
    Print the current network configuration
    """    
    if not error:
        try:
            response = res.json()
            if response['status'] == "OK":
                data = response['powerSupplySettings']
                table = Table("Param", "Value")
                if data['moduleStatus'] == '0':
                    data['moduleStatus'] = 'Disconnected'
                elif data['moduleStatus'] == '1':
                    data['moduleStatus'] = 'Connected'
                else:
                    data['moduleStatus'] = 'Undefined'

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


@app.command(name="input-set")
def input_set(ctx: typer.Context,
                module_id: Annotated[int, typer.Argument(min=1, help="Module ID")],
                inputvoltage: Annotated[int, typer.Option(min=5,max=25, help='Input voltage for the connected power supply')],
                vcr: Annotated[float, typer.Option(min=1.0,max=20.0, help='Voltage conversion ratio')],
                tolerance: Annotated[float, typer.Option(min=1.0,max=20.0, help='Percentage value of the tolerance as an offset of the input voltage')]):
    """
    Change the configuration for a power supply
    """
    proceed = typer.confirm("Are you sure you want to proceed? Note that the APS board will be rebooted and all output ports will be powered off. At the end of the procedure, the output ports should have the same status they had before the reboot")
    if not proceed:
        raise typer.Abort()
    
    d = {}
    d['mod'] = module_id - 1
    d['iv'] = inputvoltage
    d['vcr'] = vcr
    d['tol'] = tolerance

    error, res = utils.do_post("{}/{}".format(ctx.obj.url, g_vars.API_DICT['input-set']['url']), 
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