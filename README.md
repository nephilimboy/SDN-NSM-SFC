# SDN-based SFC with NSM
 
###Requirments to deploy the packet forwarder
* [Sysrepo python](https://github.com/sysrepo/sysrepo-python)

* [Sysrepo](https://github.com/sysrepo/sysrepo)

* [libyang](https://github.com/CESNET/libyang)

* [libnetconf](https://github.com/CESNET/libnetconf)


## Folder structure
    .
    ├── pakcet_forwarder      
    │   ├── main.py          # Packet forwarder code
    │   ├── sfc-route.yang   # Yang model for packet forwarder
    │   └── simpleRoute.xml  # Simple XML for the packet forwarder Yang model
    ├── ...
    └── ReadMe.md