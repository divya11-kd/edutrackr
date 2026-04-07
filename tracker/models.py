from django.db import models
from django.contrib.auth.models import User


# MARKS TRACKER
class Mark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    exam_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

    marks_obtained = models.IntegerField()
    total_marks = models.IntegerField()

    exam_date = models.DateField()
    feedback = models.TextField(blank=True)

    def percentage(self):
        return (self.marks_obtained / self.total_marks) * 100

    def __str__(self):
        return f"{self.subject} - {self.exam_name}"


# ASSIGNMENT TRACKER
class Assignment(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Submitted', 'Submitted'),
    ]

    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=200)

    due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )

    def __str__(self):
        return self.title


# TASK TRACKER
class Task(models.Model):

    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )

    due_date = models.DateField()

    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# PROFILE PAGE
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.user.username

from django.db import models
from django.contrib.auth.models import User

class Marks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    marks_obtained = models.IntegerField()
    total_marks = models.IntegerField()
    date = models.DateField()

    def percentage(self):
        return round((self.marks_obtained / self.total_marks) * 100, 2)

    def performance(self):
        p = self.percentage()

        if p >= 90:
            return "Excellent"
        elif p >= 75:
            return "Very Good"
        elif p >= 60:
            return "Good"
        elif p >= 40:
            return "Needs Improvement"
        else:
            return "Poor"

from django.db import models
from django.contrib.auth.models import User

class Assignment(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)

    name=models.CharField(max_length=200)

    subject=models.CharField(max_length=100)

    due_date=models.DateField()

    priority=models.CharField(max_length=20)

    completed=models.BooleanField(default=False)

from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    priority = models.CharField(max_length=20)

    due_date = models.DateField(null=True,blank=True)

    completed = models.BooleanField(default=False)
    def __str__(self):
        return self.title