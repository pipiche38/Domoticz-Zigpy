# Zigpy plugin for Domoticz

UNFORTUNATLY THIS PROJECT IS CLOSE, DUE TO THE FACT THAT THE ZIGPY LIBRARY IS NOT COMPATIBLE WITH DOMOTICZ (OR VICE-VERSA).

## Introduction

[Domoticz-Zigpy](https://github.com/zigpy/zigpy) is an integration project which goal is to implement hardware independent Zigbee support in [Domoticz](https://www.domoticz.com/) open source home automation software using the [https://github.com/zigpy/zigpy/ zigpy] Python library.

Zigbee integration via zigpy this way would allow users to directly connect one of many off-the-shelf Zigbee adapters from different manufacturers using one of the available Zigbee radio library modules compatible with the zigpy API to control Zigbee based devices, without the need for a third-party gateway/hub/bridge that needs to be managed separately. This can enable the use of the same common interface no matter which Zigbee hardware adapter that users have. 

The ultimate goal of zigpy (often also refered to as "zigpy library" or "zigpy project") is to be a free and open source software library that can interface with a Zigbee coordinator (sometimes referred to as a Zigbee controller) from any manufacturer and allow anyone who integrates zigpy to create applications to control devices on a Zigbee network, without requiring a very deep knowledge of the Zigbee specifications and manufacturer proprietary implementations.

The zigpy Github Organization is located at https://github.com/zigpy/. There are several repositories at that location. Their README of the main project , located in the https://github.com/zigpy/zigpy/ repository. This software is aimed at application developers who wish to incorporate or integrate Zigbee functionality into their applications. The project consists of the main zigpy library, wrappers for Zigbee radios from different manufacturers, and supporting projects, all written in Python.

## WARNING!!! - Work in progress

This project at this early stage is more a developers-only POC (Proof-Of-Concept) than anything else, as such users should not expect anything with it to work as of yet.

Due to a bug ( https://github.com/domoticz/domoticz/issues/4312 ) this plugin does not currently work at all with a standard Domoticz binary file.
This means that in order to be able to test this plugin the Domoicz application must at this time first be recompiled and linked with disabling the use of "BUILTIN_SQLITE".
To do that, edit the file CMakeList.txt and disable the "Use of builtin sqlite library" in order to link with the standard SQLITE3 library.
`option(USE_BUILTIN_SQLITE "Use builtin sqlite library" NO)`

## Current showstoppers

For now there are a number of show stoppers that need to be solved/sorted/fixed or have a more acceptable workaround before can move forward:

   * Domoticz issue, there are some conflict around SQLITE3 usage [Issue #4312](https://github.com/domoticz/domoticz/issues/4312)
   * Zigpy library and quirk are developped for Home Automation with no documentation on how to use. These are very focus on the HA design. Using Zigpy on Domoticz required a lot of work at that stage :
      1. Understand how to use zigpy
      2. Understand what to do in order to have a correct setup (inside the plugin) to get all events from devices
      
   * Zigpy has not a lot of manufacturer device support. During my work on the proof of concept, quiet a number of the devices that I am using often for my devlopement and tests where not full supported and created error messages. The end result would be for the current ZiGat users a lack of supported devices.
      * Aqara Opple Switches not supported
      * Xiaomi Vibration making errors
      * Legrand devices not supported (they leave the network after a while)
   
   * The Zigate layer is not really mature and is at an early stage. That mean that we would not have such integration level with ZiGate as we have currently with the ZiGate plugin for Domoticz.
   

Unfortunatly at that stage, I am probably not able to move forward:

1. Risk to develop a plugin based on assumption that Domoticz sqlite3 issue will be fixed.
2. Required a lot of time to be spent in order to understand how the zigpy library .


## TO BE ADDRESSED

* [IMPORTANT] Performance (response-time). The proof-of-concept implemenation has been developed with a LUMI Motion Sensor from Xiaomi/Aquara. This communicate 2 events ( Motion detection via Cluster 0x0406 and Illuminence via cluster 0x0400 ). 
  * This is using the "quirk" part (from [ZHA Device Handlers](https://github.com/zigpy/zha-device-handlers/)), and I do not fully understand how it works (especially in regards to that issue https://github.com/zigpy/zha-device-handlers/issues/469 - I do not understand what Cluster IAS should do here!)
  * But in general I found the performance not as expected. Quiet some lag between the Motion and the event reported into the plugin layer (not the Domoticz itself). The lag could be at several levels:
    * Maybea localized issue only with Xiaomi/Aquara LUMI devices? Maybe even localized issue only with battery-operated Xiaomi/Aquara LUMI devices?
    * zigpy-zigate as the implementation is quiet early?
    * Difference between the asyncio and the all zigpy stack in comparaison with the zigate plugin which is fully asynchrone with no waiting and synchronisation mecanism? From what I have measured with the zigate plugin the delay between receiving a message from the UART and getting the update on Domoticz widget is around 3ms. Here I have the impression that an important lag  between a motion should be detected, and the time the motion is seen by the app layer .
  * I had the impression that doing two pairing at the same time could be problematic - but need to be checked again, as I do not see why.

* zigpy provides a method call get_signature() which is available on the device object and provide a "device signature". In other words it gives in a python dictionary format informations like:
  * List of Endpoints
  * List of Cluster In and CLuster Out for each Endpoint
  
  I found the information useful, but currently too restrictive in regards of a device. For instance if get_signature() could returned information like:
    * Model Name (provided by Cluster 0x0000 Attribute 0x0005 )
    * Manufacturer Code
    * Manufacturer Name
    * DeviceID (which is EndPoint based) and which can give information on the purpose of the device
    

## LIMITATIONS

* Currently Zigpy library do not provide to interact directly with all the hardware features on a Zigbee radio. For instance in the context of the ZiGate coordinator:
  * Currently not posibility to reset the PDM and erase the all memory. That is a shame as this is quiet convenient to get a clean situation
  * Currently no access to the LED control
  * Currently no access to the Certification CE or FCC
  * Currently no access to the TX Power / Energy level
  * Currently no access to ZiGate reset ( which is quiet convenient when hang). The reset allow to reboot the Zigbee stack of the zigate without any break.


## Design Principle

As of the ZiGate plugin, Domoticz Widgets will be created based on the Zigbee device capabilities. Most likely the device signature from a Zigpy standpoint. Basically based on the Cluster list by device.

In order to identify each device in Domoticz with a plugin uniq identifier, the IEEE will be used, this prevent any issues when the device changes its short address (NwkId).

onMessage will not be use as zigpy will open the communication line with the HW.

Keep the same principle as for the ZiGate plugin, no middle application in between. Makes the plugin fully autonomous and bridge Domoticz to the HW.

Try to ease the integration of the Zigate plugin . There are quiet a large developement done like Schneider (where we simulate more-less the HUB) , and it would benefit to the new plugin. In such it might be helpfull to keep a number of API common between the 2 plugins !

Two-steps approach could be taken:
1. Building a kind of layer between the zigpy and the existing zigate plugin in order to speedup and reuse the existing code and make the integration at a similar level of the current Zigate plugin with the admin interface.
   * It will anyway remove some of the existing code, as the quirk will provide "native" what is currently embedded in the zigate plugin code.
   * On the otherside, need to see how to faster the existing Device integration and get quirks for them ( Legrand is an important one, Livolo ....)
2. Refactor the code to use the zigpy power.

### Threads (to be clarified)

1. The PythonPluginThread (main thread).
2. One thread will be dedicated to the Zigbee layer and will manage the all zigpy part
3. One thread will manage the Domoticz layer ( Widget creation and all updates required by inbound communition from Zigbee )
4. A communication scheme (Queue) will be put in place to ensure communication between the three threads:
   * zigpy thread <-> domoticz thread
   * main thread <-> zigpy thread

Will most-likely required a Web-Admin page in order to:

* Configure the plugin
* Configure the port (baud rate, serial-port or socket and port for IP gateways like ZiGate WiFi)
* Configure the HW ( channel, Extended PANId, TX Power, LED .... )
* Manage Groups
* Manage Bindings
* Display device mapping
* ...

### To be considered

1. How to configure the Zigpy hardware layer to be used? Basically from my current understand you need to import a specific "zigpy-**[zigbee hardware]**" radio library as a module to interface with the corresponding hardware. Some of those radio libraries will have enabled some features while some others have not. How to handle that (independently) for each radio library and hardware?

2. How to handle device update. From my current undestanding we get async call, and if we use them straigh to update the Domoticz Database, we might have some reentrance issues. Most-likely a lock mecanism needs to be in place to protect the Domoticz Database update (at least at the python framework level).

3. How to handle Device provisioning? End-to-End.

4. Would it be possible to migrate Zigate users from Domoticz-Zigate plugin to Domoticz-Zigpy plugin? From a pure HW perspective the ZiGate firmware does not really care of who is using it. From a plugin standpoinit it might be interested to see if we could populate the Zigpy database from the ZiGate plugin or vice versa?


## Details on the Zigpy project

This project as such will rely on multiple radio libraries from the zigpy project as a dependency to interface 
with Zigbee radios which all aim to provide a coherent and consistent API in order among them to make it 
easier for integrations to support multiple adapters for different hardware manufacturers. For now though it 
is only being tested with the ZiGate hardware using the zigpy-zigate radio library.

- [bellows - zigpy radio library supporting Silicons Labs EmberZNet based Zigbee radios](https://github.com/zigpy/bellows)
- [zigpy-znp - zigpy radio library supporting newer Texas Instruments Z-Stack (CC2652 and CC1352) based Zigbee 
radios](https://github.com/zha-ng/zigpy-znp)
- [zigpy-deconz - zigpy radio library supporting dresden dlektronik deCONZ (ConBee and RaspBee) based Zigbee 
radios](https://github.com/zigpy/zigpy-deconz)
- [zigpy-xbee - zigpy radio library supporting XBee based Zigbee radios](https://github.com/zigpy/zigpy-xbee)
- [zigpy-zigate - zigpy radio library supporting ZiGate based Zigbee radios](https://github.com/zigpy/zigpy-zigate)

It addition it will utilize the zha-device-handlers (a.k.a. zha-quirks) library from the zigpy project as a 
dependency which will act as a tranaslator to try to handle individual Zigbee device exception and deviation 
handling for those Zigbee devices that do not fully conform to the standard specifications set by the Zigbee 
Alliance.

- <https://github.com/zigpy/zha-device-handlers>
