"""
<plugin key="Zigpy" name="Zigpy plugin" author="pipiche38" version="0.0.1" wikilink="http://www.domoticz.com/wiki/plugins/plugin.html" externallink="https://www.google.com/">
    <description>
        <h2> Plugin Zigate for Domoticz </h2><br/>
    <h3> Short description </h3>
           This plugin allow Domoticz to access to the Zigate (Zigbee) worlds of devices.<br/>
    <h3> Configuration </h3>
          You can use the following parameter to interact with the Zigate:<br/>
    <ul style="list-style-type:square">
            <li> Model: Wifi</li>
            <ul style="list-style-type:square">
                <li> IP : For Wifi Zigate, the IP address. </li>
                <li> Port: For Wifi Zigate,  port number. </li>
                </ul>
                <li> Model USB ,  PI or DIN:</li>
            <ul style="list-style-type:square">
                <li> Serial Port: this is the serial port where your USB or DIN Zigate is connected. (The plugin will provide you the list of possible ports)</li>
                </ul>
            <li> Initialize ZiGate with plugin: This is a required step, with a new ZiGate or if you have done an Erase EEPROM. This will for instance create a new ZigBee Network. </li>
    </ul>
    <h3> Support </h3>
    Please use first the Domoticz forums in order to qualify your issue. Select the ZigBee or Zigate topic.
    </description>
    <params>
        <param field="Mode1" label="Zigate Model" width="75px" required="true" default="None">
            <options>
                <option label="USB" value="USB" default="true" />
                <option label="DIN" value="DIN" />
                <option label="PI" value="PI" />
                <option label="Wifi" value="Wifi"/>
                <option label="None" value="None"/>
            </options>
        </param>
        <param field="Address" label="IP" width="150px" required="true" default="0.0.0.0"/>
        <param field="Port" label="Port" width="150px" required="true" default="9999"/>
        <param field="SerialPort" label="Serial Port" width="150px" required="true" default="/dev/ttyUSB0"/>

        <param field="Mode3" label="Initialize ZiGate (Erase Memory) " width="75px" required="true" default="False" >
            <options>
                <option label="True" value="True"/>
                <option label="False" value="False" default="true" />
            </options>
        </param>

        <param field="Mode4" label="Listening port for Web Admin GUI " width="75px" required="true" default="9440" />

        <param field="Mode6" label="Verbors and Debuging" width="150px" required="true" default="None">
            <options>
                        <option label="None" value="0"  default="true"/>
                        <option label="Plugin Verbose" value="2"/>
                        <option label="Domoticz Plugin" value="4"/>
                        <option label="Domoticz Devices" value="8"/>
                        <option label="Domoticz Connections" value="16"/>
                        <option label="Verbose+Plugin+Devices" value="14"/>
                        <option label="Verbose+Plugin+Devices+Connections" value="30"/>
                        <option label="Domoticz Framework - All (useless but in case)" value="-1"/>
            </options>
        </param>
    </params>
</plugin>
"""


import Domoticz
import asyncio

# There are many different radio libraries but they all have the same API
from zigpy_zigate.zigbee.application import ControllerApplication


class MainListener:
    """
    Contains callbacks that zigpy will call whenever something happens.
    Look for `listener_event` in the Zigpy source or just look at the logged warnings.
    """

    def __init__(self, application):
        self.application = application

    def device_joined(self, device):
        print(f"Device joined: {device}")

    def attribute_updated(self, device, cluster, attribute_id, value):
        print(f"Received an attribute update {attribute_id}={value}"
              f" on cluster {cluster} from device {device}")

async def main():
    app = ControllerApplication(ControllerApplication.SCHEMA({
        "database_path": "/var/lib/domoticz/plugins/Domoticz-Zigpy/Datas/zigpy.db",
        "device": {
            "path": "/dev/ttyUSBRPI3",
        }

    }))

    listener = MainListener(app)
    app.add_listener(listener)

    await app.startup(auto_form=True)

    # Permit joins for a minute
    await app.permit(60)
    await asyncio.sleep(60)

    # Just run forever
    await asyncio.get_running_loop().create_future()


class BasePlugin:
    enabled = False
    def __init__(self):
        #self.var = 123
        pass

    def onStart(self):
        asyncio.run(main())
        Domoticz.Log("onStart called")

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
