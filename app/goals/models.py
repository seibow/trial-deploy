from django.db import models
from django.conf import settings

# Create your models here.
class GoalsModel(models.Model):
    title = models.CharField(max_length=128)
    limit_age = models.DateField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name='goals'
    )