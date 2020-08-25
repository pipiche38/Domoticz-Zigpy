# Zigpy plugin for Domoticz

## Introduction

[Domoticz-Zigpy](https://github.com/zigpy/zigpy) is an integration project which goal is to implement Zigbee support in [Domoticz] home automation software using the zigpy Python library.

Zigbee integration via zigpy will allow users to directly connect one of many off-the-shelf Zigbee adapters from different manufacturers using one of the available Zigbee radio library modules compatible with the zigpy API to control Zigbee based devices. This can enable the use of the same common interface no matter which hardware users have.

- https://github.com/zigpy/zigpy

This project as such will rely on multiple radio libraries from the zigpy project as a dependency to interface with Zigbee radios which all aim to provide a coherent and consistent API in order among them to make it easier for integrations to support multiple adapters for different hardware manufacturers. For now though it is only being tested with the ZiGate hardware using the zigpy-zigate radio library.

- [bellows - zigpy radio library supporting Silicons Labs EmberZNet based Zigbee radios](https://github.com/zigpy/bellows)
- [zigpy-cc - zigpy radio library supporting older Texas Instruments Z-Stack (CC253x) based Zigbee radios](https://github.com/zigpy/zigpy-cc)
- [zigpy-deconz - zigpy radio library supporting dresden dlektronik deCONZ (ConBee and RaspBee) based Zigbee radios](https://github.com/zigpy/zigpy-deconz)
- [zigpy-xbee - zigpy radio library supporting XBee based Zigbee radios](https://github.com/zigpy/zigpy-xbee)
- [zigpy-zigate - zigpy radio library supporting ZiGate based Zigbee radios](https://github.com/zigpy/zigpy-zigate)
- [zigpy-znp - zigpy radio library supporting newer Texas Instruments Z-Stack (CC2652 and CC1352) based Zigbee radios](https://github.com/zha-ng/zigpy-znp)

It addition it will utilize the zha-device-handlers (a.k.a. zha-quirks) library from the zigpy project as a dependency as it will act as a tranaslator to try to handle individual Zigbee device exception and deviation handling for those Zigbee devices that do not fully conform to the standard specifications set by the Zigbee Alliance.

- https://github.com/zigpy/zha-device-handlers

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
