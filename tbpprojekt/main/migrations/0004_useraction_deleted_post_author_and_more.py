# Generated by Django 4.2.2 on 2023-06-19 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_useraction_target_post_useraction_target_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraction',
            name='deleted_post_author',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='useraction',
            name='action_type',
            field=models.CharField(choices=[('POST', 'User created a post'), ('DELETE', 'User deleted a post'), ('BANNED', 'User banned user'), ('UNBANNED', 'User unbanned user')], max_length=12),
        ),
        migrations.AlterField(
            model_name='useraction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to=settings.AUTH_USER_MODEL),
        ),
    ]
