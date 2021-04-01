from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import profileModel, realstateModel, ImageAlbumModel


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            profileModel.objects.create(user=instance)
        instance.user_profile.save()
@receiver(post_save, sender=realstateModel)
def create_or_update_album(sender, instance, created, **kwargs):
        if created:
            ImageAlbumModel.objects.create(album=instance)
