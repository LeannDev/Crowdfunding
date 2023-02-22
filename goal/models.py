from django.db import models

from user.models import User

class GoalModel(models.Model):

  title = models.CharField(max_length=60, null=True, blank=True)
  description = models.CharField(max_length=300, null=True, blank=True)
  price = models.DecimalField(max_digits=7, decimal_places=2)
  goal = models.DecimalField(max_digits=11, decimal_places=2)
  progress = models.DecimalField(max_digits=11, decimal_places=2, default=0)
  completed = models.BooleanField(default=False)
  category = models.CharField(max_length=30, null=True, blank=True)
  user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='goal')

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = 'Goal'
    verbose_name_plural = 'Goals'

  def __str__(self):
    return self.title