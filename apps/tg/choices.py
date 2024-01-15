from django.db.models import IntegerChoices


class RoleTypeChoices(IntegerChoices):
    ADMIN = 0, "Admin"
    USER = 1, "Foydalanuvchi"
    NOT_SPECIFIED = 2, "Noaniq"
