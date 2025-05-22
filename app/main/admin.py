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
    inlines = [PersonInline]

@admin.register(CategoryAccess)
class CategoryAccessAdmin(admin.ModelAdmin):
    pass


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass



@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    pass


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    pass
