from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from nested_admin.nested import NestedModelAdmin, NestedStackedInline, NestedTabularInline

# Register your models here.
from accounts.models import *

# admin.site.register(social_platformModel)
from content.models import ImageModel, ImageAlbumModel, hotspotModel

admin.site.register(profileModel)


admin.site.unregister(User)

class platformInline(NestedTabularInline):
    model=social_platformModel
    extra = 1

class rollinline(NestedTabularInline):
    model=rollModel
    extra = 1

    # fields = "__all__"
class UserProfileInline(NestedTabularInline):
    model = profileModel
    extra = 1

    inlines = [rollinline,platformInline ]
    def has_delete_permission(self, request, obj=None):
        return False


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, ]


class hotspotModelInline(NestedTabularInline):
    model = hotspotModel
    extra = 1


class ImageInline(NestedTabularInline):
    model = ImageModel
    extra = 0
    inlines = [hotspotModelInline, ]
    # fields = "__all__"

    # readonly_fields = ['mainpic']
    def image_tag(self, obj):
        return format_html('<img src="{}" width="150" height="150"/>'.format(obj.image.url))

    image_tag.short_description = 'تصویر'


class albumInlineInline(NestedTabularInline):
    model = ImageAlbumModel
    extra = 0
    inlines = [ImageInline, ]

    def has_delete_permission(self, request, obj=None):
        return False
class realstateadmin(NestedModelAdmin):
    # fields = "__all__"
    inlines = [platformInline,albumInlineInline]


admin.site.register(realstateModel, realstateadmin)
admin.site.register(User, UserProfileAdmin)
