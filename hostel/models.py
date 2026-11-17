from django.db import models

class Hostel(models.Model):
    STATUS_CHOICES=[
        ('O', 'Open'),
        ('F', 'Full'),
    ]
    hostel_name = models.CharField(max_length=50)
    hostel_id = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    capacity = models.IntegerField()
    status = models.CharField(max_length=50,choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.hostel_id} - {self.hostel_name}"

class Room(models.Model):
    STATUS_CHOICES=[
        ('O', 'Open'),
        ('F', 'Full'),
    ]
    room_id = models.CharField(max_length=10)
    room_number = models.CharField(max_length=10)
    hostel_id = models.CharField(max_length=50)
    capacity = models.IntegerField()
    status = models.CharField(max_length=50,choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.room_id} - Room {self.room_number}"

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    student_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    room_id = models.CharField(max_length=10)
    birth_date = models.DateField(auto_now=False, auto_now_add=False)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    course = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"
    
class Warden(models.Model):
    warden_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    hostel_id = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)

class Visitor(models.Model):
    visitor_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    relation_to_student = models.CharField(max_length=50)
    date_of_visit = models.DateField()
    intime = models.TimeField()
    outtime = models.TimeField()
    contact = models.CharField(max_length=15)
    address = models.CharField(max_length=50)

class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('C', 'Cash'),
        ('B', 'Bank '),
        ('MM', 'Mobile Money'),
    ]
    STATUS_CHOICES = [
        ('P', 'Paid'),
        ('U', 'Unpaid'),    
    ]

    payment_id = models.CharField(max_length=10)
    student_id = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_payment = models.DateField()
    mode_of_payment = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    academic_year = models.CharField(max_length=10)
    semester = models.CharField(max_length=10)
