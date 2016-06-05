import os
import sys
import datetime
import django
import commands

from itertools import groupby
from operator import itemgetter
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "madapp.settings")
from django.core.management import execute_from_command_line
from django.db.models import Count, Avg
import django.db.models.query

from madapp import settings
from madapp.mad.models import *

import time
django.setup()

INTERVAL = 0.1


while True:
  config_MD = ConfigTable.objects.values('ex_mdDeteccao', 'block_seqPortas','block_numFluxos')
  for conf in config_MD:
      exec_md = conf['ex_mdDeteccao'] # Define intervalo de Exec do Script
      block_seq =  conf['block_seqPortas'] # Define sequencia de portas no PortScan a serem bloq.
      block_nunf = conf['block_numFluxos'] # Define Numero de Fluxos a Partir do mesmo IP 
  print exec_md
  print block_seq
  print block_nunf 
  something = []
  pd_port = [] #Lista de portas Agrupadas
  swt_port = [] #Lista de switches e portas por fluxo concatenadas
# padrao = []  
  pattern = [] #Lista com portas a sererem identificadas como Padrao
  ip_atacante = [] #Lista de Ips Atacantes
  ip_rule = []
  swt_port_atacante = [] #Lista de portas com ataques ofiginados
  ip_ant = 0 
  ptr = 0
  tst = 0 # Define quando o teste por IP para Md.02
# IDENTIFICA PORTSCAN
  fl = TemporaryFlows.objects.values('ip_src','ip_dst','dst_port').filter(dst_port__lt = 10024).annotate(num_ports = Count('dst_port')).order_by('ip_src')
  for x in fl:
       if (ip_ant == x['ip_src']and ptr==0):                   
	 pd_port.append(x['dst_port'])
         for k, g in groupby(enumerate(pd_port), lambda (i, x): i-x):
            pattern =  map(itemgetter(1), g)
         # Verifica se sequencia esta dentro do definido 
         if  len(pattern) > block_seq:   # Se for maior que o definido:
              ip_atacante.append(x['ip_src']) 
              print "ataque"
              ptr = 1
         else:
              ptr = 0
         ip_ant=x['ip_src']
       else:
         ip_ant=x['ip_src']
         ptr = 0
         del pattern[:]

# IDENTIFICA INSISTENCIA EM PORTA/FLUXOS
#  timeisnow=datetime.datetime.now() - timedelta(minutes=1)
  temps = TemporaryFlows.objects.values ('id_switch','switchport','ip_src','ip_dst', 'dst_port').filter(dst_port__lte='10024').annotate(num_ports=Count('dst_port'))
  counter = 0
  for flow in temps:
     counter = flow['num_ports']
# Se Numero de requisicoes for maior que o estabelecido
     if (counter > block_nunf): # verifica se ha varias tentativas na mesma porta
   #  swt_port_atacante.append(str(flow.id_switch) + ':' + str(flow.switchport))
# swt_port_atacante.append((str(flow['id_switch']) + ':' + (str(flow['switchport']))))
         print "Ataque MD2" 
         switches = Switches.objects.get(id_switch =flow['id_switch'])
         rt = RuleTable.objects.get_or_create(id_switch=switches, switchport = flow['switchport'], ip_src = flow['ip_src'],
             ip_dst = flow['ip_dst'], dst_port = flow['dst_port'], idle_timeout=3000, hard_timeout=20000, action='DST_HONEYPOT')
#         hr = HistoricoRules(id_switch=switch, ip_src = ip_flow,
#             ip_dst = f['ip_dst'], idle_timeout=3000, hard_timeout=20000, action='DST_HONEYPOT',timestamp=timezone.now())

#         hr.save()

#         rt.save()
     else:
      	 attack = 0

# CRIAR REGRAS A PARTIR DOS FLUXOS IDENTIFICADOS COMO ATAQUES;
  flows = TemporaryFlows.objects.values ('id_switch','ip_src','ip_dst', 'dst_port').filter(dst_port__lt = 10024)
  rules = RuleTable.objects.all()
  for rule in rules:
      if (rule.action=='DST_HONEYPOT'):
     	 pass
      else:
     	 ip_rule.append(str(rule.id_switch) + ':' + rule.ip_src  + ':' + rule.ip_dst)
  for f in flows:
      ip_flow = f['ip_src']
      ipf_dst = f['ip_dst']
      switch_id = str(f['id_switch'])
      something.append(switch_id + ':' + ip_flow + ':' + ipf_dst)
#      swt_port.append(str(f.id_switch) + ':' + str(f.switchport))
#      print "THIS IS SWT PORT"
#      print swt_port
#      print swt_port_atacante
      if (ip_flow in ip_atacante) and ((switch_id + ':' + ip_flow + ':' + ipf_dst) not in ip_rule):
        switch = Switches.objects.get(id_switch =flow['id_switch'])
        rule = RuleTable.objects.get_or_create(id_switch=switch, ip_src = ip_flow,
             ip_dst = f['ip_dst'], idle_timeout=3000, hard_timeout=20000, action='DROP')
#        rt = HistoricoRules(id_switch=switch, ip_src = ip_flow,
#             ip_dst = f['ip_dst'], idle_timeout=3000, hard_timeout=20000, action='DROP',timestamp=timezone.now())

#        rt.save()
#        print ip_atacante 
#        print 'ATENCAO ATAQUE ADVINDO DOS IPS %s', ip_atacante
      else:
        print 'Nao ha ataques md._01'
#        counter = swt_port_atacante.__len__()
#      all(x in swt_port for x in swt_port_atacante)
#      a = "HI"
#      a = all(x)
#      print str(a)
  
#      for i in range(0,counter):
#          for j in swt_port_atacante[i]:
#            if (swt_port_atacante[i] in swt_port) and (tst==0):
#               print "ATENCAO ATAQUE MODULO 2"
#               tst == 1
#            else:
#               print "Nao ha ataques md.02"
#               tst == 0
#  swt_port_atacante 
#ARMAZENA REGRAS NA TABELA DEFINITIVA E LIMPA TABELA TEMPORARIA
  rls = RuleTable.objects.all().filter(ip_dst='10.0.0.1',action='DST_HONEYPOT').delete()
  fl = TemporaryFlows.objects.all()
  for flow in fl:
      collectedflows =StatsTable(id_switch = flow.id_switch, switchport = flow.switchport, ip_src = flow.ip_src, ip_dst = flow.ip_dst, src_port = flow.src_port, dst_port = flow.dst_port, timestamp = timezone.now())
      collectedflows.save()
  dl_temp = TemporaryFlows.objects.all().delete()
  time.sleep(exec_md)

