# Global variables file
from rich.console import Console

API_DICT = {
    'port-set': {'url': 'port_set.json', 'method': 'get'},
    'port-status': {'url': 'port_status.json', 'method': 'get'},
    'port-show': {'url': 'port_details.json', 'method': 'get'},
    'net-show': {'url': 'config/net_details.json', 'method': 'get'},
    'net-change': {'url': 'config/net_change.json', 'method': 'post'}
}

console = Console()