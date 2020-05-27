# PyControl
README Languages: [PT](README-pt.md) | [EN](README.md) \

## Description
Simple python script to control another computer's keyboard and mouse through network

## Prerequisites
1. [Python 3.x](https://www.python.org/downloads/).
2. [Package installer for Python (pip)](https://pypi.org/project/pip/), to install pynput.
3. [pynput library](https://pypi.org/project/pynput/), to listen and control keyboard and mouse input.

## Warning
It is not recommended to run this script in an unsafe network.
An attacker could easily execute arbitrary commands on the server machine.

## Using this tool

### Running the server
On the computer you want to control, run the server.
By default it runs on port TCP 1234. 
To keep the code simple, I didn't add an option to change the port. 
But you can change it by setting the port variable value (line 12).

To run the server, execute:
```
./pycontrol.py
```

### Controlling the computer
To control the computer, get the IP address of the computer that is running the server and execute:

```
./pycontrol.py <ADDRESS>
```

### Escape key
The escape key disables and enables the control of the other machine.
By default it is the Right Control key, but you can change it by adding a third
argument in line 22, for example:

```
client = Client(addr, port, Key.tab)
```
This changes the escape key to the tab key.

## Final tip
You can also control a computer outside your LAN, setting a port forwarding 
on the router it is connected, or using some service like [ngrok](https://ngrok.com/).

## Authors
* **Igor Costa Melo**
