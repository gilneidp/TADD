# Copyright 2012-2013 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "madapp.settings")
from django.core.management import execute_from_command_line

from django.utils import timezone
from django.db.models import Count
from array import *
from django.db.models import F
from madapp import settings
from madapp.mad.models import *

from pox.core import core
import pox
log = core.getLogger()

from pox.lib.packet.ethernet import ethernet, ETHER_BROADCAST
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.tcp import tcp
from pox.lib.packet.arp import arp
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.util import str_to_bool, dpid_to_str
from pox.lib.recoco import Timer

import pox.openflow.libopenflow_01 as of

from pox.lib.revent import *

import time
from datetime import timedelta


# Timeout for flows
FLOW_IDLE_TIMEOUT = 1

# Timeout for ARP entries
ARP_TIMEOUT = 2 * 2

# Maximum number of packet to buffer on a switch for an unknown IP
MAX_BUFFERED_PER_IP = 5

# Maximum time to hang on to a buffer for an unknown IP in seconds
MAX_BUFFER_TIME = 5


class Entry (object):
  
  def __init__ (self, port, mac):
    self.timeout = time.time() + ARP_TIMEOUT
    self.port = port
    self.mac = mac

  def __eq__ (self, other):
    if type(other) == tuple:
      return (self.port,self.mac)==other
    else:
      return (self.port,self.mac)==(other.port,other.mac)
  def __ne__ (self, other):
    return not self.__eq__(other)

  def isExpired (self):
    if self.port == of.OFPP_NONE: return False
    return time.time() > self.timeout


def dpid_to_mac (dpid):
  return EthAddr("%012x" % (dpid & 0xffFFffFFffFF,))


class l3_switch (EventMixin):
  def __init__ (self, fakeways = [], arp_for_unknowns = False):
    # These are "fake gateways" -- we'll answer ARPs for them with MAC
    # of the switch they're connected to.
    self.fakeways = set(fakeways)

    # If this is true and we see a packet for an unknown
    # host, we'll ARP for it.
    self.arp_for_unknowns = arp_for_unknowns

    # (dpid,IP) -> expire_time
    # We use this to keep from spamming ARPs
    self.outstanding_arps = {}

    # (dpid,IP) -> [(expire_time,buffer_id,in_port), ...]
    # These are buffers we've gotten at this datapath for this IP which
    # we can't deliver because we don't know where they go.
    self.lost_buffers = {}

    # For each switch, we map IP addresses to Entries
    self.arpTable = {}

    # This timer handles expiring stuff
    self._expire_timer = Timer(5, self._handle_expiration, recurring=True)

    self.listenTo(core)

  def _handle_expiration (self):
    # Called by a timer so that we can remove old items.
    empty = []
    for k,v in self.lost_buffers.iteritems():
      dpid,ip = k

      for item in list(v):
        expires_at,buffer_id,in_port = item
        if expires_at < time.time():
          # This packet is old.  Tell this switch to drop it.
          v.remove(item)
          po = of.ofp_packet_out(buffer_id = buffer_id, in_port = in_port)
          core.openflow.sendToDPID(dpid, po)
	  print dpid, po
      if len(v) == 0: empty.append(k)

    # Remove empty buffer bins
    for k in empty:
      del self.lost_buffers[k]

  def _send_lost_buffers (self, dpid, ipaddr, macaddr, port):
    if (dpid,ipaddr) in self.lost_buffers:
      bucket = self.lost_buffers[(dpid,ipaddr)]
      del self.lost_buffers[(dpid,ipaddr)]
      log.info("Sending %i buffered packets to %s from %s and port %s"
                % (len(bucket),ipaddr,dpid_to_str(dpid), port))
      for _,buffer_id,in_port in bucket:
        po = of.ofp_packet_out(buffer_id=buffer_id,in_port=in_port)
        po.actions.append(of.ofp_action_dl_addr.set_dst(macaddr))
        po.actions.append(of.ofp_action_output(port = port))
        core.openflow.sendToDPID(dpid, po)
	print po

  def _handle_GoingUpEvent (self, event):
    self.listenTo(core.openflow)
    log.debug("Up...")

  def _handle_PacketIn (self, event):
    dpid = event.connection.dpid
    inport = event.port
    packet = event.parsed
    #know = packet.next.next.srcport
    if not packet.parsed:
      log.info("%i %i ignoring unparsed packet", dpid, inport, packet)
      return

    if dpid not in self.arpTable:
      # New switch -- create an empty table
      self.arpTable[dpid] = {}
      for fake in self.fakeways:
        self.arpTable[dpid][IPAddr(fake)] = Entry(of.OFPP_NONE,
         dpid_to_mac(dpid))

    if packet.type == ethernet.LLDP_TYPE:
      # Ignore LLDP packets
      return
    ## -- gilnei - Cap Flows
    if isinstance(packet.next.next,tcp):
      sport = packet.next.next.srcport
      dport = packet.next.next.dstport
      attack = 3
      prttype = 6
      counter1 = 0
      log.info ("AQUI DPID %i src_port %i dst_port %i" , dpid, sport, dport)
      switches = Switches.objects.get(name_switch = dpid)
      fl = TemporaryFlows(id_switch = switches, switchport = inport, ip_src = packet.next.srcip, ip_dst = packet.next.dstip, src_port = sport, dst_port = dport, timestamp = datetime.datetime.now())
      fl.save()
    # Verificar se e ataque 
      timeisnow=datetime.datetime.now() - timedelta(minutes=1)
      temps = TemporaryFlows.objects.values ('switchport','ip_src','ip_dst', 'dst_port').filter(timestamp__gte=timeisnow, dst_port__lte='10024').annotate(num_ports=Count('dst_port'))
      tempd = TemporaryFlows.objects.values ('switchport','ip_src','ip_dst', 'src_port').filter(timestamp__gte=timeisnow).annotate(num_ports=Count('src_port'))
      for flow in temps:
        counter1 = flow['num_ports']
      for flow in tempd:
        counter2 = flow['num_ports']
      portctr = TemporaryFlows.objects.values('switchport','ip_src','ip_dst').filter(timestamp__gte=timeisnow,
      					      dst_port__lte='10024').annotate(port_counter=Count('dst_port', distinct=True))
      for ct in portctr:
      	ctr = ct['port_counter']
      for flow in temps:
        counter1 = flow['num_ports']
      if (ctr > 10): 
      	attack = 1
	rt = RuleTable(id_switch=switches, switchport = 
		        inport, ip_src = packet.next.srcip,
		 	ip_dst = packet.next.dstip, src_port = sport,
		 	dst_port = dport, timestamp = datetime.datetime.now(), 
		        idle_timeout=3000, hard_timeout=20000,
		        action= 0) # porta 0 n existe = DROP
	rt.save()
      elif (counter1 > 120 and counter1 < 240): 
     	attack = 1
        rt = RuleTable(id_switch=switches, switchport = inport, 
        		ip_src = packet.next.srcip,
		        ip_dst = packet.next.dstip, 
		        src_port = sport, dst_port = dport,
		        timestamp = datetime.datetime.now(),
		        idle_timeout=3000, hard_timeout=20000, 
		        action= "DST_TO_HNP")
        rt.save()
      elif (counter1 > 240):
      	attack = 1
	rt = RuleTable(id_switch=switches, switchport = 
	                inport, ip_src = packet.next.srcip,
		 	ip_dst = packet.next.dstip, src_port = sport,
		 	dst_port = dport, timestamp = datetime.datetime.now(), 
		        idle_timeout=3000, hard_timeout=20000,
		        action= 0)
		 
        rt.save()
      else:
        attack = 0
       #else:
      if isinstance(packet.next, ipv4):
      		log.debug("%i %i IP %s => %s", dpid,inport,
                packet.next.srcip,packet.next.dstip)
      # Send any waiting packets...
      self._send_lost_buffers(dpid, packet.next.srcip, packet.src, inport)

      # Learn or update port/MAC info
      if packet.next.srcip in self.arpTable[dpid]:
        if self.arpTable[dpid][packet.next.srcip] != (inport, packet.src):
          log.debug("%i %i RE-learned %s", dpid,inport,packet.next.srcip)
      else:
        log.debug("%i %i learned %s", dpid,inport,str(packet.next.srcip))
      self.arpTable[dpid][packet.next.srcip] = Entry(inport, packet.src)
      
      # Try to forward
      dstaddr = packet.next.dstip
      srcaddr = packet.next.srcip

      if dstaddr in self.arpTable[dpid]:
        # We have info about what port to send it out on...
	prt = self.arpTable[dpid][dstaddr].port
        mac = self.arpTable[dpid][dstaddr].mac
        self.arpTable[dpid][packet.next.srcip] = Entry(inport, packet.src)

        if prt == inport:
	    log.debug("notsending")

        #  log.debug("%i %i not sending packet for %s back out of the " + 
                 #  "input port" % (dpid, inport, str(dstaddr)))
       #else:
        if (attack == 0):
          log.debug("%i %i installing flow for %s thisto %i  => %s out port %i"
                    % (dpid, inport, packet.next.srcip, packet.next.tos, dstaddr, prt))

          actions = []
          actions.append(of.ofp_action_dl_addr.set_dst(mac))
          actions.append(of.ofp_action_output(port = prt))
          match = of.ofp_match.from_packet(packet, inport)
          match.dl_src = None # Wildcard source MAC

          msg = of.ofp_flow_mod(command=of.OFPFC_ADD,
                                idle_timeout=FLOW_IDLE_TIMEOUT,
                                hard_timeout=of.OFP_FLOW_PERMANENT,
                                buffer_id=event.ofp.buffer_id,
                                actions=actions,
                                match=of.ofp_match.from_packet(packet,
                                                               inport))
          event.connection.send(msg.pack())

        if (attack == 1):
        # tmf = datetime.datetime.now() - timedelta(minutes= 2)
        # rules = RuleTable.objects.filter(timestamp__gte=tmf)
	# print ("Variaveis Filter %s %s %s %s"%(switches.__dict__,inport,packet.next.srcip,packet.next.dstip))
         rules = RuleTable.objects.all().filter(switchport = inport,ip_src = packet.next.srcip,ip_dst = packet.next.dstip, src_port = packet.next.next.srcport)
         #rules = RuleTable.objects.all().filter(id_switch=switches,switchPort=inport,ip_src=packet.next.srcip,ip_dst=packet.next.dstip)
        # rules = RuleTable.objects.all()

         for rule in rules:

            msg = of.ofp_flow_mod()
	    msg.match.dl_type = 0x800
            msg.match.nw_proto = prttype
            msg.match.nw_src = str(rule.ip_src)
            msg.match.nw_dst = str(rule.ip_dst)
            msg.priority = 65535 
       #     msg.match.tp_dst = int(rule.dst_port)
        #   msg.match.in_port = rule.switchport
            msg.idle_timeout = rule.idle_timeout
            msg.hard_timeout = rule.hard_timeout
            if (rule.action ==  "DST_TO_HNP"):
              msg.actions.append(of.ofp_action_nw_addr.set_dst(IPAddr("10.0.0.2")))
              msg.actions.append(of.ofp_action_output(port = dpid))
        #    core.openflow.getConnection(dpid).send(msg)
            event.connection.send(msg)
          #`  print msg.__dict__

      elif self.arp_for_unknowns:
        # We don't know this destination.
        # First, we track this buffer so that we can try to resend it later
        # if we learn the destination, second we ARP for the destination,
        # which should ultimately result in it responding and us learning
        # where it is

        # Add to tracked buffers
        if (dpid,dstaddr) not in self.lost_buffers:
          self.lost_buffers[(dpid,dstaddr)] = []
        bucket = self.lost_buffers[(dpid,dstaddr)]
        entry = (time.time() + MAX_BUFFER_TIME,event.ofp.buffer_id,inport)
        bucket.append(entry)
        while len(bucket) > MAX_BUFFERED_PER_IP: del bucket[0]

        # Expire things from our outstanding ARP list...
        self.outstanding_arps = {k:v for k,v in
         self.outstanding_arps.iteritems() if v > time.time()}

        # Check if we've already ARPed recently
        if (dpid,dstaddr) in self.outstanding_arps:
          # Oop, we've already done this one recently.
          return

        # And ARP...
        self.outstanding_arps[(dpid,dstaddr)] = time.time() + 4

        r = arp()
        r.hwtype = r.HW_TYPE_ETHERNET
        r.prototype = r.PROTO_TYPE_IP
        r.hwlen = 6
        r.protolen = r.protolen
        r.opcode = r.REQUEST
        r.hwdst = ETHER_BROADCAST
        r.protodst = dstaddr
        r.hwsrc = packet.src
        r.protosrc = packet.next.srcip
        e = ethernet(type=ethernet.ARP_TYPE, src=packet.src,
                     dst=ETHER_BROADCAST)
        e.set_payload(r)
        log.debug("%i %i ARPing for %s on behalf of %s" % (dpid, inport,
         str(r.protodst), str(r.protosrc)))
        msg = of.ofp_packet_out()
        msg.data = e.pack()
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        msg.in_port = inport
        event.connection.send(msg)

    elif isinstance(packet.next, arp):
      a = packet.next
      log.debug("%i %i ARP %s %s => %s", dpid, inport,
       {arp.REQUEST:"request",arp.REPLY:"reply"}.get(a.opcode,
       'op:%i' % (a.opcode,)), str(a.protosrc), str(a.protodst))

      if a.prototype == arp.PROTO_TYPE_IP:
        if a.hwtype == arp.HW_TYPE_ETHERNET:
          if a.protosrc != 0:

            # Learn or update port/MAC info
            if a.protosrc in self.arpTable[dpid]:
              if self.arpTable[dpid][a.protosrc] != (inport, packet.src):
                log.info("%i %i RE-learned %s", dpid,inport,str(a.protosrc))
            else:
              log.info("%i %i learned hey %s", dpid,inport,str(a.protosrc))
            self.arpTable[dpid][a.protosrc] = Entry(inport, packet.src)

            # Send any waiting packets...
            self._send_lost_buffers(dpid, a.protosrc, packet.src, inport)

            if a.opcode == arp.REQUEST:
              # Maybe we can answer

              if a.protodst in self.arpTable[dpid]:
                # We have an answer...

                if not self.arpTable[dpid][a.protodst].isExpired():
                  # .. and it's relatively current, so we'll reply ourselves

                  r = arp()
                  r.hwtype = a.hwtype
                  r.prototype = a.prototype
                  r.hwlen = a.hwlen
                  r.protolen = a.protolen
                  r.opcode = arp.REPLY
                  r.hwdst = a.hwsrc
                  r.protodst = a.protosrc
                  r.protosrc = a.protodst
                  r.hwsrc = self.arpTable[dpid][a.protodst].mac
                  e = ethernet(type=packet.type, src=dpid_to_mac(dpid),
                               dst=a.hwsrc)
                  e.set_payload(r)
                  log.info("%i %i answering ARP for %s" % (dpid, inport,
                   str(r.protosrc)))
                  msg = of.ofp_packet_out()
                  msg.data = e.pack()
                  msg.actions.append(of.ofp_action_output(port =
                                                          of.OFPP_IN_PORT))
                  msg.in_port = inport
                  event.connection.send(msg)
                  return

      # Didn't know how to answer or otherwise handle this ARP, so just flood it
      log.debug("%i %i flooding ARP %s %s => %s" % (dpid, inport,
       {arp.REQUEST:"request",arp.REPLY:"reply"}.get(a.opcode,
       'op:%i' % (a.opcode,)), str(a.protosrc), str(a.protodst)))

      msg = of.ofp_packet_out(in_port = inport, data = event.ofp,
          action = of.ofp_action_output(port = of.OFPP_FLOOD))
      event.connection.send(msg)

	# When we get flow stats, print stuff out
  def handle_flow_stats (self, event):
    web_bytes = 0
    web_flows = 0
    for f in event.stats:
      if f.match.tp_dst == 80 or f.match.tp_src == 80:
       web_bytes += f.byte_count
       web_flows += 1
       print ("Web traffic: %s bytes over %s flows", web_bytes, web_flows)
 
     # Listen for flow stats
       core.openflow.addListenerByName("FlowStatsReceived", handle_flow_stats)
 
# Now actually request flow stats from all switches
    for con in core.openflow.connections: # make this _connections.keys() for pre-betta
      con.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))

def launch (fakeways="", arp_for_unknowns=None):
  fakeways = fakeways.replace(","," ").split()
  fakeways = [IPAddr(x) for x in fakeways]
  if arp_for_unknowns is None:
    arp_for_unknowns = len(fakeways) > 0
  else:
    arp_for_unknowns = str_to_bool(arp_for_unknowns)
  core.registerNew(l3_switch, fakeways, arp_for_unknowns)

