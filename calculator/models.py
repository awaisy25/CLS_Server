from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"

class University(models.Model):
    name = models.CharField(max_length=100)
    
    in_state= models.IntegerField()
    out_state = models.IntegerField()
    
    def __str__(self):
        return f"{self.name}"