from django.contrib import admin  # type: ignore

from user_control.models import BlackListedToken, User

# Register your models here.


admin.site.register(User)
admin.site.register(BlackListedToken)
