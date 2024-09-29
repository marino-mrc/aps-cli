# Advanced Power Supply (APS) CLI
## What's the Advanced Power Supply?
The Advanced Power Supply is a modular electronic device I built from scratch based on a PIC32MZ microcontroller for powering clusters of single-board computers or Mini PCs.
It represents the ideal solution in low-power clusters (up to 2/3 KW) and edge computing solutions.

Some interesting features:
* Supports up to 16 devices (Mini PCs or SBCs)
* It can be used through the aps-cli or an optional touchscreen display
* Restful APIs for almost everything (per-port power consumption monitoring included)
* It supports _virtually_ all SBCs and Mini PCs with an operating voltage between 5 and 24V. The output power depends on the power supply you use. I successfully tested it with a total power of ~1KW shared between 8 Mini PCs with 32GB of RAM and an 8-core CPU per node
* It's fully compatible with [MaaS](https://maas.io/) and [Juju](https://juju.is/) by Canonical. This means you can efficiently provision clusters of Mini PCs and deploy applications on them using MaaS and Juju. MaaS handles the power management and the APS is fully compatible with it. K3s, K8s, OpenStack, and many other things in your lab without the hassle of powering off and on your devices!
* It's completely modular, hence the board can be easily customized based on your needs without buying a new PCB:
  * Removing the touchscreen is possible and this reduces the global cost of the board
  * Each "Switch Board" supports up to 8 devices (see the diagram below), but you can have 2 Switch Boards and the APS can manage up to 16 devices!
  * Various output voltages are supported, there is no need to change the schematic

![aps-diagram-white](https://github.com/marino-mrc/aps-cli/assets/1167190/4dd858b4-6f68-49e4-ae34-53420ebbdac2)

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
## V2 is coming
### What's new in V2?
* Supports up to 64 ports. Each board has 8 ports, you can scale up to 8 boards using a hardware bus
* The "control" board has been removed. You can use _any_ device with a serial port and one GPIO line (yes, Raspberry works)
* Additional 5V and 12V unmonitored output lines (for powering on the control board without any external power supply)
* Multiple power suppliers are supported _simultaneously_: it's possible to have 2 groups of 4 output ports and each group can have a different output voltage
* Maximum input current: 80A
* Maximum output current per line: 10A
* Supports the MeanWell “Programmable Output Voltage” function. More info [here](https://www.meanwell-web.com/content/files/pdfs/productPdfs/MW/UHP-1500/UHP-1500-spec.pdf)
* Agent on clients for advanced monitoring (TBD)
* Grafana dashboards through SNMP

## Images of the APS board

#### The APS board (Control + Switch board)
![aps_top_view_rotated](https://github.com/marino-mrc/aps-cli/assets/1167190/ae850f01-13ba-4b16-9aae-aee16bb57b51)

#### A cluster of x86_64 boards built with APS
![mylab](https://github.com/marino-mrc/aps-cli/assets/1167190/03aba38a-a6f2-42a3-8399-7b51e35331c2)

## How to contribute?
Please, ping me at marino dot mrc at gmail.com
I'm open to any type of collaboration on this project!

## Installing the required dependencis
```bash
git clone 
cd aps-cli
pip3 install poetry
poetry install
poetry shell
```


