# Advanced Power Supply (APS) CLI
## What's the Advanced Power Supply?
The [**Advanced Power Supply (APS)**](https://gitlab.marino-mrc.com/aps/aps-server) is an electronic device I designed and developed from scratch to manage the power supply for clusters of single-board computers (SBCs) or Mini PCs.  
It is an ideal solution for low-power clusters (up to 2–3 kW) and edge computing environments.<br/><br/>
This repo contains the Python CLI to interact with the Advanced Power Supply.

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
│ mac      │ 44:b7:d0:a8:23:85 │
│ dhcp     │ true              │
└──────────┴───────────────────┘
```

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


