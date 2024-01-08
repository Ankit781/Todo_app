from django.db import models
from django.utils.text import slugify

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('WORKING', 'Working'),
        ('DONE', 'Done'),
        ('OVERDUE', 'Overdue'),
    ]
     
    timestamp = models.DateTimeField(auto_now_add=True,editable=False)
    title = models.CharField(max_length = 100, blank = False)
    description = models.CharField(max_length = 1000, blank = False)
    due_date = models.DateTimeField(editable=True)
    tags = models.ManyToManyField(Tag, blank=True)
    status =models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN',blank = False)
    

    
    def __str__(self):
        return self.title

        
    

    
    
