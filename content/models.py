from django.db import models
from django_jalali.db import models as jmodels
# Create your models here.
from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.models import realstateModel
from accounts.utils import compress


class ImageModel(models.Model):

    class Meta:
        verbose_name="تصویر"
        verbose_name_plural="تصاویر"

    image = models.ImageField(verbose_name="تصویر اصلی",upload_to="a")
    album = models.ForeignKey("ImageAlbumModel",verbose_name="مربوط به آلبوم", related_name="imagesA", on_delete=models.CASCADE)
    create_time = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.album.id)

    # def save(self, *args, **kwargs):
    #     if self.mainpic:
    #         try:
    #             temp = ImageModel.objects.get(mainpic=True)
    #             if self != temp:
    #                 temp.mainpic = False
    #                 temp.save()
    #         except ImageModel.DoesNotExist:
    #             pass
    #     new_image = compress(self.image)
    #     self.image = new_image
    #     super().save(*args, **kwargs)
    #     # instance = super(ImageModel, self).save(*args, **kwargs)
    #     # image = ImageModel.open(instance.photo.path)
    #     # image.save(instance.photo.path, quality=50, optimize=True)
    #     # return instance
    #     # else:
    #     #
    #     #     try:
    #     #         temp= ImageModel.objects.get(mainpic=True)
    #     #
    #     #     except:
    #     #
    #     #         self.mainpic = True
    #     #         self.save()
    #     super(ImageModel, self).save(*args, **kwargs)
    # content_connect = models.ForeignKey("content", related_name='images', on_delete=models.CASCADE)
    # name = models.CharField(max_length=255)
    # default = models.BooleanField(default=False)
    # width = models.FloatField(default=100)
    # length = models.FloatField(default=100)


class ImageAlbumModel(models.Model):
    schoices = (
        (0, "غیرفعال"),
        (1, "فعال")
    )
    class Meta:
        verbose_name="آلبوم"
        verbose_name_plural="آلبوم"
    # class Meta:
    #     verbose_name="آلبوم"
    #     verbose_name_plural="آلبوم ها"
    # albumname = models.CharField(max_length=30, default=get_album_name, editable=False)
    album = models.ForeignKey("accounts.realstateModel",verbose_name="مربوط به املاک ", related_name='modelAlbum', on_delete=models.CASCADE, null=True)
    title = models.CharField(verbose_name="عنوان",max_length=20)
    create_time = jmodels.jDateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(verbose_name="وضعیت",choices=schoices, default=1)
    # parent=models.ForeignKey("ImageAlbumModel",verbose_name="مربوط به آلبوم",on_delete=models.PROTECT)
    def get_images(self):
        image = self.imagesA.all()
        return image

    def set_images(self, images):
        for i in images:
            self.imagesA.create(image=i)

    def default(self):
        return self.imagesA.filter(default=True).first()

    def thumbnails(self):
        return self.imagesA.filter(width__lt=100, length_lt=100)

    def __str__(self):
        return str(self.id)

        # instance.ImageAlbumModel.save()

class hotspotModel(models.Model):

    x=models.SmallIntegerField(verbose_name="مختصات افقی",default=0,null=True,blank=True)
    y=models.SmallIntegerField(verbose_name="مختصات عمودی",default=0,null=True,blank=True)
    z=models.SmallIntegerField(verbose_name="مختصات عمقی",default=0,null=True,blank=True)
    hotspot=models.ForeignKey("ImageModel",verbose_name="هات اسپات برای ", on_delete=models.CASCADE,related_name="imagehotspot")
    def __str__(self):
        return f"({self.x},{self.y},{self.z})"


@receiver(pre_save, sender=ImageModel)
def pre_save_image(sender, instance, **kwargs):
    # if not instance._state.adding:
    #     pass
    # else:
    new_image = compress(instance.image)
    instance.image = new_image

