#dio koda preuzet sa https://youtu.be/WuyKxdLcw3w

from django.apps import AppConfig
from django.conf import settings

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

#za dodat sve nove usere u default grupu po defaultu
    def ready(self):
        from django.contrib.auth.models import Group
        from django.db.models.signals import post_save

        def add_to_default_group(sender, **kwargs):
            user = kwargs["instance"]
            if kwargs['created']:
                if not user.is_staff:  # Provjerite je li korisnik staff
                    group, ok = Group.objects.get_or_create(name="Registrirani")
                    group.user_set.add(user)

        post_save.connect(add_to_default_group,
                          sender=settings.AUTH_USER_MODEL)