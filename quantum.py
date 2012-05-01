#
# Copyright 2009-2011 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# Refer to the README and COPYING files for full details of the license
#

from vdsm import utils

class Quantum(object):
    def __init__(self, log, plugin, network_id, port_id, attach_id):
        self.log = log
        self.plugin = plugin
        self.q_network_id = network_id
        self.q_port_id = port_id
        self.q_attachment_id = attach_id
        self.deviceName = "tap" + self.q_attachment_id[0:11]
        self.log = log
        self.log.debug("Quantum : %s : %s/%s/%s", self.plugin, self.q_network_id,
                       self.q_port_id, self.q_attachment_id)
        if plugin == 'LinuxBridge':
            self.vifAdd = self.vifAddLinuxBridge
            self.vifDelete = self.vifDeleteLinuxBridge
        elif plugin == 'openvswitch':
            self.vifAdd = self.vifAddOpenVswitch
            self.vifDelete = self.vifDeleteOpenVswitch
        else:
            self.log.error("Quantum: Invalid plugin %s", self.plugin)

    def vifAdd(self, vmUuid, maddAddr):
        self.log.error("Quantum: Invalid plugin %s", self.plugin)

    def vifDelete(self):
        self.log.error("Quantum: Invalid plugin %s", self.plugin)

    def vifDeviceName(self):
        return self.deviceName

    def vifAddOpenVswitch(self, vmUuid, macAddr):
        command = ["/sbin/ip", "tuntap", "add", self.deviceName, "mode", "tap"]
        utils.execCmd(command, sudo=True)
        command = ["/sbin/ip", "link", "set", self.deviceName, "up"]
        utils.execCmd(command, sudo=True)
        command = ["/usr/bin/ovs-vsctl", "--", "--may-exist", "add-port", "br-int", self.deviceName,
                   "--", "set", "Interface", self.deviceName, "external-ids:iface-id=%s" % self.q_attachment_id,
                   "--", "set", "Interface", self.deviceName, "external-ids:iface-status=active",
                   "--", "set", "Interface", self.deviceName, "external-ids:attached-mac=%s" % macAddr,
                   "--", "set", "Interface", self.deviceName, "external-ids:vm-uuid=%s" % vmUuid]
        utils.execCmd(command, sudo=True)

    def vifDeleteOpenVswitch(self):
        command = ["/usr/bin/ovs-vsctl", "del-port", "br-int", self.deviceName]
        utils.execCmd(command, sudo=True)
        command = ["/sbin/ip", "link", "delete", self.deviceName]
        utils.execCmd(command, sudo=True)

    def vifAddLinuxBridge(self, vmUuid, macAddr):
        command = ["/sbin/ip", "tuntap", "add", self.deviceName, "mode", "tap"]
        utils.execCmd(command, sudo=True)
        command = ["/sbin/ip", "link", "set", self.deviceName, "up"]
        utils.execCmd(command, sudo=True)

    def vifDeleteLinuxBridge(self):
        command = ["/sbin/ip", "link", "delete", self.deviceName]
        utils.execCmd(command, sudo=True)
