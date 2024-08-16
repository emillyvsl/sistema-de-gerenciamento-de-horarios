from django.db import models

class Centro(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)