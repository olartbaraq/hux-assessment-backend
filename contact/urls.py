"""
URL configuration for contact project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin  # type: ignore
from django.urls import include, path  # type: ignore
from user_control.views import login, logout, register_user  # type: ignore

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/register/", register_user, name="register"),
    path("api/v1/auth/login/", login, name="login"),
    path("api/v1/contact/", include("contact_control.urls")),
    path("api/v1/auth/logout/", logout, name="logout"),
]
