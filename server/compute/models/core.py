# from model_utils.managers import InheritanceManager
from abc import abstractmethod
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import Group, Permission
from django.utils import timezone
from django.db import models
from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager
from simple_history.models import HistoricalRecords

class Item(PolymorphicModel):
    is_collection = models.BooleanField(default=False)

    class Meta:
        abstract = True

class ModelHierarchy(models.Model):
    child = models.CharField(max_length=125)
    parent = models.CharField(max_length=125)
    filter_path_to_child = models.CharField(max_length=500)
    filter_path_to_parent = models.CharField(max_length=500)

    class Meta:
        unique_together = [["child", "parent","filter_path_to_child","filter_path_to_parent"]]


    def __str__(self):
        return "{1} > {0}".format(self.child, self.parent)