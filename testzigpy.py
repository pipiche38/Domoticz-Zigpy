import asyncio
import logging
import threading

from zigpy.device import Device

# There are many different radio libraries but they all have the same API
from zigpy_zigate.zigbee.application import ControllerApplication
import zigpy_zigate.config as config

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
        print(f"Device joined: {device}")
        print(" - NwkId: %s" %device.nwk)
        print(" - IEEE: %s" %device._ieee)
        print(" - LQI: %s" %device.lqi)
        print(" - RSSI: %s" %device.rssi)
        
        for key, endp in device.endpoints.items():
            LOGGER.info("endpoint %s", key)

            if hasattr(endp, "in_clusters"):
                LOGGER.info("in_clusters %s", endp.in_clusters)
                LOGGER.info("out_clusters %s", endp.out_clusters)

                asyncio.sleep(2)
                endp.out_clusters[8].bind()

                    
        #print(" - Manuf: %s" %device.manufacturer())
        #print(" - Model: %s" %device.model())

        print(" - Signature: %s" %device.get_signature())

    def attribute_updated(self, device, cluster, attribute_id, value):
        print(f"Received an attribute update {attribute_id}={value}"
              f" on cluster {cluster} from device {device}")


async def main( ):

    import zhaquirks  # noqa: F401

    try:
        zigpyApp = ControllerApplication(APP_CONFIG)
        
    except KeyError:
        LOGGER.error("DB error, removing DB...")



    listener = MainListener(zigpyApp)
    zigpyApp.add_listener(listener)

    await zigpyApp.startup(auto_form=False)
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
    launch_thread()
    #asyncio.run(main())
