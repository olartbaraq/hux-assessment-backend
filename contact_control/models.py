from django.db import models  # type: ignore

# Create your models here.


class Contact(models.Model):
    """Model Contact equivalent to Contcat tabble to store the contacts information

    Args:
        models (class): a classnto be extends from while creating a Model/Table
    """

    firstname = models.CharField(max_length=50, blank=False, null=False)
    lastname = models.CharField(max_length=50, blank=False, null=False)
    phone_number = models.CharField(max_length=15, unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.firstname} - {self.lastname}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "Contact"
