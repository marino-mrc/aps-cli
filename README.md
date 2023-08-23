# Advanced Power Supply (APS) CLI
## What's the Advanced Power Supply
The Advanced Power Supply is an electronic board I built from scratch based on a PIC32MZ microcontroller for powering clusters of Single Board Computers or Mini PCs.

Some interesting features:
* The board supports up to 16 devices
* It and can be used through the aps-cli or through a touch screen display I added to the board
* It supports _virtually_ all SBCs and Mini PCs with a voltage between 5 and 24V
* It's fully compatible with [MaaS](https://maas.io/) by Canonical. This basically means you can provision MiniPC clusters in an efficient manner
* It's completely modular, and this basically means that the board can be easily customized without buying a new PCB based on your needs:
  * Removing the touchscreen is possible and this permits to reduce the global cost
  * The minimum amount of supported devices is 8, but you can add another module and the APS can manage 16 boards!
  * Various output voltage are supported, no need to change the schematic

## Example usage

## Some images of the APS board 

