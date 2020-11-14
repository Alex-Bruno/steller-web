from django.db import models
from django.utils import timezone
from django.urls import reverse
#
from accessApp.models import Vehicle


class AccessManager(models.Manager):
    def get_queryset(self):
        return super(AccessManager, self).get_queryset() \
            .filter(active=True)


class Access(models.Model):
    plate = models.CharField(verbose_name='Placa', max_length=12, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    entrance = models.DateTimeField(verbose_name='Entrada', blank=True, null=True)
    exit = models.DateTimeField(verbose_name='Saída', blank=True, null=True)
    active = models.BooleanField(default=True)
    vehicle = models.ForeignKey(Vehicle,
                                on_delete=models.CASCADE,
                                related_name='access',
                                blank=True, null=True)

    isCreatedManual = models.BooleanField(default=False)
    isUpdatedManual = models.BooleanField(default=False)

    objects = AccessManager()

    def get_absolute_url_edit(self):
        return reverse("access_edit", args={self.pk})

    class Meta:
        verbose_name = "Acesso"
        verbose_name_plural = "Acessos"
        ordering = ('-created',)

    def __str__(self):
        if self.plate:
            return self.plate
        return self.vehicle.plate
