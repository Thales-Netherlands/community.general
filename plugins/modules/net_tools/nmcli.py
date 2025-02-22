#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2015, Chris Long <alcamie@gmail.com> <chlong@redhat.com>
# Copyright: (c) 2017, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: nmcli
author:
- Chris Long (@alcamie101)
short_description: Manage Networking
requirements:
- nmcli
description:
    - 'Manage the network devices. Create, modify and manage various connection and device type e.g., ethernet, teams, bonds, vlans etc.'
    - 'On CentOS 8 and Fedora >=29 like systems, the requirements can be met by installing the following packages: NetworkManager.'
    - 'On CentOS 7 and Fedora <=28 like systems, the requirements can be met by installing the following packages: NetworkManager-tui.'
    - 'On Ubuntu and Debian like systems, the requirements can be met by installing the following packages: network-manager'
    - 'On openSUSE, the requirements can be met by installing the following packages: NetworkManager.'
options:
    state:
        description:
            - Whether the device should exist or not, taking action if the state is different from what is stated.
        type: str
        required: true
        choices: [ absent, present ]
    autoconnect:
        description:
            - Whether the connection should start on boot.
            - Whether the connection profile can be automatically activated
        type: bool
        default: yes
    conn_name:
        description:
            - The name used to call the connection. Pattern is <type>[-<ifname>][-<num>].
        type: str
        required: true
    ifname:
        description:
            - The interface to bind the connection to.
            - The connection will only be applicable to this interface name.
            - A special value of C('*') can be used for interface-independent connections.
            - The ifname argument is mandatory for all connection types except bond, team, bridge and vlan.
            - This parameter defaults to C(conn_name) when left unset.
        type: str
    type:
        description:
            - This is the type of device or network connection that you wish to create or modify.
            - Type C(dummy) is added in community.general 3.5.0.
            - Type C(generic) is added in Ansible 2.5.
            - Type C(infiniband) is added in community.general 2.0.0.
        type: str
        choices: [ bond, bond-slave, bridge, bridge-slave, dummy, ethernet, generic, infiniband, ipip, sit, team, team-slave, vlan, vxlan, wifi ]
    mode:
        description:
            - This is the type of device or network connection that you wish to create for a bond or bridge.
        type: str
        choices: [ 802.3ad, active-backup, balance-alb, balance-rr, balance-tlb, balance-xor, broadcast ]
        default: balance-rr
    master:
        description:
            - Master <master (ifname, or connection UUID or conn_name) of bridge, team, bond master connection profile.
        type: str
    ip4:
        description:
            - The IPv4 address to this interface.
            - Use the format C(192.0.2.24/24).
            - If defined and I(method4) is not specified, automatically set C(ipv4.method) to C(manual).
        type: str
    gw4:
        description:
            - The IPv4 gateway for this interface.
            - Use the format C(192.0.2.1).
            - This parameter is mutually_exclusive with never_default4 parameter.
        type: str
    gw4_ignore_auto:
        description:
            - Ignore automatically configured IPv4 routes.
        type: bool
        default: false
        version_added: 3.2.0
    routes4:
        description:
            - The list of ipv4 routes.
            - Use the format '192.0.3.0/24 192.0.2.1'
        type: list
        elements: str
        version_added: 2.0.0
    route_metric4:
        description:
            - Set metric level of ipv4 routes configured on interface.
        type: int
        version_added: 2.0.0
    routing_rules4:
        description:
            - Is the same as in an C(ip route add) command, except always requires specifying a priority.
        type: str
        version_added: 3.3.0
    never_default4:
        description:
            - Set as default route.
            - This parameter is mutually_exclusive with gw4 parameter.
        type: bool
        default: no
        version_added: 2.0.0
    dns4:
        description:
            - A list of up to 3 dns servers.
            - IPv4 format e.g. to add two IPv4 DNS server addresses, use C(192.0.2.53 198.51.100.53).
        elements: str
        type: list
    dns4_search:
        description:
            - A list of DNS search domains.
        elements: str
        type: list
    dns4_ignore_auto:
        description:
            - Ignore automatically configured IPv4 name servers.
        type: bool
        default: false
        version_added: 3.2.0
    method4:
        description:
            - Configuration method to be used for IPv4.
            - If I(ip4) is set, C(ipv4.method) is automatically set to C(manual) and this parameter is not needed.
        type: str
        choices: [auto, link-local, manual, shared, disabled]
        version_added: 2.2.0
    may_fail4:
        description:
            - If you need I(ip4) configured before C(network-online.target) is reached, set this option to C(false).
        type: bool
        default: true
        version_added: 3.3.0
    ip6:
        description:
            - The IPv6 address to this interface.
            - Use the format C(abbe::cafe).
            - If defined and I(method6) is not specified, automatically set C(ipv6.method) to C(manual).
        type: str
    gw6:
        description:
            - The IPv6 gateway for this interface.
            - Use the format C(2001:db8::1).
        type: str
    gw6_ignore_auto:
        description:
            - Ignore automatically configured IPv6 routes.
        type: bool
        default: false
        version_added: 3.2.0
    dns6:
        description:
            - A list of up to 3 dns servers.
            - IPv6 format e.g. to add two IPv6 DNS server addresses, use C(2001:4860:4860::8888 2001:4860:4860::8844).
        elements: str
        type: list
    dns6_search:
        description:
            - A list of DNS search domains.
        elements: str
        type: list
    dns6_ignore_auto:
        description:
            - Ignore automatically configured IPv6 name servers.
        type: bool
        default: false
        version_added: 3.2.0
    method6:
        description:
            - Configuration method to be used for IPv6
            - If I(ip6) is set, C(ipv6.method) is automatically set to C(manual) and this parameter is not needed.
            - C(disabled) was added in community.general 3.3.0.
        type: str
        choices: [ignore, auto, dhcp, link-local, manual, shared, disabled]
        version_added: 2.2.0
    mtu:
        description:
            - The connection MTU, e.g. 9000. This can't be applied when creating the interface and is done once the interface has been created.
            - Can be used when modifying Team, VLAN, Ethernet (Future plans to implement wifi, pppoe, infiniband)
            - This parameter defaults to C(1500) when unset.
        type: int
    dhcp_client_id:
        description:
            - DHCP Client Identifier sent to the DHCP server.
        type: str
    primary:
        description:
            - This is only used with bond and is the primary interface name (for "active-backup" mode), this is the usually the 'ifname'.
        type: str
    miimon:
        description:
            - This is only used with bond - miimon.
            - This parameter defaults to C(100) when unset.
        type: int
    downdelay:
        description:
            - This is only used with bond - downdelay.
        type: int
    updelay:
        description:
            - This is only used with bond - updelay.
        type: int
    arp_interval:
        description:
            - This is only used with bond - ARP interval.
        type: int
    arp_ip_target:
        description:
            - This is only used with bond - ARP IP target.
        type: str
    stp:
        description:
            - This is only used with bridge and controls whether Spanning Tree Protocol (STP) is enabled for this bridge.
        type: bool
        default: yes
    priority:
        description:
            - This is only used with 'bridge' - sets STP priority.
        type: int
        default: 128
    forwarddelay:
        description:
            - This is only used with bridge - [forward-delay <2-30>] STP forwarding delay, in seconds.
        type: int
        default: 15
    hellotime:
        description:
            - This is only used with bridge - [hello-time <1-10>] STP hello time, in seconds.
        type: int
        default: 2
    maxage:
        description:
            - This is only used with bridge - [max-age <6-42>] STP maximum message age, in seconds.
        type: int
        default: 20
    ageingtime:
        description:
            - This is only used with bridge - [ageing-time <0-1000000>] the Ethernet MAC address aging time, in seconds.
        type: int
        default: 300
    mac:
        description:
            - MAC address of the connection.
            - Note this requires a recent kernel feature, originally introduced in 3.15 upstream kernel.
        type: str
    slavepriority:
        description:
            - This is only used with 'bridge-slave' - [<0-63>] - STP priority of this slave.
        type: int
        default: 32
    path_cost:
        description:
            - This is only used with 'bridge-slave' - [<1-65535>] - STP port cost for destinations via this slave.
        type: int
        default: 100
    hairpin:
        description:
            - This is only used with 'bridge-slave' - 'hairpin mode' for the slave, which allows frames to be sent back out through the slave the
              frame was received on.
        type: bool
        default: yes
    runner:
        description:
            - This is the type of device or network connection that you wish to create for a team.
        type: str
        choices: [ broadcast, roundrobin, activebackup, loadbalance, lacp ]
        default: roundrobin
        version_added: 3.4.0
    runner_hwaddr_policy:
        description:
            - This defines the policy of how hardware addresses of team device and port devices
              should be set during the team lifetime.
        type: str
        choices: [ same_all, by_active, only_active ]
        version_added: 3.4.0
    vlanid:
        description:
            - This is only used with VLAN - VLAN ID in range <0-4095>.
        type: int
    vlandev:
        description:
            - This is only used with VLAN - parent device this VLAN is on, can use ifname.
        type: str
    flags:
        description:
            - This is only used with VLAN - flags.
        type: str
    ingress:
        description:
            - This is only used with VLAN - VLAN ingress priority mapping.
        type: str
    egress:
        description:
            - This is only used with VLAN - VLAN egress priority mapping.
        type: str
    vxlan_id:
        description:
            - This is only used with VXLAN - VXLAN ID.
        type: int
    vxlan_remote:
       description:
            - This is only used with VXLAN - VXLAN destination IP address.
       type: str
    vxlan_local:
       description:
            - This is only used with VXLAN - VXLAN local IP address.
       type: str
    ip_tunnel_dev:
        description:
            - This is used with IPIP/SIT - parent device this IPIP/SIT tunnel, can use ifname.
        type: str
    ip_tunnel_remote:
       description:
            - This is used with IPIP/SIT - IPIP/SIT destination IP address.
       type: str
    ip_tunnel_local:
       description:
            - This is used with IPIP/SIT - IPIP/SIT local IP address.
       type: str
    zone:
       description:
            - The trust level of the connection.
            - When updating this property on a currently activated connection, the change takes effect immediately.
       type: str
       version_added: 2.0.0
    wifi_sec:
       description:
            - 'The security configuration of the WiFi connection. The valid attributes are listed on:
              U(https://networkmanager.dev/docs/api/latest/settings-802-11-wireless-security.html).'
            - 'For instance to use common WPA-PSK auth with a password:
              C({key-mgmt: wpa-psk, psk: my_password}).'
       type: dict
       version_added: 3.0.0
    ssid:
       description:
            - Name of the Wireless router or the access point.
       type: str
       version_added: 3.0.0
    wifi:
       description:
            - 'The configuration of the WiFi connection. The valid attributes are listed on:
              U(https://networkmanager.dev/docs/api/latest/settings-802-11-wireless.html).'
            - 'For instance to create a hidden AP mode WiFi connection:
              C({hidden: true, mode: ap}).'
       type: dict
       version_added: 3.5.0
'''

EXAMPLES = r'''
# These examples are using the following inventory:
#
# ## Directory layout:
#
# |_/inventory/cloud-hosts
# |           /group_vars/openstack-stage.yml
# |           /host_vars/controller-01.openstack.host.com
# |           /host_vars/controller-02.openstack.host.com
# |_/playbook/library/nmcli.py
# |          /playbook-add.yml
# |          /playbook-del.yml
# ```
#
# ## inventory examples
# ### groups_vars
# ```yml
# ---
# #devops_os_define_network
# storage_gw: "192.0.2.254"
# external_gw: "198.51.100.254"
# tenant_gw: "203.0.113.254"
#
# #Team vars
# nmcli_team:
#   - conn_name: tenant
#     ip4: '{{ tenant_ip }}'
#     gw4: '{{ tenant_gw }}'
#   - conn_name: external
#     ip4: '{{ external_ip }}'
#     gw4: '{{ external_gw }}'
#   - conn_name: storage
#     ip4: '{{ storage_ip }}'
#     gw4: '{{ storage_gw }}'
# nmcli_team_slave:
#   - conn_name: em1
#     ifname: em1
#     master: tenant
#   - conn_name: em2
#     ifname: em2
#     master: tenant
#   - conn_name: p2p1
#     ifname: p2p1
#     master: storage
#   - conn_name: p2p2
#     ifname: p2p2
#     master: external
#
# #bond vars
# nmcli_bond:
#   - conn_name: tenant
#     ip4: '{{ tenant_ip }}'
#     gw4: ''
#     mode: balance-rr
#   - conn_name: external
#     ip4: '{{ external_ip }}'
#     gw4: ''
#     mode: balance-rr
#   - conn_name: storage
#     ip4: '{{ storage_ip }}'
#     gw4: '{{ storage_gw }}'
#     mode: balance-rr
# nmcli_bond_slave:
#   - conn_name: em1
#     ifname: em1
#     master: tenant
#   - conn_name: em2
#     ifname: em2
#     master: tenant
#   - conn_name: p2p1
#     ifname: p2p1
#     master: storage
#   - conn_name: p2p2
#     ifname: p2p2
#     master: external
#
# #ethernet vars
# nmcli_ethernet:
#   - conn_name: em1
#     ifname: em1
#     ip4: '{{ tenant_ip }}'
#     gw4: '{{ tenant_gw }}'
#   - conn_name: em2
#     ifname: em2
#     ip4: '{{ tenant_ip1 }}'
#     gw4: '{{ tenant_gw }}'
#   - conn_name: p2p1
#     ifname: p2p1
#     ip4: '{{ storage_ip }}'
#     gw4: '{{ storage_gw }}'
#   - conn_name: p2p2
#     ifname: p2p2
#     ip4: '{{ external_ip }}'
#     gw4: '{{ external_gw }}'
# ```
#
# ### host_vars
# ```yml
# ---
# storage_ip: "192.0.2.91/23"
# external_ip: "198.51.100.23/21"
# tenant_ip: "203.0.113.77/23"
# ```



## playbook-add.yml example

---
- hosts: openstack-stage
  remote_user: root
  tasks:

  - name: Install needed network manager libs
    ansible.builtin.package:
      name:
        - NetworkManager-libnm
        - nm-connection-editor
        - libsemanage-python
        - policycoreutils-python
      state: present

##### Working with all cloud nodes - Teaming
  - name: Try nmcli add team - conn_name only & ip4 gw4
    community.general.nmcli:
      type: team
      conn_name: '{{ item.conn_name }}'
      ip4: '{{ item.ip4 }}'
      gw4: '{{ item.gw4 }}'
      state: present
    with_items:
      - '{{ nmcli_team }}'

  - name: Try nmcli add teams-slave
    community.general.nmcli:
      type: team-slave
      conn_name: '{{ item.conn_name }}'
      ifname: '{{ item.ifname }}'
      master: '{{ item.master }}'
      state: present
    with_items:
      - '{{ nmcli_team_slave }}'

###### Working with all cloud nodes - Bonding
  - name: Try nmcli add bond - conn_name only & ip4 gw4 mode
    community.general.nmcli:
      type: bond
      conn_name: '{{ item.conn_name }}'
      ip4: '{{ item.ip4 }}'
      gw4: '{{ item.gw4 }}'
      mode: '{{ item.mode }}'
      state: present
    with_items:
      - '{{ nmcli_bond }}'

  - name: Try nmcli add bond-slave
    community.general.nmcli:
      type: bond-slave
      conn_name: '{{ item.conn_name }}'
      ifname: '{{ item.ifname }}'
      master: '{{ item.master }}'
      state: present
    with_items:
      - '{{ nmcli_bond_slave }}'

##### Working with all cloud nodes - Ethernet
  - name: Try nmcli add Ethernet - conn_name only & ip4 gw4
    community.general.nmcli:
      type: ethernet
      conn_name: '{{ item.conn_name }}'
      ip4: '{{ item.ip4 }}'
      gw4: '{{ item.gw4 }}'
      state: present
    with_items:
      - '{{ nmcli_ethernet }}'

## playbook-del.yml example
- hosts: openstack-stage
  remote_user: root
  tasks:

  - name: Try nmcli del team - multiple
    community.general.nmcli:
      conn_name: '{{ item.conn_name }}'
      state: absent
    with_items:
      - conn_name: em1
      - conn_name: em2
      - conn_name: p1p1
      - conn_name: p1p2
      - conn_name: p2p1
      - conn_name: p2p2
      - conn_name: tenant
      - conn_name: storage
      - conn_name: external
      - conn_name: team-em1
      - conn_name: team-em2
      - conn_name: team-p1p1
      - conn_name: team-p1p2
      - conn_name: team-p2p1
      - conn_name: team-p2p2

  - name: Add an Ethernet connection with static IP configuration
    community.general.nmcli:
      conn_name: my-eth1
      ifname: eth1
      type: ethernet
      ip4: 192.0.2.100/24
      gw4: 192.0.2.1
      state: present

  - name: Add an Team connection with static IP configuration
    community.general.nmcli:
      conn_name: my-team1
      ifname: my-team1
      type: team
      ip4: 192.0.2.100/24
      gw4: 192.0.2.1
      state: present
      autoconnect: yes

  - name: Optionally, at the same time specify IPv6 addresses for the device
    community.general.nmcli:
      conn_name: my-eth1
      ifname: eth1
      type: ethernet
      ip4: 192.0.2.100/24
      gw4: 192.0.2.1
      ip6: 2001:db8::cafe
      gw6: 2001:db8::1
      state: present

  - name: Add two IPv4 DNS server addresses
    community.general.nmcli:
      conn_name: my-eth1
      type: ethernet
      dns4:
      - 192.0.2.53
      - 198.51.100.53
      state: present

  - name: Make a profile usable for all compatible Ethernet interfaces
    community.general.nmcli:
      ctype: ethernet
      name: my-eth1
      ifname: '*'
      state: present

  - name: Change the property of a setting e.g. MTU
    community.general.nmcli:
      conn_name: my-eth1
      mtu: 9000
      type: ethernet
      state: present

  - name: Add VxLan
    community.general.nmcli:
      type: vxlan
      conn_name: vxlan_test1
      vxlan_id: 16
      vxlan_local: 192.168.1.2
      vxlan_remote: 192.168.1.5

  - name: Add ipip
    community.general.nmcli:
      type: ipip
      conn_name: ipip_test1
      ip_tunnel_dev: eth0
      ip_tunnel_local: 192.168.1.2
      ip_tunnel_remote: 192.168.1.5

  - name: Add sit
    community.general.nmcli:
      type: sit
      conn_name: sit_test1
      ip_tunnel_dev: eth0
      ip_tunnel_local: 192.168.1.2
      ip_tunnel_remote: 192.168.1.5

  - name: Add zone
    community.general.nmcli:
      type: ethernet
      conn_name: my-eth1
      zone: external
      state: present

# nmcli exits with status 0 if it succeeds and exits with a status greater
# than zero when there is a failure. The following list of status codes may be
# returned:
#
#     - 0 Success - indicates the operation succeeded
#     - 1 Unknown or unspecified error
#     - 2 Invalid user input, wrong nmcli invocation
#     - 3 Timeout expired (see --wait option)
#     - 4 Connection activation failed
#     - 5 Connection deactivation failed
#     - 6 Disconnecting device failed
#     - 7 Connection deletion failed
#     - 8 NetworkManager is not running
#     - 9 nmcli and NetworkManager versions mismatch
#     - 10 Connection, device, or access point does not exist.

- name: Create the wifi connection
  community.general.nmcli:
    type: wifi
    conn_name: Brittany
    ifname: wlp4s0
    ssid: Brittany
    wifi_sec:
      key-mgmt: wpa-psk
      psk: my_password
    autoconnect: true
    state: present

- name: Create a hidden AP mode wifi connection
  community.general.nmcli:
    type: wifi
    conn_name: ChocoMaster
    ifname: wlo1
    ssid: ChocoMaster
    wifi:
      hidden: true
      mode: ap
    autoconnect: true
    state: present

'''

RETURN = r"""#
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
import re


class NmcliModuleError(Exception):
    pass


class Nmcli(object):
    """
    This is the generic nmcli manipulation class that is subclassed based on platform.
    A subclass may wish to override the following action methods:-
            - create_connection()
            - delete_connection()
            - modify_connection()
            - show_connection()
            - up_connection()
            - down_connection()
    All subclasses MUST define platform and distribution (which may be None).
    """

    platform = 'Generic'
    distribution = None

    def __init__(self, module):
        self.module = module
        self.state = module.params['state']
        self.autoconnect = module.params['autoconnect']
        self.conn_name = module.params['conn_name']
        self.master = module.params['master']
        self.ifname = module.params['ifname']
        self.type = module.params['type']
        self.ip4 = module.params['ip4']
        self.gw4 = module.params['gw4']
        self.gw4_ignore_auto = module.params['gw4_ignore_auto']
        self.routes4 = module.params['routes4']
        self.route_metric4 = module.params['route_metric4']
        self.routing_rules4 = module.params['routing_rules4']
        self.never_default4 = module.params['never_default4']
        self.dns4 = module.params['dns4']
        self.dns4_search = module.params['dns4_search']
        self.dns4_ignore_auto = module.params['dns4_ignore_auto']
        self.method4 = module.params['method4']
        self.may_fail4 = module.params['may_fail4']
        self.ip6 = module.params['ip6']
        self.gw6 = module.params['gw6']
        self.gw6_ignore_auto = module.params['gw6_ignore_auto']
        self.dns6 = module.params['dns6']
        self.dns6_search = module.params['dns6_search']
        self.dns6_ignore_auto = module.params['dns6_ignore_auto']
        self.method6 = module.params['method6']
        self.mtu = module.params['mtu']
        self.stp = module.params['stp']
        self.priority = module.params['priority']
        self.mode = module.params['mode']
        self.miimon = module.params['miimon']
        self.primary = module.params['primary']
        self.downdelay = module.params['downdelay']
        self.updelay = module.params['updelay']
        self.arp_interval = module.params['arp_interval']
        self.arp_ip_target = module.params['arp_ip_target']
        self.slavepriority = module.params['slavepriority']
        self.forwarddelay = module.params['forwarddelay']
        self.hellotime = module.params['hellotime']
        self.maxage = module.params['maxage']
        self.ageingtime = module.params['ageingtime']
        self.hairpin = module.params['hairpin']
        self.path_cost = module.params['path_cost']
        self.mac = module.params['mac']
        self.runner = module.params['runner']
        self.runner_hwaddr_policy = module.params['runner_hwaddr_policy']
        self.vlanid = module.params['vlanid']
        self.vlandev = module.params['vlandev']
        self.flags = module.params['flags']
        self.ingress = module.params['ingress']
        self.egress = module.params['egress']
        self.vxlan_id = module.params['vxlan_id']
        self.vxlan_local = module.params['vxlan_local']
        self.vxlan_remote = module.params['vxlan_remote']
        self.ip_tunnel_dev = module.params['ip_tunnel_dev']
        self.ip_tunnel_local = module.params['ip_tunnel_local']
        self.ip_tunnel_remote = module.params['ip_tunnel_remote']
        self.nmcli_bin = self.module.get_bin_path('nmcli', True)
        self.dhcp_client_id = module.params['dhcp_client_id']
        self.zone = module.params['zone']
        self.ssid = module.params['ssid']
        self.wifi = module.params['wifi']
        self.wifi_sec = module.params['wifi_sec']

        if self.method4:
            self.ipv4_method = self.method4
        elif self.type == 'dummy' and not self.ip4:
            self.ipv4_method = 'disabled'
        elif self.ip4:
            self.ipv4_method = 'manual'
        else:
            self.ipv4_method = None

        if self.method6:
            self.ipv6_method = self.method6
        elif self.type == 'dummy' and not self.ip6:
            self.ipv6_method = 'disabled'
        elif self.ip6:
            self.ipv6_method = 'manual'
        else:
            self.ipv6_method = None

    def execute_command(self, cmd, use_unsafe_shell=False, data=None):
        if isinstance(cmd, list):
            cmd = [to_text(item) for item in cmd]
        else:
            cmd = to_text(cmd)
        return self.module.run_command(cmd, use_unsafe_shell=use_unsafe_shell, data=data)

    def connection_options(self, detect_change=False):
        # Options common to multiple connection types.
        options = {
            'connection.autoconnect': self.autoconnect,
            'connection.zone': self.zone,
        }

        # IP address options.
        if self.ip_conn_type and not self.master:
            options.update({
                'ipv4.addresses': self.ip4,
                'ipv4.dhcp-client-id': self.dhcp_client_id,
                'ipv4.dns': self.dns4,
                'ipv4.dns-search': self.dns4_search,
                'ipv4.ignore-auto-dns': self.dns4_ignore_auto,
                'ipv4.gateway': self.gw4,
                'ipv4.ignore-auto-routes': self.gw4_ignore_auto,
                'ipv4.routes': self.routes4,
                'ipv4.route-metric': self.route_metric4,
                'ipv4.routing-rules': self.routing_rules4,
                'ipv4.never-default': self.never_default4,
                'ipv4.method': self.ipv4_method,
                'ipv4.may-fail': self.may_fail4,
                'ipv6.addresses': self.ip6,
                'ipv6.dns': self.dns6,
                'ipv6.dns-search': self.dns6_search,
                'ipv6.ignore-auto-dns': self.dns6_ignore_auto,
                'ipv6.gateway': self.gw6,
                'ipv6.ignore-auto-routes': self.gw6_ignore_auto,
                'ipv6.method': self.ipv6_method,
            })

        # Layer 2 options.
        if self.mac:
            options.update({self.mac_setting: self.mac})

        if self.mtu_conn_type:
            options.update({self.mtu_setting: self.mtu})

        # Connections that can have a master.
        if self.slave_conn_type:
            options.update({
                'connection.master': self.master,
            })

        # Options specific to a connection type.
        if self.type == 'bond':
            options.update({
                'arp-interval': self.arp_interval,
                'arp-ip-target': self.arp_ip_target,
                'downdelay': self.downdelay,
                'miimon': self.miimon,
                'mode': self.mode,
                'primary': self.primary,
                'updelay': self.updelay,
            })
        elif self.type == 'bond-slave':
            options.update({
                'connection.slave-type': 'bond',
            })
        elif self.type == 'bridge':
            options.update({
                'bridge.ageing-time': self.ageingtime,
                'bridge.forward-delay': self.forwarddelay,
                'bridge.hello-time': self.hellotime,
                'bridge.max-age': self.maxage,
                'bridge.priority': self.priority,
                'bridge.stp': self.stp,
            })
        elif self.type == 'team':
            options.update({
                'team.runner': self.runner,
                'team.runner-hwaddr-policy': self.runner_hwaddr_policy,
            })
        elif self.type == 'bridge-slave':
            options.update({
                'connection.slave-type': 'bridge',
                'bridge-port.path-cost': self.path_cost,
                'bridge-port.hairpin-mode': self.hairpin,
                'bridge-port.priority': self.slavepriority,
            })
        elif self.type == 'team-slave':
            options.update({
                'connection.slave-type': 'team',
            })
        elif self.tunnel_conn_type:
            options.update({
                'ip-tunnel.local': self.ip_tunnel_local,
                'ip-tunnel.mode': self.type,
                'ip-tunnel.parent': self.ip_tunnel_dev,
                'ip-tunnel.remote': self.ip_tunnel_remote,
            })
        elif self.type == 'vlan':
            options.update({
                'vlan.id': self.vlanid,
                'vlan.parent': self.vlandev,
            })
        elif self.type == 'vxlan':
            options.update({
                'vxlan.id': self.vxlan_id,
                'vxlan.local': self.vxlan_local,
                'vxlan.remote': self.vxlan_remote,
            })
        elif self.type == 'wifi':
            options.update({
                '802-11-wireless.ssid': self.ssid,
                'connection.slave-type': 'bond' if self.master else None,
            })
            if self.wifi:
                for name, value in self.wifi.items():
                    # Disregard 'ssid' via 'wifi.ssid'
                    if name == 'ssid':
                        continue
                    options.update({
                        '802-11-wireless.%s' % name: value
                    })
            if self.wifi_sec:
                for name, value in self.wifi_sec.items():
                    options.update({
                        '802-11-wireless-security.%s' % name: value
                    })
        # Convert settings values based on the situation.
        for setting, value in options.items():
            setting_type = self.settings_type(setting)
            convert_func = None
            if setting_type is bool:
                # Convert all bool options to yes/no.
                convert_func = self.bool_to_string
            if detect_change:
                if setting in ('vlan.id', 'vxlan.id'):
                    # Convert VLAN/VXLAN IDs to text when detecting changes.
                    convert_func = to_text
                elif setting == self.mtu_setting:
                    # MTU is 'auto' by default when detecting changes.
                    convert_func = self.mtu_to_string
            elif setting_type is list:
                # Convert lists to strings for nmcli create/modify commands.
                convert_func = self.list_to_string

            if callable(convert_func):
                options[setting] = convert_func(options[setting])

        return options

    @property
    def ip_conn_type(self):
        return self.type in (
            'bond',
            'bridge',
            'dummy',
            'ethernet',
            'generic',
            'infiniband',
            'team',
            'vlan',
            'wifi'
        )

    @property
    def mac_setting(self):
        if self.type == 'bridge':
            return 'bridge.mac-address'
        else:
            return '802-3-ethernet.cloned-mac-address'

    @property
    def mtu_conn_type(self):
        return self.type in (
            'dummy',
            'ethernet',
            'team-slave',
        )

    @property
    def mtu_setting(self):
        return '802-3-ethernet.mtu'

    @staticmethod
    def mtu_to_string(mtu):
        if not mtu:
            return 'auto'
        else:
            return to_text(mtu)

    @property
    def slave_conn_type(self):
        return self.type in (
            'bond-slave',
            'bridge-slave',
            'team-slave',
            'wifi',
        )

    @property
    def tunnel_conn_type(self):
        return self.type in (
            'ipip',
            'sit',
        )

    @staticmethod
    def bool_to_string(boolean):
        if boolean:
            return "yes"
        else:
            return "no"

    @staticmethod
    def list_to_string(lst):
        return ",".join(lst or [""])

    @staticmethod
    def settings_type(setting):
        if setting in ('bridge.stp',
                       'bridge-port.hairpin-mode',
                       'connection.autoconnect',
                       'ipv4.never-default',
                       'ipv4.ignore-auto-dns',
                       'ipv4.ignore-auto-routes',
                       'ipv4.may-fail',
                       'ipv6.ignore-auto-dns',
                       'ipv6.ignore-auto-routes',
                       '802-11-wireless.hidden'):
            return bool
        elif setting in ('ipv4.dns',
                         'ipv4.dns-search',
                         'ipv4.routes',
                         'ipv4.route-metric'
                         'ipv6.dns',
                         'ipv6.dns-search'):
            return list
        return str

    def list_connection_info(self):
        cmd = [self.nmcli_bin, '--fields', 'name', '--terse', 'con', 'show']
        (rc, out, err) = self.execute_command(cmd)
        if rc != 0:
            raise NmcliModuleError(err)
        return out.splitlines()

    def connection_exists(self):
        return self.conn_name in self.list_connection_info()

    def down_connection(self):
        cmd = [self.nmcli_bin, 'con', 'down', self.conn_name]
        return self.execute_command(cmd)

    def up_connection(self):
        cmd = [self.nmcli_bin, 'con', 'up', self.conn_name]
        return self.execute_command(cmd)

    def connection_update(self, nmcli_command):
        if nmcli_command == 'create':
            cmd = [self.nmcli_bin, 'con', 'add', 'type']
            if self.tunnel_conn_type:
                cmd.append('ip-tunnel')
            else:
                cmd.append(self.type)
            cmd.append('con-name')
        elif nmcli_command == 'modify':
            cmd = [self.nmcli_bin, 'con', 'modify']
        else:
            self.module.fail_json(msg="Invalid nmcli command.")
        cmd.append(self.conn_name)

        # Use connection name as default for interface name on creation.
        if nmcli_command == 'create' and self.ifname is None:
            ifname = self.conn_name
        else:
            ifname = self.ifname

        options = {
            'connection.interface-name': ifname,
        }

        options.update(self.connection_options())

        # Constructing the command.
        for key, value in options.items():
            if value is not None:
                cmd.extend([key, value])

        return self.execute_command(cmd)

    def create_connection(self):
        status = self.connection_update('create')
        if self.create_connection_up:
            status = self.up_connection()
        return status

    @property
    def create_connection_up(self):
        if self.type in ('bond', 'dummy', 'ethernet', 'infiniband', 'wifi'):
            if (self.mtu is not None) or (self.dns4 is not None) or (self.dns6 is not None):
                return True
        elif self.type == 'team':
            if (self.dns4 is not None) or (self.dns6 is not None):
                return True
        return False

    def remove_connection(self):
        # self.down_connection()
        cmd = [self.nmcli_bin, 'con', 'del', self.conn_name]
        return self.execute_command(cmd)

    def modify_connection(self):
        return self.connection_update('modify')

    def show_connection(self):
        cmd = [self.nmcli_bin, '--show-secrets', 'con', 'show', self.conn_name]

        (rc, out, err) = self.execute_command(cmd)

        if rc != 0:
            raise NmcliModuleError(err)

        p_enum_value = re.compile(r'^([-]?\d+) \((\w+)\)$')

        conn_info = dict()
        for line in out.splitlines():
            pair = line.split(':', 1)
            key = pair[0].strip()
            key_type = self.settings_type(key)
            if key and len(pair) > 1:
                raw_value = pair[1].lstrip()
                if raw_value == '--':
                    conn_info[key] = None
                elif key == 'bond.options':
                    # Aliases such as 'miimon', 'downdelay' are equivalent to the +bond.options 'option=value' syntax.
                    opts = raw_value.split(',')
                    for opt in opts:
                        alias_pair = opt.split('=', 1)
                        if len(alias_pair) > 1:
                            alias_key = alias_pair[0]
                            alias_value = alias_pair[1]
                            conn_info[alias_key] = alias_value
                elif key == 'ipv4.routes':
                    conn_info[key] = [s.strip() for s in raw_value.split(';')]
                elif key_type == list:
                    conn_info[key] = [s.strip() for s in raw_value.split(',')]
                else:
                    m_enum = p_enum_value.match(raw_value)
                    if m_enum is not None:
                        value = m_enum.group(1)
                    else:
                        value = raw_value
                    conn_info[key] = value

        return conn_info

    def _compare_conn_params(self, conn_info, options):
        changed = False
        diff_before = dict()
        diff_after = dict()

        for key, value in options.items():
            if not value:
                continue

            if key in conn_info:
                current_value = conn_info[key]
                if key == 'ipv4.routes' and current_value is not None:
                    # ipv4.routes do not have same options and show_connection() format
                    # options: ['10.11.0.0/24 10.10.0.2', '10.12.0.0/24 10.10.0.2 200']
                    # show_connection(): ['{ ip = 10.11.0.0/24, nh = 10.10.0.2 }', '{ ip = 10.12.0.0/24, nh = 10.10.0.2, mt = 200 }']
                    # Need to convert in order to compare both
                    current_value = [re.sub(r'^{\s*ip\s*=\s*([^, ]+),\s*nh\s*=\s*([^} ]+),\s*mt\s*=\s*([^} ]+)\s*}', r'\1 \2 \3',
                                     route) for route in current_value]
                    current_value = [re.sub(r'^{\s*ip\s*=\s*([^, ]+),\s*nh\s*=\s*([^} ]+)\s*}', r'\1 \2', route) for route in current_value]
                if key == self.mac_setting:
                    # MAC addresses are case insensitive, nmcli always reports them in uppercase
                    value = value.upper()
                    # ensure current_value is also converted to uppercase in case nmcli changes behaviour
                    current_value = current_value.upper()
            else:
                # parameter does not exist
                current_value = None

            if isinstance(current_value, list) and isinstance(value, list):
                # compare values between two lists
                if sorted(current_value) != sorted(value):
                    changed = True
            else:
                if current_value != to_text(value):
                    changed = True

            diff_before[key] = current_value
            diff_after[key] = value

        diff = {
            'before': diff_before,
            'after': diff_after,
        }
        return (changed, diff)

    def is_connection_changed(self):
        options = {
            'connection.interface-name': self.ifname,
        }
        options.update(self.connection_options(detect_change=True))
        return self._compare_conn_params(self.show_connection(), options)


def main():
    # Parsing argument file
    module = AnsibleModule(
        argument_spec=dict(
            autoconnect=dict(type='bool', default=True),
            state=dict(type='str', required=True, choices=['absent', 'present']),
            conn_name=dict(type='str', required=True),
            master=dict(type='str'),
            ifname=dict(type='str'),
            type=dict(type='str',
                      choices=[
                          'bond',
                          'bond-slave',
                          'bridge',
                          'bridge-slave',
                          'dummy',
                          'ethernet',
                          'generic',
                          'infiniband',
                          'ipip',
                          'sit',
                          'team',
                          'team-slave',
                          'vlan',
                          'vxlan',
                          'wifi',
                      ]),
            ip4=dict(type='str'),
            gw4=dict(type='str'),
            gw4_ignore_auto=dict(type='bool', default=False),
            routes4=dict(type='list', elements='str'),
            route_metric4=dict(type='int'),
            routing_rules4=dict(type='str'),
            never_default4=dict(type='bool', default=False),
            dns4=dict(type='list', elements='str'),
            dns4_search=dict(type='list', elements='str'),
            dns4_ignore_auto=dict(type='bool', default=False),
            method4=dict(type='str', choices=['auto', 'link-local', 'manual', 'shared', 'disabled']),
            may_fail4=dict(type='bool', default=True),
            dhcp_client_id=dict(type='str'),
            ip6=dict(type='str'),
            gw6=dict(type='str'),
            gw6_ignore_auto=dict(type='bool', default=False),
            dns6=dict(type='list', elements='str'),
            dns6_search=dict(type='list', elements='str'),
            dns6_ignore_auto=dict(type='bool', default=False),
            method6=dict(type='str', choices=['ignore', 'auto', 'dhcp', 'link-local', 'manual', 'shared', 'disabled']),
            # Bond Specific vars
            mode=dict(type='str', default='balance-rr',
                      choices=['802.3ad', 'active-backup', 'balance-alb', 'balance-rr', 'balance-tlb', 'balance-xor', 'broadcast']),
            miimon=dict(type='int'),
            downdelay=dict(type='int'),
            updelay=dict(type='int'),
            arp_interval=dict(type='int'),
            arp_ip_target=dict(type='str'),
            primary=dict(type='str'),
            # general usage
            mtu=dict(type='int'),
            mac=dict(type='str'),
            zone=dict(type='str'),
            # bridge specific vars
            stp=dict(type='bool', default=True),
            priority=dict(type='int', default=128),
            slavepriority=dict(type='int', default=32),
            forwarddelay=dict(type='int', default=15),
            hellotime=dict(type='int', default=2),
            maxage=dict(type='int', default=20),
            ageingtime=dict(type='int', default=300),
            hairpin=dict(type='bool', default=True),
            path_cost=dict(type='int', default=100),
            # team specific vars
            runner=dict(type='str', default='roundrobin',
                             choices=['broadcast', 'roundrobin', 'activebackup', 'loadbalance', 'lacp']),
            # team active-backup runner specific options
            runner_hwaddr_policy=dict(type='str', choices=['same_all', 'by_active', 'only_active']),
            # vlan specific vars
            vlanid=dict(type='int'),
            vlandev=dict(type='str'),
            flags=dict(type='str'),
            ingress=dict(type='str'),
            egress=dict(type='str'),
            # vxlan specific vars
            vxlan_id=dict(type='int'),
            vxlan_local=dict(type='str'),
            vxlan_remote=dict(type='str'),
            # ip-tunnel specific vars
            ip_tunnel_dev=dict(type='str'),
            ip_tunnel_local=dict(type='str'),
            ip_tunnel_remote=dict(type='str'),
            ssid=dict(type='str'),
            wifi=dict(type='dict'),
            wifi_sec=dict(type='dict', no_log=True),
        ),
        mutually_exclusive=[['never_default4', 'gw4']],
        required_if=[("type", "wifi", [("ssid")])],
        supports_check_mode=True,
    )
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')

    nmcli = Nmcli(module)

    (rc, out, err) = (None, '', '')
    result = {'conn_name': nmcli.conn_name, 'state': nmcli.state}

    # check for issues
    if nmcli.conn_name is None:
        nmcli.module.fail_json(msg="Please specify a name for the connection")
    # team checks
    if nmcli.type == "team":
        if nmcli.runner_hwaddr_policy and not nmcli.runner == "activebackup":
            nmcli.module.fail_json(msg="Runner-hwaddr-policy is only allowed for runner activebackup")
    # team-slave checks
    if nmcli.type == 'team-slave':
        if nmcli.master is None:
            nmcli.module.fail_json(msg="Please specify a name for the master when type is %s" % nmcli.type)
        if nmcli.ifname is None:
            nmcli.module.fail_json(msg="Please specify an interface name for the connection when type is %s" % nmcli.type)

    try:
        if nmcli.state == 'absent':
            if nmcli.connection_exists():
                if module.check_mode:
                    module.exit_json(changed=True)
                (rc, out, err) = nmcli.down_connection()
                (rc, out, err) = nmcli.remove_connection()
                if rc != 0:
                    module.fail_json(name=('No Connection named %s exists' % nmcli.conn_name), msg=err, rc=rc)

        elif nmcli.state == 'present':
            if nmcli.connection_exists():
                changed, diff = nmcli.is_connection_changed()
                if module._diff:
                    result['diff'] = diff

                if changed:
                    # modify connection (note: this function is check mode aware)
                    # result['Connection']=('Connection %s of Type %s is not being added' % (nmcli.conn_name, nmcli.type))
                    result['Exists'] = 'Connections do exist so we are modifying them'
                    if module.check_mode:
                        module.exit_json(changed=True, **result)
                    (rc, out, err) = nmcli.modify_connection()
                else:
                    result['Exists'] = 'Connections already exist and no changes made'
                    if module.check_mode:
                        module.exit_json(changed=False, **result)
            if not nmcli.connection_exists():
                result['Connection'] = ('Connection %s of Type %s is being added' % (nmcli.conn_name, nmcli.type))
                if module.check_mode:
                    module.exit_json(changed=True, **result)
                (rc, out, err) = nmcli.create_connection()
            if rc is not None and rc != 0:
                module.fail_json(name=nmcli.conn_name, msg=err, rc=rc)
    except NmcliModuleError as e:
        module.fail_json(name=nmcli.conn_name, msg=str(e))

    if rc is None:
        result['changed'] = False
    else:
        result['changed'] = True
    if out:
        result['stdout'] = out
    if err:
        result['stderr'] = err

    module.exit_json(**result)


if __name__ == '__main__':
    main()
