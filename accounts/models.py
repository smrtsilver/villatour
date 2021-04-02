from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_jalali.db import models as jmodels
from accounts.utils import compress
from ckeditor.fields import RichTextField
# Create your models here.

# from django.conf import settings
# import os
#

# def index_path_upload(instance, filename):
#     if not instance.pk:
#        # get count of all object, so is will be unique
#        number = instance.__class__.objects.count() + 1
#     else:
#        number = instance.pk
#     # replace filename to all object have the same
#     filename = "index.html"
#     path =  f"templates/theme/template{number}/{filename}"
#     return os.path.join(settings.BASE_DIR, path)

def get_upload_path(instance, filename):
    # model = instance.content.__class__._meta
    username=instance.user.username
    return f'profile/{username}/{filename}'


class profileModel(models.Model):
    class Meta:
        verbose_name="پروفایل"
        verbose_name_plural="پروفایل"
    schoices = (
        (0, "غیرفعال"),
        (1, "فعال")
    )
    profile_pic = models.ImageField(verbose_name="عکس پروفایل",upload_to="profileModel", null=True)
    user = models.OneToOneField(User, verbose_name="کابر",on_delete=models.CASCADE, related_name="user_profile")
    phonenumber = models.CharField(verbose_name="شماره تماس",max_length=11)
    bio = RichTextField(verbose_name="بیوگرافی")
    profileroll = models.ManyToManyField("rollModel",verbose_name="نقش ها", related_name="profile_roll")
    status = models.SmallIntegerField(verbose_name="وضعیت",choices=schoices, default=1)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            profileModel.objects.create(user=instance)
        instance.user_profile.save()


class rollModel(models.Model):
    class Meta:
        verbose_name="نقش"
        verbose_name_plural="نقش"
    Choices = (
        (1, "مشاور ملک"),
        (2, "مدیر ملک"),
    )
    schoices = (
        (0, "غیرفعال"),
        (1, "فعال")
    )
    roll = models.IntegerField(verbose_name="نقش",choices=Choices, default=1)
    rollamlak = models.ForeignKey("realstateModel",verbose_name="املاک", related_name="roll_amlak", on_delete=models.PROTECT)
    create_time = jmodels.jDateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(verbose_name="وضعیت",choices=schoices, default=1)


class social_platformModel(models.Model):
    class Meta:
        verbose_name="شبکه اجتماعی"
        verbose_name_plural="شبکه اجتماعی"
    pChoices = (
        (1, "تلگرام"),
        (2, "اینستاگرام"),
        (3, "سایت"),
    )

    platform = models.IntegerField(verbose_name="پلتفرم",choices=pChoices)
    platform_ID = models.CharField(verbose_name="آیدی",max_length=50)
    realstate_connect = models.ForeignKey("realstateModel", verbose_name="مربوط به املاک",on_delete=models.CASCADE, related_name="realstate_platform",
                                          null=True, blank=True)
    profile_connect = models.ForeignKey("profileModel", verbose_name="مربوط به شخص",on_delete=models.CASCADE, related_name="realstate_platform",
                                        null=True, blank=True)


class realstateModel(models.Model):
    class Meta:
        verbose_name = "املاک"
        verbose_name_plural = "املاک"

    schoices = (
        (0, "غیرفعال"),
        (1, "فعال")
    )
    logo = models.ImageField(verbose_name="لوگو", upload_to="logo", null=True)
    header = models.ImageField(verbose_name="بنر", upload_to="headers", null=True)
    name = models.CharField(verbose_name="نام", max_length=20)
    bio = RichTextField(verbose_name="توضیحات", )
    address = models.TextField(verbose_name="آدرس", )
    create_time = jmodels.jDateTimeField(auto_now_add=True)
    update_time = jmodels.jDateTimeField(auto_now=True)
    status = models.SmallIntegerField(verbose_name="وضعیت", choices=schoices, default=1)

    def __str__(self):
        return self.name

    def delete_post(self):
        self.status = 0
        self.save()


class phonenumberModel(models.Model):
    class Meta:
        verbose_name="شماره تماس"
        verbose_name_plural="شماره تماس"
    # Todo
    # add validator
    number = models.CharField(verbose_name="شماره تماس",max_length=20)
    amlaknumber = models.ForeignKey("profileModel",verbose_name="مربوط به املاک", on_delete=models.CASCADE, related_name="phonenumber_realstate")



@receiver(pre_save, sender=realstateModel)
def pre_save_image(sender, instance, **kwargs):
    # if not instance._state.adding:
    #     pass
    # else:
    newlogo = compress(instance.logo)
    instance.logo = newlogo
    newheader = compress(instance.header)
    instance.header = newheader
