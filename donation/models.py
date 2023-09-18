from django.db import models

from goal.models import GoalModel

class DonationModel(models.Model):

    name = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    text = models.TextField(max_length=300, blank=True, null=True)
    donation = models.IntegerField()
    paid = models.BooleanField(default=False)
    goal = models.ForeignKey(GoalModel, on_delete=models.CASCADE, related_name='donation')
    payment_method = models.CharField(max_length=3, null=True, blank=True)
    payment_token = models.CharField(max_length=36, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'

    def __str__(self):
        return f'{self.donation} - {self.goal}'