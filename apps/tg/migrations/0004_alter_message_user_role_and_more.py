# Generated by Django 4.2.7 on 2023-12-04 07:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tg", "0003_alter_chat_subscribers_alter_message_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="user_role",
            field=models.IntegerField(
                choices=[(0, "Admin"), (1, "Foydalanuvchi"), (2, "Noaniq")],
                default=2,
                verbose_name="Rol",
            ),
        ),
        migrations.AlterField(
            model_name="telegramuser",
            name="current_role_in_chat",
            field=models.IntegerField(
                choices=[(0, "Admin"), (1, "Foydalanuvchi"), (2, "Noaniq")],
                default=2,
                verbose_name="Rol",
            ),
        ),
    ]
