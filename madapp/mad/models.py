from __future__ import unicode_literals

from django.db import models


class FlowTableHasStatsTable(models.Model):
    flow_table_flow_id = models.IntegerField(db_column='Flow_table_Flow.id')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    stats_table_stats_id = models.ForeignKey('StatsTable', db_column='Stats_table_Stats.id')  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Flow_table_has_Stats_table'
      


class RuleTable(models.Model):
    id_rule = models.AutoField(primary_key=True)
    id_switch = models.ForeignKey('Switches', db_column='id_switch', verbose_name="Nome do Switch")
    switchport = models.IntegerField(db_column='switchPort', blank=True, null=True, verbose_name="Porta do Switch")  # Field name made lowercase.
    ip_src = models.CharField(max_length=45, verbose_name="IP de Origem")
    ip_dst = models.CharField(max_length=45, verbose_name="IP de Destino")
    src_port = models.IntegerField(blank=True, null=True, verbose_name="Porta de Origem")
    dst_port = models.IntegerField(blank=True, null=True, verbose_name="Porta de Destino")
    action = models.CharField(max_length=45, blank=True, null=True, verbose_name="Action")
    timestamp = models.DateTimeField(blank=True, null=True)
    idle_timeout = models.IntegerField(blank=True, null=True)
    hard_timeout = models.IntegerField(blank=True, null=True)
    # Inserir Regras manualmente
    def __unicode__(self):
 	 return "IP de Origem:" + self.ip_src + "| Porta de Origem:" + str(self.src_port) + "| IP de Destino:" + self.ip_dst + "| Porta de Destino:" + str(self.dst_port) + "| ACTION:" + self.action
    class Meta:
        verbose_name = 'Adicionar Regra'
        verbose_name_plural = 'Adicionar Regras'
        managed = False
        db_table = 'Rule_table'

class HsTable(models.Model):
    id_rule = models.AutoField(primary_key=True)
    id_switch = models.ForeignKey('Switches', db_column='id_switch')
    switchport = models.IntegerField(db_column='switchPort', blank=True, null=True)  # Field name made lowercase.
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
    stats_id = models.AutoField(db_column='Stats.id', primary_key=True)  # Field name made lowercase. 
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
        return str(self.name_switch)
    
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
    id_switch=  models.ForeignKey('Switches', db_column='id_switch')
    switchport = models.IntegerField(db_column='switchPort', blank=True, null=True)  # Field name made lowercase.
    ip_src = models.CharField(max_length=45, blank=True, null=True)
    ip_dst = models.CharField(max_length=45, blank=True, null=True)
    src_port = models.IntegerField(blank=True, null=True)
    dst_port = models.IntegerField(blank=True, null=True)

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

    class Meta:
        managed = False
        db_table = 'Usage_table'
