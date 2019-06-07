from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    is_publishable = models.BooleanField(default=False)
    course_image = models.ImageField(upload_to='images/')
