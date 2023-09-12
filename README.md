# Advanced Power Supply (APS) CLI
## What's the Advanced Power Supply?
The Advanced Power Supply is a modular electronic board I built from scratch based on a PIC32MZ microcontroller for powering clusters of single-board computers or Mini PCs.
It represents the ideal solution in low-power clusters (up to 2/3 KW) and edge computing solutions.

Some interesting features:
* Supports up to 16 devices (Mini PCs or SBCs)
* It can be used through the aps-cli or through an optional touchscreen display I added
* Restful APIs for almost everything (per-port power consumption monitoring included)
* It supports _virtually_ all SBCs and Mini PCs with an operating voltage between 5 and 24V. The output power depends on the power supply you use. I successfully tested it with a total power of 1KW shared between 8 Mini PCs with 32GB of RAM and an 8-core CPU per node
* It's fully compatible with [MaaS](https://maas.io/) and [Juju](https://juju.is/) by Canonical. This basically means you can provision clusters of Mini PCs in an efficient manner and deploy applications on them using MaaS and Juju. The power management is handled by MaaS and the APS is fully compatible. K3s, K8s, OpenStack, and many other things in your lab without the hassle of powering off and on your devices!
* It's completely modular, hence the board can be easily customized without buying a new PCB based on your needs:
  * Removing the touchscreen is possible and this reduces the global cost of the board
  * Each "Switch Board" supports up to 8 devices (see the diagram below), but you can have 2 Switch Boards and the APS can manage up to 16 devices!
  * Various output voltages are supported, no need to change the schematic

![APS diagram](https://github.com/marino-mrc/aps-cli/assets/1167190/093a1e4e-9cae-4159-977d-2213fc422c52)

The firmware of the APS board can be freely downloaded from [here](https://github.com/marino-mrc/aps-firmware). The schematic will be available soon.

## CLI Example Usage
#### Export env variables needed for connection and authentication:
```bash
$ export APS_URL="http://192.168.191.47"
$ export APS_USERNAME="admin"
$ export APS_PASSWORD="microchip"
```

#### Check the status of all ports:
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

#### Check the status of a single port:
```bash
$ aps port-status 4
┏━━━━━━┳━━━━━━━━┓
┃ Port ┃ Status ┃
┡━━━━━━╇━━━━━━━━┩
│ 4    │ ON     │
└──────┴────────┘
```

#### Change the status of a port:
```bash
$ aps port-set 1 off
Status: OFF
```

#### Check the network configuration:
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
## Images of the APS board

#### The control board
![control_board_c](https://github.com/marino-mrc/aps-cli/assets/1167190/34f1e602-7b5f-4a2b-8981-a646a62db12f)

#### The Switch Board
![switch_board_c](https://github.com/marino-mrc/aps-cli/assets/1167190/76bfedb5-3608-44c8-93e6-4933f23b1406)

#### A cluster of ARM64 boards built with an old version of my APS
![cluster_aps_old_c](https://github.com/marino-mrc/aps-cli/assets/1167190/2bcf0493-5d98-402b-a8d6-2193d4d6e372)

## How to contribute?
Please, ping me at marino dot mrc at gmail.com
I'm open to any type of collaboration on this project!

