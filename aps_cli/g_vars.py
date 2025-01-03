# Global variables file
from rich.console import Console

MAX_INPUT_PORTS = 2
MAX_OUTPUT_PORTS = 8
MAX_MODULES = 2
MIN_SPI_INTERVAL = 10
MAX_SPI_INTERVAL = 5000

API_DICT = {
    # Aps
    'status': {'url': 'status.json', 'method': 'get'},
    'spi-config': {'url': 'aps_config_spi.json', 'method': 'post'},
    'pw-change': {'url': 'aps_config_password.json', 'method': 'post'},
    # Ports
    'port-set': {'url': 'ports/set.json', 'method': 'post'},
    'port-status': {'url': 'ports/status.json', 'method': 'get'},
    'port-show': {'url': 'ports/details.json', 'method': 'get'},

    # Modules
    'module-status': {'url': 'modules/status.json', 'method': 'get'},
    'module-show': {'url': 'modules/details.json', 'method': 'get'},
    'module-set': {'url': 'modules/set.json', 'method': 'post'}, #To enable or disable a module
    'module-configure': {'url': 'modules/configure.json', 'method': 'post'}, #To configure a module

    # Network
    'net-show': {'url': 'config/net.json', 'method': 'get'}
}


MODULE_DICT = {
    'moduleType': { '0': 'Single Input', '1': 'Double Input'},
    'moduleStatus': { '0': 'Disconnected', '1': 'Connected' }
}
console = Console()