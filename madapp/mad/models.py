# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class FlowTableHasStatsTable(models.Model):
    flow_table_flow_id = models.IntegerField(db_column='Flow_table_Flow.id')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    stats_table_stats_id = models.ForeignKey('StatsTable', db_column='Stats_table_Stats.id')  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Flow_table_has_Stats_table'
      # unique_together = (('Flow_table_Flow.id', 'Stats_table_Stats.id'),)


class RuleTable(models.Model):
    id_rule = models.AutoField(primary_key=True)
    id_switch = models.ForeignKey('Switches', db_column='id_switch')
    switchport = models.IntegerField(db_column='switchPort', blank=True, null=True)  # Field name made lowercase.
   # mac_src = models.CharField(max_length=45, blank=True, null=True)
   # mac_dst = models.CharField(max_length=45, blank=True, null=True)
    ip_src = models.CharField(max_length=45)
    ip_dst = models.CharField(max_length=45)
    src_port = models.IntegerField(blank=True, null=True)
    dst_port = models.IntegerField(blank=True, null=True)
    action = models.CharField(max_length=45, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    idle_timeout = models.IntegerField(blank=True, null=True)
    hard_timeout = models.IntegerField(blank=True, null=True)
    # Inserir Regras manualmente
    def __unicode__(self):
 	 return "| IP de Origem:" + self.ip_src + "| Porta de Origem:" + str(self.src_port) + "| IP de Destino:" + self.ip_dst + "| Porta de Destino:" + str(self.dst_port) + "| ACTION:" + self.action
    class Meta:
        verbose_name = 'Tabela de Regra'
        verbose_name_plural = 'Tabela de Regras'
        managed = False
        db_table = 'Rule_table'

class HsTable(models.Model):
    id_rule = models.AutoField(primary_key=True)
    id_switch = models.ForeignKey('Switches', db_column='id_switch')
    switchport = models.IntegerField(db_column='switchPort', blank=True, null=True)  # Field name made lowercase.
   # mac_src = models.CharField(max_length=45, blank=True, null=True)
   # mac_dst = models.CharField(max_length=45, blank=True, null=True)
    ip_src = models.CharField(max_length=45)
    ip_dst = models.CharField(max_length=45)
    src_port = models.IntegerField(blank=True, null=True)
    dst_port = models.IntegerField(blank=True, null=True)
    action = models.CharField(max_length=45, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    idle_time = models.IntegerField(blank=True, null=True)
    hard_time = models.IntegerField(blank=True, null=True)
    # Inserir Regras manualmente
    def __unicode__(self):
         return "| IP de Origem:" + self.ip_src + "| Porta de Origem:" + str(self.src_port) + "| IP de Destino:" + self.ip_dst + "| Porta de Destino:" + str(self.dst_port) + "| ACTION:" + self.action
    class Meta:
        verbose_name = 'Tabela de Regra'
        verbose_name_plural = 'Registro de Regras'
        managed = False
        db_table = 'Hs_table'

class StatsTable(models.Model):
    stats_id = models.AutoField(db_column='Stats.id', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
#    id_temporaryflow = models.ForeignKey('TemporaryFlows', db_column='id_temporaryflow')
    id_switch=  models.ForeignKey('Switches', db_column='id_switch')
    switchport = models.IntegerField(db_column='switchPort', blank=True, null=True)  # Field name made lowercase.
    ip_src = models.CharField(max_length=45, blank=True, null=True)
    ip_dst = models.CharField(max_length=45, blank=True, null=True)
    src_port = models.IntegerField(blank=True, null=True)
    dst_port = models.IntegerField(blank=True, null=True)
    packet_counter = models.FloatField(db_column='Packet_counter', blank=True, null=True)  # Field name made lowercase.
    byte_counter = models.FloatField(db_column='Byte_counter', blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Stats_table'


class Switches(models.Model):
    id_switch = models.AutoField(primary_key=True)
    name_switch = models.CharField(max_length=45)
    def __unicode__(self):
        return str(self.id_switch)
    
    class Meta:
        managed = False
        db_table = 'Switches'

class ConfigTable(models.Model):
    id_config_table =  models.AutoField(db_column='id_config_table', primary_key=True)
    ex_mdDeteccao = models.IntegerField(blank=True, null=True, verbose_name="Ex. Modulo Deteccao cada (s)")
    ex_mdMitigacao = models.IntegerField(blank=True, null=True, verbose_name="Ex. Modulo Mitigacao cada (s)")
    block_seqPortas = models.IntegerField(blank=True, null=True,  verbose_name="Define requisicoes seq. para bloqueio")
    block_numFluxos = models.IntegerField(blank=True, null=True,  verbose_name="Numero de tentativas por porta para bloqueio")
    def __unicode__(self):
        return "|Executar Md. Deteccao cada: " + str(self.ex_mdDeteccao) + " Segundos" + "| Executar Md. Mitigacao cada: " + str(self.ex_mdMitigacao) + " Segundos" + "| Bloquear apos: " + str(self.block_seqPortas) + " Portas Sequenciais" + "| Bloqueas apos: " + str(self.block_numFluxos) + " Fluxos"

    class Meta:
        verbose_name = 'Configurar Modulos'
        verbose_name_plural = 'Configurar Modulos'
        managed = False
        db_table = 'Config_table'

class TemporaryFlows(models.Model):
    id_temporaryflow = models.AutoField(db_column='id_temporaryFlow', primary_key=True)  # Field name made lowercase.
  # id_switch = models.ForeignKey(Switches, db_column='id_switch')
    id_switch=  models.ForeignKey('Switches', db_column='id_switch')
    switchport = models.IntegerField(db_column='switchPort', blank=True, null=True)  # Field name made lowercase.
#    mac_src = models.CharField(max_length=45, blank=True, null=True)
#    mac_dst = models.CharField(max_length=45, blank=True, null=True)
    ip_src = models.CharField(max_length=45, blank=True, null=True)
    ip_dst = models.CharField(max_length=45, blank=True, null=True)
    src_port = models.IntegerField(blank=True, null=True)
    dst_port = models.IntegerField(blank=True, null=True)
#    action = models.CharField(max_length=45, blank=True, null=True)
#    timeout_time = models.TimeField(blank=True, null=True)
#    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Temporary_Flows'


class UsageTable(models.Model):
    srv_id = models.AutoField(db_column='Srv.id', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    servername = models.CharField(db_column='Servername', max_length=45)  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True)
    cpu_usage = models.FloatField(db_column='Cpu_usage', blank=True, null=True)  # Field name made lowercase.
    input_traffic = models.FloatField(db_column='Input_traffic', blank=True, null=True)  # Field name made lowercase.
    output_traffic = models.FloatField(db_column='Output_traffic', blank=True, null=True)  # Field name made lowercase.
    timestamp =  models.DateTimeField()
  #  timestamp = models.CharField(db_column='Timestamp', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Usage_table'
