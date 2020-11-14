from django.db import models
from django.utils import timezone
#
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
#
from authApp.models import User


class VehicleManager(models.Manager):
    def get_queryset(self):
        return super(VehicleManager, self).get_queryset() \
            .filter(active=True)


class Vehicle(models.Model):
    plate = models.CharField(verbose_name='Placa',
                             max_length=9, unique=True)
    description = models.TextField(
        verbose_name='Descrição', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='vehicles')
    slug = models.SlugField(unique=True, blank=True)

    objects = VehicleManager()

    def get_absolute_url_edit(self):
        return reverse("vehicle_edit", args={self.slug})

    def get_absolute_url_delete(self):
        return reverse("vehicle_delete", args={self.slug})

    def get_absolute_url_access(self):
        return reverse("vehicle_access", args={self.pk})

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ('plate',)

    def __str__(self):
        return str(self.plate)


@receiver(post_save, sender=Vehicle)
def insert_slug(sender, instance, **kwargs):
    if not instance.slug:
        slug = slugify(instance.plate)
        instance.slug = slug
        return instance.save()
