from django.db import models
from django.conf import settings

class MethodRouting(models.Model):

    method = models.CharField(
        max_length=255,
        verbose_name="Operation id ",
        help_text="Test endpoint opreation id",
        blank=True,
        null=True
    )

    bank_id_pattern = models.CharField(
        max_length=255,
        verbose_name="bank_id_pattern id ",
        help_text="bank_id_pattern",
        blank=True,
        null=True
    )

    parameters = models.CharField(
        max_length=255,
        verbose_name="parameters ",
        help_text="parameters",
        blank=True,
        null=True
    )

    value = models.CharField(
        max_length=255,
        verbose_name="value",
        help_text="value",
        blank=True,
        null=True,
    )

    select2 = models.CharField(
        max_length=255,
        verbose_name="select2",
        help_text="select2",
        blank=True,
        null=True,
    )

    select1 = models.CharField(
        max_length=255,
        verbose_name="select1",
        help_text="select1",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Test Profile Operation'
        verbose_name_plural = 'Test Profile Operation'
