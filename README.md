# Zigpy plugin for Domoticz

## Introduction

Rely on the zigpy library to interface with all Zigbee related HW and provide a coherent/consistent and uniq API.

## Design Principle

In order to cohexist with the Domoticz Python Plugin Framework, a dedicated thread will be lauched a plugin start to handle all zigpy related matters.

As of the ZiGate plugin, Domoticz Widgets will be created based on the Zigbee device capabilities. Most likely the device signature from a Zigpy standpoint. Basically based on the Cluster list by device.

In order to identify each device in Domoticz with a plugin uniq identifier, the IEEE will be used, this prevent any issues when the device changes its short address (NwkId).

onMessage won't be use as zigpy will open the communication line with the HW.

