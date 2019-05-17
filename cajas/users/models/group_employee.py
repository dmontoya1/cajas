from django.db import models
from .employee import Employee
from .group import Group


class GroupEmployee(models.Model):

    group = models.ForeignKey(
        Group,
        verbose_name='Grupo',
        on_delete=models.CASCADE,
        related_name='related_group'
    )

    supervisor = models.ForeignKey(
        Employee,
        verbose_name='Supervisor',
        on_delete=models.CASCADE,
        related_name='related_group_supervisor'
    )

    def __str__(self):
        return self.group.admin.user.username

    class Meta:
        verbose_name = 'Grupo'
