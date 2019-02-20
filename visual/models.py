from django.db import models


# Create your models here.
class NeuralNetworkModel(models.Model):
    model_name = models.CharField(max_length=30)
    model_duration = models.IntegerField()
    model_created = models.CharField(max_length=30)
    model_path = models.CharField(max_length=100)


class Layer(models.Model):
    config_id = models.IntegerField()
    num_nets = models.IntegerField()
    model_id = models.IntegerField()


class Config(models.Model):
    dropout_rate = models.DecimalField(max_digits=5, decimal_places=5)
    num_passes = models.IntegerField()
    model_id = models.IntegerField()


