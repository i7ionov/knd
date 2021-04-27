from django.db import models

# Create your models here.

class Request(models.Model):
    task = models.TextField()
    token = models.TextField()
    type = models.TextField()
    text = models.TextField()


class Response(models.Model):
    request = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True)
    name = models.TextField()
    exe_production = models.TextField()
    details = models.TextField()
    subject = models.TextField()
    department = models.TextField()
    bailiff = models.TextField()
    ip_end = models.TextField()