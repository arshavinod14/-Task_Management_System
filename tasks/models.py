from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('completed','Completed')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='Pending')
    due_date = models.DateField()

    def __str__(self):
        return self.title
    