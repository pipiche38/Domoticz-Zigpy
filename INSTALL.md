# How to install the zigpy environment on RPI4 

## Current version:
`Linux raspberrypi 4.19.75-v7l+ #1270 SMP Tue Sep 24 18:51:41 BST 2019 armv7l GNU/Linux`


1. Make sure you have the latest pip setuptools
   `pip install -U setuptools``


1. Install the zigpy zha-quirks libraries and their dependencies.
pip3 install zigpy-zigate zha-quirks zigpy



## Notes

My current development platform is :

* RPI3B+
* Fedora 32
* Zigate ( USB, DIN, RPI)

### Installation (Fedora specific )

* Under Fedora32 it looks like there are some conflict between the various python3 librariries used by zigpy and mainly zigpy-zigate.
* In order to get closer to the end users, all the zigpy related libraries and dependencies are directly installed on the directory where the Domoticz plugin is.
  * `pip3 install -t . zigpy zha-device-handlers`
  
  * For zigpy-zigate I have done the following as `pip3 install -t zigpy-zigate` failed.
    ```
    pip3 install -t . pyserial
    git clone https://github.com/pyserial/pyserial-asyncio.git
    git clone https://github.com/zigpy/zigpy-zigate.git
    ln -s zigpy-zigate/zigpy_zigate zigpy_zigate
    ln -s pyserial-asyncio/serial_asyncio serial_asyncio
    ```

