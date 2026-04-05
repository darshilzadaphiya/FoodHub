from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from .managers import ItemManager


# Create your models here.
class Item(models.Model):
    class Meta:
        indexes = [models.Index(fields = ['user_name','item_price'])]

    def __str__(self):
        return self.item_name

    def delete(self, using = None, keep_parents = False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    item_name = models.CharField(max_length=200, db_index=True)
    item_desc = models.CharField()
    item_price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    item_image = models.URLField(max_length=500, default='https://www.svgrepo.com/show/66980/fast-food-placeholder.svg')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True) #Saves timestamp of when deleted

    objects = ItemManager()
    all_objects = models.Manager()

class Category(models.Model):
    name = models.CharField(max_length=100)
    added_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.name