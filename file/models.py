from django.db import models
from datetime import date


class Employee(models.Model):
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField()
    salary = models.IntegerField()
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))