from django.db import models
from dictionaries.models import User


class ExportResult(models.Model):
    text = models.TextField(null=True)
    datetime = models.DateTimeField(null=True)
    file = models.FileField(upload_to='exports/', null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
