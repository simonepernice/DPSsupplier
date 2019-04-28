DPSsupplier

DPS supplier driver and graphical interface management software written by Simone Pernice

DPS supplier should be able to run on Python 2.x and 3.x on both Linux and Windows OS.

DPS supplier is an open source driver and software to manage DPS converter via USB.

DPS devices are a set of DC-DC converter controllable via serial interface (through USB or bluetooth).

DPS suppliers are available in several versions called DPSxxyy where:
-xx is the maximum output voltage
-yy is the maximum output current

Some version available are showed below:

- DPS3005 (max output voltage 30V, max output current 5A)
- DPS3015 (max output voltage 30V, max output current 15A)
- DPS5005 (max output voltage 50V, max output current 5A)
- DPS5015 (max output voltage 50V, max output current 15A)
- DPS5020 (max output voltage 50V, max output current 20A)

DPS supplier  has several functions:

- Measure output voltage
- Measure output current
- Set output voltage-current to work in voltage-current mode
- Set protection against voltage, current, power
- Enable/disable output
- Set display brightness
- Enable/disable keys
- Memories (9) with preset values for all the above settings
- ...

It but it can be difficult manage all those setting through the DPS because it has very few inputs (a knob and 3 buttons). 

A management software is available but it is closed source and only for Windows.

At the beginning my purpose was to write a DPS driver for python to manage the DPS interactively through the command line. However once I made the driver I decide to build an user interface. The user interface allow new functions:

- DPS acquired parameters are used to display voltage, current and power in a time diagram
- It is possible to draw a waveform that will be reproduced by DPS converter

Those programs are available as open source software under GPL 3.0.

The DPS driver depends on those modules:

- pyserial to use the USB port as a serial port (a version is provided with this package)
- modbus-tk to send modbus commands over serial port (a version is provided with this package)

To use the graphical interface it is also required to install Tk-interface.



