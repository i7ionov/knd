from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Court)
admin.site.register(models.ExecutionResult)
admin.site.register(models.Adjudication)
admin.site.register(models.ADStage)
