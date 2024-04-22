# SDN-based SFC with NSM

###Requirments to deploy the packet forwarder
* [Sysrepo python](https://github.com/sysrepo/sysrepo-python)

* [Sysrepo](https://github.com/sysrepo/sysrepo)

* [libyang](https://github.com/CESNET/libyang)

* [libnetconf](https://github.com/CESNET/libnetconf)

### NSM_example folder

Provides simple SFC scenarios with Kernel-type network interfaces for middleboxes using NSM. 
These scenarios may utilize a packet forwarder to ensure end-to-end connectivity between the 
sender and receiver. However, in the absence of a packet forwarder or any similar application, 
the internal traffic routing within the middleboxes must be managed manually.

## Folder structure
    .
    ├── NSM_examples         # SFC examples with kernel-type interfaces using NSM
    │   ├── 1middlebox       # A simple SFC scenario with 1 middlebox 
    │   └── 2middlebox       # A simple SFC scenario with 2 middleboxes with multipl Kernel-type NICs
    ├── pakcet_forwarder      
    │   ├── main.py          # Packet forwarder code
    │   ├── sfc-route.yang   # Yang model for packet forwarder
    │   └── simpleRoute.xml  # Simple XML for the packet forwarder Yang model
    └── ReadMe.md