from django.db import models


class Task(models.Model):
    
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    due_date = models.DateTimeField(null=True, blank=True)
    phonenumber=models.BigIntegerField(null=0, blank=True)
    age=models.IntegerField(null=True,blank=True)
     
    

    def __str__(self):
        return self.title

