from django.shortcuts import render

from course.models import Course

def home(request):
    courses = Course.objects
    return render(request, 'jobs/home.html', {'courses':courses})

# Create your views here.
