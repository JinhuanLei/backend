from django.db import models


# Create your models here.
class NeuralNetworkModel(models.Model):
    model_name = models.CharField(max_length=30)
    model_duration = models.IntegerField()
    model_created = models.DateTimeField(auto_now_add=True, blank=True)
    model_path = models.CharField(max_length=100)


class Layer(models.Model):
    config_id = models.IntegerField()
    num_nets = models.IntegerField()
    model_id = models.IntegerField()


class Config(models.Model):
    num_passes = models.IntegerField()
    model_id = models.IntegerField()
    loss_function = models.CharField(max_length=30)
    sequence_length = models.IntegerField()
    batch_size = models.IntegerField()
    recur_button = models.BooleanField()
    drop_out = models.FloatField()
    max_grad = models.IntegerField()
    variational_recurrent = models.BooleanField()

class TrainingSet(models.Model):
    path = models.CharField(max_length=100)


