from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    occupation = models.CharField(max_length=200)
    salary = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Transactions(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_amount = models.IntegerField()
    purpose = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} --> {self.transaction_amount}"
