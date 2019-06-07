from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Course


# Create your views here.
@login_required
def createcourse(request):

	if request.method == 'POST':
		if request.POST['title'] and request.POST['description']:
			course = Course()
			course.title = request.POST['title']
			course.description = request.POST['description']
			if request.FILES.get('course_image', False):
						course.course_image = request.FILES['course_image']
			else:
				return render(request, 'course/createcourse.html',{'error':'cant upload image'})
			course.creation_date = timezone.datetime.now()
			course.creator = request.user
			course.save()
			return redirect('home')
		else:
			return render(request, 'course/createcourse.html',{'error':'All fields are required'})
	else:
		return render(request, 'course/createcourse.html')
