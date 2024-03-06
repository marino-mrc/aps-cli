# Global variables file
from rich.console import Console

API_DICT = {
    'port-set': {'url': 'port_set.json', 'method': 'post'},
    'port-status': {'url': 'port_status.json', 'method': 'get'},
    'port-show': {'url': 'port_details.json', 'method': 'get'},
    'net-show': {'url': 'config/net_details.json', 'method': 'get'},
    'net-change': {'url': 'config/net_change.json', 'method': 'post'},
    'pw-change': {'url': 'config/pw_change.json', 'method': 'post'},
    'https-change': {'url': 'config/https_change.json', 'method': 'post'},
    'adc-show': {'url': 'config/adc_details.json', 'method': 'get'},
    'power-show': {'url': 'config/power_details.json', 'method': 'get'}
}

console = Console()