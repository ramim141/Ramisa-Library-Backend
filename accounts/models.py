from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserAccount(models.Model):
    user=models.OneToOneField(User,related_name='account',on_delete=models.CASCADE)
    initial_deposite_date=models.DateField(auto_now_add=True)
    balance=models.DecimalField(default=0,max_digits=12, decimal_places=2)
    image=models.ImageField(upload_to='accounts/')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'