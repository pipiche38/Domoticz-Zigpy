# Zigpy plugin for Domoticz

## Introduction

Rely on the zigpy library to interface with all Zigbee related HW and provide a coherent/consistent and uniq API.

## Design Principle

In order to cohexist with the Domoticz Python Plugin Framework, a dedicated thread will be lauched a plugin start to handle all zigpy related matters.

As of the ZiGate plugin, Domoticz Widgets will be created based on the Zigbee device capabilities. Most likely the device signature from a Zigpy standpoint. Basically based on the Cluster list by device.

In order to identify each device in Domoticz with a plugin uniq identifier, the IEEE will be used, this prevent any issues when the device changes its short address (NwkId).

onMessage won't be use as zigpy will open the communication line with the HW.

Keep the same principle as for the ZiGate plugin, no middle application in between. Makes the plugin fully autonomous and bridge Domoticz to the HW.

Will most-likely required a Web Admin page in order to :

* Configure the plugin
* Configure the HW ( channel, Extended PANId, Power, Led .... )
* Manage Groups
* Manage Bindings
* Display device mapping
* ...

### To be considered

1. How to configured the Zigpy HW layer to be used ? Basically from my current understand you need to import a specific "zigpy_[zigbee hardware]" module to interface with the corresponding HW. Some will enabled some features, some other not. How to handle that (independently) ?

1. How to handle device update. From my current undestanding we get async call, and if we use them straigh to update the Domoticz Database, we might have some reentrance issues. Most-likely a lock mecanism needs to be in place to protect the Domoticz Database update (at least at the python framework level).

1. How to handle Device provisioning ? End to End

1. Would it be possible to migrate Zigate users from Domoticz-Zigate plugin to Domoticz-Zigpy plugin ? From a pure HW perspective the ZiGate doesn't really care of who is using it. From a plugin standpoinit it might be interested to see if from the ZiGate plugin we could populate the Zigpy database ?
