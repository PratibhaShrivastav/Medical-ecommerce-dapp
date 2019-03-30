from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username+"'s cart"

class BlockIds(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block_id = models.IntegerField(null=False,blank=False)

    def __str__(self):
        return self.user.username + "'s block number " + self.block_id