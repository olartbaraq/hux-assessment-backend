from django.db import models  # type: ignore
from user_control.models import User


class Contact(models.Model):
    """Model Contact equivalent to Contcat tabble to store the contacts information

    Args:
        models (class): a class into be extends from while creating a Model/Table
    """

    firstname = models.CharField(max_length=50, blank=False, null=False)
    lastname = models.CharField(max_length=50, blank=False, null=False)
    phone_number = models.CharField(unique=True, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.firstname} - {self.lastname}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "Contact"
