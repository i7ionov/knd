from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Department)
admin.site.register(models.User)
admin.site.register(models.Article)
admin.site.register(models.OrganizationType)
admin.site.register(models.Recipient)
admin.site.register(models.Address)