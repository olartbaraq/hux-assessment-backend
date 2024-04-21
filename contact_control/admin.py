from django.contrib import admin  # type: ignore

from contact_control.models import Contact  # type: ignore

# Register your models here.

admin.site.register(Contact)
