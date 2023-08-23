# Global variables file
from rich.console import Console

API_DICT = {
    'set-port': {'url': 'set_port.json', 'method': 'get'},
    'port-status': {'url': 'port_status.json', 'method': 'get'},
    'net-show': {'url': 'config/net_details.json', 'method': 'get'}
}

console = Console()