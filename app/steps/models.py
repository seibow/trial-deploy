from django.db import models
from django.conf import settings

# Create your models here.
class StepsModel(models.Model):
    title = models.CharField(max_length=128)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    goals = models.ForeignKey(
    'goals.GoalsModel',
    on_delete=models.CASCADE,
    db_column='goals_id',
    related_name='steps'
    )