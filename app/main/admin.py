from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *


class PersonInline(admin.StackedInline):
    model = Person
    can_delete = False


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass
    # inlines = [PersonInline]


@admin.register(Vebmaster)
class VebmasterAdmin(admin.ModelAdmin):
    pass


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ['name', 'image','image_url']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            image_url = obj.image.url
            obj.image_url = image_url

        if change:

            if obj.image:
                obj.image_url = obj.image.url

        obj.save()


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    pass


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    pass
