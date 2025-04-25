from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return self.username
    

class StudentMeasurement(models.Model):
    student_name = models.CharField(max_length=100)
    school_name = models.CharField(max_length=100)
    chest = models.FloatField()
    waist = models.FloatField()
    height = models.FloatField()
    sleeve_length = models.FloatField()

    def __str__(self):
        return f"{self.student_name} - {self.school_name}"
    
class FabricAccessory(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    measurement = models.ForeignKey(StudentMeasurement, on_delete=models.CASCADE, related_name="orders")
    fabric = models.ForeignKey(FabricAccessory, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')])

    def __str__(self):
        return f"Order {self.id} - {self.measurement.student_name}"