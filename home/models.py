from django.db import models
from django.contrib.auth.models import AbstractUser

class Package(models.Model):
    pkg_name = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=25, blank=True, null=True)
    price = models.IntegerField()
    # validity_days = models.IntegerField()  # Duration of the package in days

    def __str__(self):
        return self.pkg_name

class AllUser(models.Model):
    userid = models.CharField(max_length=70, unique=True)
    name = models.CharField(max_length=70)
    contact = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    pkg = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
    rechargedate = models.DateField(null=True, blank=True)
    monthlyfees = models.IntegerField()
    balance = models.IntegerField(default=0)
    remarks = models.TextField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.userid

class UserRechargeHistory(models.Model):
    user = models.ForeignKey(AllUser, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=70, blank=True, null=True)  # Store the user's name at the time of payment
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True)
    recharge_date = models.DateTimeField(auto_now_add=True)
    monthlyfees = models.IntegerField(blank=True, null=True, default=0)
    remarks = models.TextField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.user_name:
            self.user_name = self.user.name
        if not self.monthlyfees:
            self.monthlyfees = self.user.monthlyfees
        if not self.package and self.user.pkg:
            self.package = self.user.pkg

        self.user.balance += self.monthlyfees
        self.user.save()
        super().save(*args, **kwargs)

class UserPaymentLedger(models.Model):
    user = models.ForeignKey(AllUser, on_delete=models.CASCADE, related_name='recharge_histories')
    user_name = models.CharField(max_length=70, blank=True, null=True)  # Store the user's name at the time of payment, if we give id to another one the name of past person will not change in ledger history so that we can tract user_id history correctly.
    paid_amount = models.IntegerField()
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_by = models.CharField(max_length=20, blank=True, null=True)
    received_by = models.CharField(max_length=20)
    # payment_method = models.CharField(max_length=20)
    remarks = models.TextField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.user_name:
            self.user_name = self.user.name
        self.user.balance -= self.paid_amount
        self.user.save()
        super().save(*args, **kwargs)
