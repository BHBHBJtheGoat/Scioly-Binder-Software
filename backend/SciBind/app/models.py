from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .helpers.document import document
from SciBind.settings import MEDIA_ROOT

import os
import random
import uuid

# Create your models here.


class DocumentField(models.Field):
    description = "A document field that can be added to a binder"

    def __init__(self, document, *args, **kwargs):
        self.document = document
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return "document"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["document"] = self.document
        return name, path, args, kwargs


class User(AbstractUser):
    chosen_events = models.ManyToManyField("EventModel", related_name="owners")
    profile_picture = models.ImageField(
        upload_to="profile_pictures", default="profile_pictures/default.png"
    )


def get_random_profile_picture():
    template_dir = os.path.join(MEDIA_ROOT, "profile_pictures", "templates")
    if templates := [
        f for f in os.listdir(template_dir) if f.endswith((".png", ".jpg", ".jpeg"))
    ]:
        return os.path.join("profile_pictures", "templates", random.choice(templates))
    return "profile_pictures/default.png"


@receiver(post_save, sender=User)
def set_random_profile_picture(sender, instance, created, **kwargs):
    if created:
        instance.profile_picture = get_random_profile_picture()
        instance.save()


class EventModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    # materialtype can either be 'binder', 'cheat sheet', or 'none'
    materialchoices = [
        ("binder", "Binder"),
        ("cheat sheet", "Cheat Sheet"),
        ("none", "None"),
    ]
    materialtype = models.CharField(max_length=100, choices=materialchoices)
    divchoices = ("a", "b", "c")
    divchoices = [(x, x) for x in divchoices]
    division = models.CharField(max_length=1, choices=divchoices)
    # Check if there are objects of this instance

    def __str__(self):
        return self.name

    def has_objects(self):
        return self.bindermodel_set.exists()


class BinderModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    shared_with = models.ManyToManyField(
        User, related_name="shared_binders", blank=True
    )
    materialtype = models.CharField(
        max_length=100, choices=EventModel.materialchoices, blank=True
    )
    division = models.CharField(max_length=1, choices=EventModel.divchoices, blank=True)
    old = models.BooleanField(default=False)
    online_users = models.ManyToManyField(User, related_name="online_binders")
    def save(self, *args, **kwargs):
        if self.event:
            self.materialtype = self.event.materialtype
            self.division = self.event.division
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event.name} Binder - {self.owner.username}"
