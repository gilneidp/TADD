# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(null=True, blank=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(unique=True, max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(null=True, blank=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FlowTableHasStatsTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flow_table_flow_id', models.IntegerField(db_column='Flow_table_Flow.id')),
            ],
            options={
                'db_table': 'Flow_table_has_Stats_table',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RuleTable',
            fields=[
                ('rule_id', models.AutoField(serialize=False, primary_key=True, db_column='Rule.id')),
                ('switchport', models.CharField(max_length=45, db_column='SwitchPort')),
                ('mac_src', models.CharField(max_length=45, null=True, db_column='MAC_src', blank=True)),
                ('mac_dst', models.CharField(max_length=45, null=True, db_column='MAC_dst', blank=True)),
                ('ip_src', models.CharField(max_length=45, null=True, db_column='IP_src', blank=True)),
                ('ip_dst', models.CharField(max_length=45, null=True, db_column='IP_dst', blank=True)),
                ('s_port', models.CharField(max_length=45, null=True, db_column='S_port', blank=True)),
                ('d_port', models.CharField(max_length=45, null=True, db_column='D_port', blank=True)),
                ('flow_table_flow_id', models.IntegerField(db_column='Flow_table_Flow.id')),
            ],
            options={
                'db_table': 'Rule_table',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StatsTable',
            fields=[
                ('stats_id', models.AutoField(serialize=False, primary_key=True, db_column='Stats.id')),
                ('packet_counter', models.FloatField(null=True, db_column='Packet_counter', blank=True)),
                ('byte_counter', models.FloatField(null=True, db_column='Byte_counter', blank=True)),
                ('flow_table_flow_id', models.IntegerField(db_column='Flow_table_Flow.id')),
            ],
            options={
                'db_table': 'Stats_table',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Switchs',
            fields=[
                ('id_switch', models.AutoField(serialize=False, primary_key=True)),
                ('name_switch', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'Switchs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SwitchsHasTemporaryFlows',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'Switchs_has_Temporary_Flows',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TemporaryFlows',
            fields=[
                ('id_temporaryflow', models.AutoField(serialize=False, primary_key=True, db_column='id_temporaryFlow')),
                ('switchport', models.IntegerField(null=True, db_column='switchPort', blank=True)),
                ('mac_src', models.CharField(max_length=45, null=True, blank=True)),
                ('mac_dst', models.CharField(max_length=45, null=True, blank=True)),
                ('ip_src', models.CharField(max_length=45, null=True, blank=True)),
                ('ip_dst', models.CharField(max_length=45, null=True, blank=True)),
                ('src_port', models.IntegerField(null=True, blank=True)),
                ('dst_port', models.IntegerField(null=True, blank=True)),
                ('action', models.CharField(max_length=45, null=True, blank=True)),
                ('timeout_time', models.TimeField(null=True, blank=True)),
                ('timestamp', models.DateTimeField()),
            ],
            options={
                'db_table': 'Temporary_Flows',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsageTable',
            fields=[
                ('srv_id', models.AutoField(serialize=False, primary_key=True, db_column='Srv.id')),
                ('servername', models.CharField(max_length=45, db_column='Servername')),
                ('cpu_usage', models.FloatField(null=True, db_column='Cpu_usage', blank=True)),
                ('input_traffic', models.FloatField(null=True, db_column='Input_traffic', blank=True)),
                ('output_traffic', models.FloatField(null=True, db_column='Output_traffic', blank=True)),
                ('timestamp', models.CharField(max_length=45, db_column='Timestamp')),
            ],
            options={
                'db_table': 'Usage_table',
                'managed': False,
            },
        ),
    ]
