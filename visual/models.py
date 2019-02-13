from django.db import models


# Create your models here.
class NeuralNetworkModel(models.Model):
    model_name = models.CharField(max_length=30)
    model_period = models.IntegerField()


class Fruit(models.Model):
    name = models.CharField(max_length=100, primary_key=True)