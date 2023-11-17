from djongo import models


class Form(models.Model):
    fields = models.JSONField()
