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

### Define a class MainListener

    This is were you will be able to catch most of the events like:

    * When a device joined: def device_joined(self, device)
    * When a device is initialized (Called at runtime after a device's information has been queried.): device_initialized(self, device, *, new=True)
    * When an object send an update (attribute report or attribute read response): attribute_updated(self, cluster, attribute_id, value)


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