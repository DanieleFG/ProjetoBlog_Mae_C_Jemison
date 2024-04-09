from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Cadastro

@receiver(post_save, sender=Cadastro)
def create_user(sender, instance, created, **kwargs):
    if created:
        User.objects.create_user(username=instance.email, email=instance.email, password=instance.senha)
