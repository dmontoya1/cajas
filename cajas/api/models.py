# -*- coding: utf-8 -*-
import uuid
from django.db import models

from .helpers import generate_key


class APIKey(models.Model):
    """
    Clase para manejar las restricciones en las APIs
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50, unique=True)
    key = models.CharField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = generate_key()
        super(APIKey, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Llave de API"
        verbose_name_plural = "Llaves de API"
        ordering = ['-created']
        app_label = "api"

    def __str__(self):
        return self.name
