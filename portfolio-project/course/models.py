from django.db import models
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class Course(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    is_publishable = models.BooleanField(default=False)
    course_image = models.ImageField(upload_to='images/')
    wd = models.ManyToManyField('WikiData',blank=True)


class WikiData(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.CharField(max_length=2000, blank=True)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=1000, blank=True)
#    associated_course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class CoursePart(models.Model):
    associated_course_id =  models.IntegerField()
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    body = models.TextField(blank=True)

class Quiz(models.Model):
    associated_coursepart_id =  models.IntegerField()
    question = models.CharField(max_length=255)
    trueAnswer = models.CharField(max_length=255)
    falseAnswer1 = models.CharField(max_length=255)
    falseAnswer2 = models.CharField(max_length=255)
    falseAnswer3 = models.CharField(max_length=255)
