from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ClientAddress, Company, CustomUser, MoneySaver, UserRole


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
    list_editable = ["role"]
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
        "email",
        "phone",
        "balance",
    ]


@admin.register(MoneySaver)
class MoneySaverAdmin(admin.ModelAdmin):
    list_display = [
        "reester_number",
        "cashType",
        "balance",
        "company",
    ]


admin.site.register([ClientAddress])
