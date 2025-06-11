# --- File: agents/models.py ---
# Model for the Agentic Service.
from django.db import models

class Agent(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

