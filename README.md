# LED String Emulator for AtHomeLED
Copyright © 2019 by Dave Hocker

## Overview
This app was designed to be a test tool for the AtHomeLED LED controller.
It basically provides a string of LEDs that can be driven by AtHomeLED
scripts. The number of LEDs defaults to 50, but can be changed through
a configuration file.

The **test_client.py** file serves as both a test of the emulator and a programming
example of how to use the emulator.

## Setup
The app requires Python 3 (>=3.6). The simplest setup is to create a
VENV using the requirements.txt file.

## Configuration

## Quick Test
Open a terminal window and activate the VENV. Start the emulator.

    python led-emulator.py

You should see the emulator window.

Open a second terminal window and run the test client.

    python3 test_client.py

The emulator window should show changing LEDs as the emulator is
driver by the test client.

## API
The app acts as a server. A client connects to the server (default port 5555)
and sends it LED data frames. Each LED data frame contains all of the data
for the emulated LED string.

### LED Data Frame
A LED data frame contains the following.

    Header
    Body
    Trailer

Where:

Header = 4 bytes of 0x00

Body = (n * 4) bytes of (brighness, r, g, b) data where n is the number
of LED pixels

Trailer = 4 bytes of 0xFF
