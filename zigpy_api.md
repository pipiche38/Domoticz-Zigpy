# Document Zigpy how-to

## Principles

    1. Create a Persistent object to store all activities. Attention the API will be based on the zigpy-<hardware> layer you are going to use.
        * For the zigpy-zigate layer
            ```
            zigpyApp = await ControllerApplication.new
            (
                config=ControllerApplication.SCHEMA
                (
                    {
                    "database_path": "/tmp/zigpy.db",
                    "device": {
                        "path": "/dev/null", #/dev/ttyUSBRPI3",
                        }
                    }
                ),
                start_radio=True,
            )
            ```

    2. Create the Zigbee listner : 
        ```
        listener = MainListener( zigpyApp )
        self.zigpyApp.add_listener(listener)self.zigpyApp.add_listener(listener)
        ````

    3. Create a listner on each Cluster of each Device
        In order to receive the event from each device, you have to create a listner for each cluster of the device

    4. For IAS clusters, it needs to have cluster_command()
        Do not understand that one
        https://github.com/zigpy/zha-device-handlers/issues/469#issuecomment-685153282

### Define a class MainListener

    This is were you will be able to catch most of the events like:

    * When a device joined: def device_joined(self, device)
    * When a device is initialized (Called at runtime after a device's information has been queried.): device_initialized(self, device, *, new=True)
    * When an object send an update (attribute report or attribute read response): attribute_updated(self, cluster, attribute_id, value)

## Configuration SCHEMA

| Parameter | Description |
| --------  | ----------- |

| CONF_DATABASE = "database_path" |  path to access the persistent database (sqlite3) |

| CONF_DEVICE = "device" | 

| CONF_DEVICE_PATH = "path" | path to access the device controler (can be a serial line, IP )

| CONF_NWK = "network" |  ???
| CONF_NWK_CHANNEL = "channel" | I guess this is the channel to be use

| CONF_NWK_CHANNELS = "channels" | I guess this is a possible list of channel to be selected by the controller ?

| CONF_NWK_EXTENDED_PAN_ID = "extended_pan_id" | allow to specify the extended_pam_id (with Zigate it is only possible after an Erase PDM at Network Setup)

| CONF_NWK_PAN_ID = "pan_id" | allow to specify the PANID (in Zigate this is not authorized)

| CONF_NWK_KEY = "key" | ???

| CONF_NWK_KEY_SEQ = "key_sequence_number" | ???

| CONF_NWK_TC_ADDRESS = "tc_address" | ???

| CONF_NWK_TC_LINK_KEY = "tc_link_key" |  ???

| CONF_NWK_UPDATE_ID = "update_id" |  ???

| CONF_OTA = "ota" |  ???

| CONF_OTA_DIR = "otau_directory" |  Where to find the OTA Firmware

| CONF_OTA_IKEA = "ikea_provider" |  ???

| CONF_OTA_LEDVANCE = "ledvance_provider" | ???


# zigpy APIs

## Application

* raw_device_initialized
* device_initialized

* device_removed
* device_joined
* device_left

## Device

* node_descriptor_updated
* device_init_failure
* device_relays_updated

* get_signature
  Provide as a python Dictionnary , an Ep list and associated cluster In and Out. Unfortunatly do not provide more like Model Name, Manufacturer Code, Manufacturer Name ....
  

## Endpoint

* unknown_cluster_message
* member_added
* member_removed

## Group

* group_added
* group_member_added
* group_removed
* group_removed

## ZCL Commands

* cluster_command
* general_command
* attribute_updated
* device_announce
* permit_duration
