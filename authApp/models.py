# coding=utf-8
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)
#
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Nome de usuário', max_length=30, unique=True)
    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome', max_length=100)

    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False)

    date_joined = models.DateTimeField('Data de cadastro', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    slug = models.SlugField(unique=True)

    objects = UserManager()

    def __str__(self):
        return self.name or self.username

    def get_shot_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

@receiver(post_save, sender=User)
def insert_slug(sender, instance, **kwargs):
    if not instance.slug:
        slug = slugify(instance.username)
        instance.slug = slug
        return instance.save()