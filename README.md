vdsm_quantum
============

VDSM and Quantum

Contains support for the POC with VDSM and Quantum.

Currently supports OVS and Linux Bridge

In the existing VDSM code replace/merge libvirtvm.py - this contains the hooking to the quantum support
The file quantum.py contains the POC for the openvswitch and linuxbridge plugins

