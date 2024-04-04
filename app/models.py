from django.db import models
from django.contrib.auth.models import User
# Create your models here.
status_choices = [
    ('C', 'completed'),
    ('P', 'pending'),
]
priority_choices = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
]


class TODO(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(
        max_length=1, choices=status_choices, default='P')
    priority = models.CharField(
        max_length=1, choices=priority_choices, default='1')
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # image=models.ImageField(upload_to='images/',null=True,blank=True)


class profile(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
