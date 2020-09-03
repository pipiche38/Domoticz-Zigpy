# Zigpy plugin for Domoticz

## Introduction

[Domoticz-Zigpy](https://github.com/zigpy/zigpy) is an integration project which goal is to implement Zigbee support in [Domoticz] home automation software using the zigpy Python library.

Zigbee integration via zigpy will allow users to directly connect one of many off-the-shelf Zigbee adapters from different manufacturers using one of the available Zigbee radio library modules compatible with the zigpy API to control Zigbee based devices. This can enable the use of the same common interface no matter which hardware users have.

- <https://github.com/zigpy/zigpy>

## LIMITATIONS

* Currently Zigpy librarry do not provide to interact directly with the hardware (Zigbee radio). For instance in the context of the ZiGate
  * Not posibility to reset the PDM and erase the all memory. That is a shame as this is quiet convenient to get a clean situation
  * No access to the Led control
  * No access to the Certification CE or FCC
  * No access to the Power/Energy level 
  

## WARNING

For now there are a number of show stoppers to go forward:

   * Domoticz issue, there are some conflict around SQLITE3 usage [Issue #4312](https://github.com/domoticz/domoticz/issues/4312)
   * Zigpy library and quirk are developped for Home Automation with no documentation on how to use. These are very focus on the HA design. Using Zigpy on Domoticz required a lot of work at that stage :
      1. Understand how to use zigpy
      1. Understand what to do in order to have a correct setup (inside the plugin) to get all events from devices
      
   * Zigpy has not a lot of manufacturer device support. During my work on the proof of concept, quiet a number of the devices that I'm using often for my devlopement and tests where not full supported and created error messages. The end result would be for the current ZiGat users a lack of supported devices.
      * Aqara Opple Switches not supported
      * Xiaomi Vibration making errors
      * Legrand devices not supported (leave the network after a while )
   
   * The Zigate layer is not really mature and is at an early stage. That mean that we wouldn't have such integration level with ZiGate as we have currently with the ZiGate plugin for Domoticz.
   
   

Unfortunatly at that stage, I'm not able to move forward:

1. Risk to develop a plugin based on assumption that Domoticz sqlite3 issue will be fixed.
1. Required a lot of time to be spent in order to understand how the zigpy library .



## Design Principle

As of the ZiGate plugin, Domoticz Widgets will be created based on the Zigbee device capabilities. Most likely the device signature from a Zigpy standpoint. Basically based on the Cluster list by device.

In order to identify each device in Domoticz with a plugin uniq identifier, the IEEE will be used, this prevent any issues when the device changes its short address (NwkId).

onMessage won't be use as zigpy will open the communication line with the HW.

Keep the same principle as for the ZiGate plugin, no middle application in between. Makes the plugin fully autonomous and bridge Domoticz to the HW.

Try to ease the integration of the Zigate plugin . There are quiet a large developement done like Schneider (where we simulate more-less the HUB) , and it would benefit to the new plugin. In such it might be helpfull to keep a number of API common between the 2 plugins !

### Threads (to be claified)

1. The PythonPluginThread (main thread).
1. One thread will be dedicated to the Zigbee layer and will manage the all zigpy part
1. One thread will manage the Domoticz layer ( Widget creation and all updates required by inbound communition from Zigbee )
1. A communication scheme (Queue) will be put in place to ensure communication between the 3 threads:
   * zigpy thread <-> domoticz thread
   * main thread <-> zigpy thread)

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


## Details on the Zigpy project

This project as such will rely on multiple radio libraries from the zigpy project as a dependency to interface 
with Zigbee radios which all aim to provide a coherent and consistent API in order among them to make it 
easier for integrations to support multiple adapters for different hardware manufacturers. For now though it 
is only being tested with the ZiGate hardware using the zigpy-zigate radio library.

- [bellows - zigpy radio library supporting Silicons Labs EmberZNet based Zigbee radios](https://github.com/
zigpy/bellows)
- [zigpy-cc - zigpy radio library supporting older Texas Instruments Z-Stack (CC253x) based Zigbee radios]
(https://github.com/zigpy/zigpy-cc)
- [zigpy-deconz - zigpy radio library supporting dresden dlektronik deCONZ (ConBee and RaspBee) based Zigbee 
radios](https://github.com/zigpy/zigpy-deconz)
- [zigpy-xbee - zigpy radio library supporting XBee based Zigbee radios](https://github.com/zigpy/zigpy-xbee)
- [zigpy-zigate - zigpy radio library supporting ZiGate based Zigbee radios](https://github.com/zigpy/
zigpy-zigate)
- [zigpy-znp - zigpy radio library supporting newer Texas Instruments Z-Stack (CC2652 and CC1352) based Zigbee 
radios](https://github.com/zha-ng/zigpy-znp)

It addition it will utilize the zha-device-handlers (a.k.a. zha-quirks) library from the zigpy project as a 
dependency as it will act as a tranaslator to try to handle individual Zigbee device exception and deviation 
handling for those Zigbee devices that do not fully conform to the standard specifications set by the Zigbee 
Alliance.

- <https://github.com/zigpy/zha-device-handlers>
