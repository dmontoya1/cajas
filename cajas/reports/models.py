
from datetime import date

from django.contrib.postgres.fields import ArrayField
from django.db import models


class RankingOffice(models.Model):

    fields = ArrayField(
        ArrayField(
            models.CharField(
                "Campo",
                max_length=255,
                null=True,
                blank=True
            )
        )
    )
    start_date = models.DateField(
        'Fecha inicio ranking',
        default=date.today()
    )
    end_date = models.DateField(
        'Fecha fin ranking',
        default=date.today()
    )

    def __str__(self):
        return "Valores Ranking"
