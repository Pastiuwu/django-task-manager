from django.db import models
from django.utils import timezone 
from datetime import timedelta

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'Alta'),
        ('medium', 'Media'),
        ('low', 'Baja'),
    ]

    description = models.CharField(max_length=255)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return self.description

    def is_due(self):
        """Retorna True si la tarea ha vencido."""
        if self.deadline:
            return self.deadline < timezone.now()
        return False

    def is_approaching(self):
        """Retorna True si la fecha límite está cerca (por ejemplo, en las siguientes 24 horas)."""
        if self.deadline:
            return self.deadline - timezone.now() < timedelta(days=1)
        return False