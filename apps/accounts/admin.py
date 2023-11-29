from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (CustomUser,
                     UserRole, Company)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "company",
        "role",

    ]
    list_editable = ['role']
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "role",
                    "company",
                )
            },
        ),
    )


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "address",
        "email",
        "phone",

    ]



