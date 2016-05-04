from django.contrib import admin
from .models import RuleTable
from .models import ConfigTable
	
admin.site.register(RuleTable)
admin.site.register(ConfigTable)

# Register your models here.
