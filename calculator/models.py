from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"

class University(models.Model):
    title = models.CharField(max_length=100)
    
    in_state= models.IntegerField()
    out_state = models.IntegerField()
    
    def __str__(self):
        return f"{self.title}"

class Salary(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE) #many to one relationship with job title
    state = models.CharField(max_length=30, blank=True, null=True) #state fields that are null or blank are U.S average salary

    entry = models.IntegerField()
    middle = models.IntegerField()
    senior = models.IntegerField()

    def __str__(self):
        return f"{self.job} - {self.state}"