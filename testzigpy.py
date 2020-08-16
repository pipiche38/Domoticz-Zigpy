import asyncio
import logging
#import coloredlogs
#coloredlogs.install(milliseconds=True, level=logging.DEBUG)

import threading

from zigpy.device import Device

# There are many different radio libraries but they all have the same API
from zigpy_zigate.zigbee.application import ControllerApplication
import zigpy.config as config

THREAD = True

APP_CONFIG = {
    config.CONF_DEVICE: {
        config.CONF_DEVICE_PATH: "/dev/ttyUSBRPI3",
    },
    config.CONF_DATABASE: "/var/lib/domoticz/plugins/Domoticz-Zigpy/Datas/zigpy.db",
}

LOGGER = logging.getLogger(__name__)

class MainListener:
    """
    Contains callbacks that zigpy will call whenever something happens.
    Look for `listener_event` in the Zigpy source or just look at the logged warnings.
    """

    def __init__(self, application):
        print("MainListener init")
        self.application = application


    def device_joined(self, device):
        # At that stage, only IEEE, NWKID are known.
        # We have to wait the full discovery completed.

        print(f"Device joined: {device}")
        print(" - NwkId: %s" %device.nwk)
        print(" - IEEE: %s" %device._ieee)

    def device_initialized(self, device, *, new=True):
        """
        Called at runtime after a device's information has been queried.
        I also call it on startup to load existing devices from the DB.
        """
        LOGGER.info("Device is ready: new=%s, device=%s", new, device)

        for ep_id, endpoint in device.endpoints.items():
            # Ignore ZDO
            if ep_id == 0:
                continue

            # You need to attach a listener to every cluster to receive events
            for cluster in endpoint.in_clusters.values():
                # The context listener passes its own object as the first argument
                # to the callback
                cluster.add_context_listener(self)


    def attribute_updated(self, cluster, attribute_id, value):
        # Each object is linked to its parent (i.e. app > device > endpoint > cluster)
        device = cluster.endpoint.device

        LOGGER.info("Received an attribute update %s=%s on cluster %s from device %s",
            attribute_id, value, cluster, device)

# def get_devices(self):
#         devices = []
# 
#         for ieee, dev in self.app.devices.items():
#             device = {
#                 "ieee": self._ieee_to_number(ieee),
#                 "nwk": dev.nwk,
#                 "endpoints": []
#             }
#             for epid, ep in dev.endpoints.items():
#                 if epid == 0:
#                     continue
#                 device["endpoints"].append({
#                     "id": epid,
#                     "input_clusters": [in_cluster for in_cluster in ep.in_clusters] if hasattr(ep, "in_clusters") else [],
#                     "output_clusters": [out_cluster for out_cluster in ep.out_clusters] if hasattr(ep, "out_clusters") else [],
#                     "status": "uninitialized" if ep.status == zigpy.endpoint.Status.NEW else "initialized"
#                 })
# 
#             devices.append(device)
#         return devices

async def main( ):

    import zhaquirks  # noqa: F401

    zigpyApp = await ControllerApplication.new(APP_CONFIG, auto_form=False)
        
    listener = MainListener(zigpyApp)
    zigpyApp.add_listener(listener)

    #await zigpyApp.startup(auto_form=False)
    await zigpyApp.form_network( channel=11 )

    # Permit joins for a minute
    await zigpyApp.permit(240)
    await asyncio.sleep(240)

    # Just run forever
    await asyncio.get_running_loop().create_future()




def zigpy_thread( ):
    print("Start thread")
    asyncio.run(main())
    print("Stop thread")

def launch_thread( ):

    print("Launch thread")
    zigpyThread = threading.Thread(
                        name="ZigpyThread", 
                        target=zigpy_thread,
                        args=())
    zigpyThread.start()    
    print("Thread launched")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if THREAD:
        launch_thread()
    else:
        asyncio.run(main())

