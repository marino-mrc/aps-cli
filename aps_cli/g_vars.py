# Global variables file
from rich.console import Console

API_DICT = {
    'port-set': {'url': 'port_set.json', 'method': 'post'},
    'port-status': {'url': 'port_status.json', 'method': 'get'},
    'port-show': {'url': 'port_details.json', 'method': 'get'},
    'net-show': {'url': 'config/net_details.json', 'method': 'get'},
    'net-change': {'url': 'config/net_change.json', 'method': 'post'},
    'pw-change': {'url': 'config/pw_change.json', 'method': 'post'},
    'adc-show': {'url': 'config/adc_details.json', 'method': 'get'},
    'input-show': {'url': 'config/input_details.json', 'method': 'get'},
    'input-set': {'url': 'config/input_set.json', 'method': 'post'},
    'module-show': {'url': 'config/module_details.json', 'method': 'get'},
    'module-set': {'url': 'config/module_set.json', 'method': 'post'}
}


MODULE_DICT = {
    'moduleType': { '0': 'Single Input', '1': 'Double Input'},
    'moduleStatus': { '0': 'Disconnected', '1': 'Connected' }
}
console = Console()