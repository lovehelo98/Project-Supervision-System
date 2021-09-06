from django.db import models
from User_Management_System.models import Account
from ckeditor.fields import RichTextField
from django.utils import timezone

# Create your models here.
class markingGrids(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class assessmentCriterias(models.Model):
    title = models.ForeignKey(markingGrids, on_delete=models.CASCADE)
    criteria = models.CharField(max_length=50)

    class Meta:
        ordering = ['criteria']

    def __str__(self):
        return self.criteria

class descriptions(models.Model):
    criteria = models.ForeignKey(assessmentCriterias, on_delete=models.CASCADE)
    descp = RichTextField(blank=True, null=True)
    #descp = models.CharField(max_length=100)

    class Meta:
        ordering = ['descp']

    def __str__(self):
        return self.descp

class comments(models.Model):
    student = models.ForeignKey(Account, related_name="Student", on_delete=models.CASCADE,)
    description = models.ForeignKey(descriptions, on_delete=models.CASCADE,)
    comment = models.CharField(max_length=100)
    teacher = models.ForeignKey(Account, related_name="Teacher", on_delete=models.CASCADE,)
    date	= models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['comment']

    def __str__(self):
        return self.comment 

class marks(models.Model):
    student = models.ForeignKey(Account, on_delete=models.CASCADE,)
    grid = models.ForeignKey(markingGrids, related_name="Grid", on_delete=models.CASCADE, null=True, blank=True)
    criteria = models.ForeignKey(assessmentCriterias, related_name="crt", null=True, blank=True, on_delete=models.SET_NULL)  
    marks = models.IntegerField(default=0)

    def __str__(self):
        return str(self.marks)
    
    
    
