# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class KidbrightProject(models.Model):
    time = models.DateTimeField()
    temp = models.FloatField()
    light = models.FloatField()
    humidity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'kidbright_project'


class ApiData(models.Model):
    time = models.DateTimeField()
    temp = models.FloatField()
    wind_kph = models.FloatField()
    humidity = models.IntegerField()
    w_condition = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'api_data'
