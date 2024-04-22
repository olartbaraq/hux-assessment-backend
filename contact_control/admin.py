from django.contrib import admin  # type: ignore

from contact_control.models import Contact  # type: ignore

# Register your models here to enable us see it in django admin panel.

admin.site.register(Contact)
