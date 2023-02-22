from django.db import models

class PaypalModel(models.Model):

    access_token = models.CharField(max_length=100)
    expires_in = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'PayPal'
        verbose_name_plural = 'PayPal'

    def __str__(self):
        return f"{self.expires_in}"