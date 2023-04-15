# -*- coding: utf-8 -*-
from django.db import models


# class DHT11Model(models.Model):  # crea el modelo que guarda temperatura y fecha
#     use_in_migrations = True
#     TEMPERATURE = models.FloatField(default=0)  # temp como float ej 24,01
#     HUMIDITY = models.FloatField(default=0)  # temp como float ej 24,01
#     DATE = models.DateTimeField(auto_now_add=True)  # la fecha es automatica cuando se registra una temp
#
#     class Meta:
#         ordering = ["pk"]
#
#     def __str__(self):
#         return '%s:  %s, %s:  %s' % (self.DATE, self.TEMPERATURE, self.DATE, self.HUMIDITY)

class CSMSModel(models.Model):  # crea el modelo que guarda temperatura y fecha
    use_in_migrations = True
    # TEMPERATURE = models.FloatField(default=0)  # temp como float ej 24,01
    HUMIDITY = models.FloatField(default=0)  # temp como float ej 24,01
    DATE = models.DateTimeField(auto_now_add=True)  # la fecha es automatica cuando se registra una temp

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return '%s:  %s' % (self.DATE, self.HUMIDITY)


class PumpingValueModel(models.Model):
    use_in_migrations = True
    id = models.AutoField(primary_key=True)
    value = models.PositiveIntegerField(default=50)

    def __str__(self):
        return self.value

    def save(self, *args, **kwargs):
        super(PumpingValueModel, self).save(*args, **kwargs)
#
# class HumModel(models.Model):  # crea el modelo que guarda temperatura y fecha
#     HUMIDITY = models.FloatField()  # temp como float ej 24,01
#     DATE = models.DateTimeField(auto_now_add=True)  # la fecha es automatica cuando se registra una temp
#
#     class Meta:
#         ordering = ["pk"]
#
#     def __str__(self):
#         return '%s:  %s' % (self.DATE, self.HUMIDITY,)
