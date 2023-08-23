# Advanced Power Supply (APS) CLI
## What's the Advanced Power Supply
The Advanced Power Supply is an electronic board I built from scratch based on a PIC32MZ microcontroller for powering clusters of Single Board Computers or Mini PCs.

Some interesting features:
* The board supports up to 16 devices
* It can be used through the aps-cli or through a touchscreen display I added to the board
* It supports _virtually_ all SBCs and Mini PCs with a voltage between 5 and 24V
* It's fully compatible with [MaaS](https://maas.io/) by Canonical. This basically means you can provision MiniPC clusters in an efficient manner and deploy application on it using [Juju](https://juju.is/)
* It's completely modular, and this basically means that the board can be easily customized without buying a new PCB based on your needs:
  * Removing the touchscreen is possible and this permits reducing the global cost of the board
  * The minimum amount of supported devices is 8, but you can add another module and the APS can manage 16 boards!
  * Various output voltages are supported, no need to change the schematic

## Example usage
### Export env variables needed for connection and authentication:
```bash
$ export APS_URL="http://192.168.191.47"
$ export APS_USERNAME="admin"
$ export APS_PASSWORD="microchip"
```

### Check the status of all ports:
```bash
$ aps port-status
┏━━━━━━┳━━━━━━━━┓
┃ Port ┃ Status ┃
┡━━━━━━╇━━━━━━━━┩
│ 0    │ ON     │
│ 1    │ OFF    │
│ 2    │ ON     │
│ 3    │ ON     │
│ 4    │ ON     │
│ 5    │ ON     │
│ 6    │ ON     │
│ 7    │ OFF    │
│ 8    │ ON     │
│ 9    │ ON     │
│ 10   │ ON     │
│ 11   │ ON     │
│ 12   │ ON     │
│ 13   │ ON     │
│ 14   │ ON     │
│ 15   │ ON     │
└──────┴────────┘
```

### Check the status of a single port:
```bash
$ aps port-status 4
┏━━━━━━┳━━━━━━━━┓
┃ Port ┃ Status ┃
┡━━━━━━╇━━━━━━━━┩
│ 4    │ ON     │
└──────┴────────┘
```

### Change the status of a port:
```bash
$ aps port-set 1 off
Status: OFF
```

### Check the network configuration:
```bash
$ aps config net-show
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ Param    ┃ Value             ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ ip       │ 192.168.191.47    │
│ gw       │ 192.168.191.1     │
│ subnet   │ 255.255.255.0     │
│ dns1     │ 192.168.191.1     │
│ dns2     │ 0.0.0.0           │
│ mac      │ 44:b7:d0:a8:23:85 │
│ dhcp     │ true              │
│ hostname │ MCHPBOARD_E       │
└──────────┴───────────────────┘
```
## A picture of the old version of the APS board
![eps_v3 2_2](https://github.com/marino-mrc/aps-cli/assets/1167190/9fd55f41-1324-4f38-ba61-8253e6ca95d8)
