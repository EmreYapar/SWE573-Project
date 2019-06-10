from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Course
from .models import WikiData
from .models import CoursePart
from .models import Quiz
import operator
import requests
import json
import hashlib
from django.http import HttpResponse


# Create your views here.
@login_required
def createcourse(request):

	if request.method == 'POST':
		if 'Finalize'in request.POST:
			redirect(home)
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
			request.session['course_id'] = course.id
			return render(request,'course/createcoursepart.html', {'course':course})
		else:
			return render(request, 'course/createcourse.html',{'error':'All fields are required'})
	else:
		return render(request, 'course/createcourse.html')

def createcoursepart(request):
	course_id =request.session['course_id']
	courses = Course.objects.all()
	for c in courses:
		if course_id == c.id:
			course = c
	if request.method == 'POST':
		if request.POST['title'] and request.POST['description'] and request.POST['body']:
			coursepart = CoursePart()
			coursepart.title = request.POST['title']
			coursepart.course = course
			coursepart.associated_course_id = course.id
			coursepart.description = request.POST['description']
			coursepart.body = request.POST['body']
			coursepart.save()
			request.session['coursepart_id'] = coursepart.id
			if 'Finalize' in request.POST:
					return render(request,'course/wikidata.html')
			elif 'AddQuiz' in request.POST:
				return render(request,'course/createquiz.html', {'coursepart':coursepart})
			elif 'AddPart' in request.POST:
				return render(request,'course/createcoursepart.html',{'course':course})

		else:
			return redirect(request,'course/createcoursepart.html',{'course':course}, {'error':'All fields are required'})
	else:

		return render(request,'course/createcoursepart.html',{'course':course})

def createquiz(request):
	coursepart_id = request.session['coursepart_id']
	courseparts = CoursePart.objects.all()
	coursepart = CoursePart()
	course = Course()
	for cp in courseparts:
		if coursepart_id == cp.id:
			coursepart = cp
	if request.method == 'POST':
		if request.POST['question'] and request.POST['trueanswer']:
			quiz = Quiz()
			quiz.associated_coursepart_id = coursepart.id
			quiz.question = request.POST['question']
			quiz.trueAnswer = request.POST['trueanswer']
			quiz.falseAnswer1 = request.POST['falseanswer1']
			quiz.falseAnswer2 = request.POST['falseanswer2']
			quiz.falseAnswer3 = request.POST['falseanswer3']
			quiz.save()
			if 'AddQuiz' in request.POST:
				return render(request,'course/createquiz.html',{'coursepart':coursepart})
			elif 'AddPart' in request.POST:
				courses =  Course.objects.all()
				for c in courses:
					if coursepart.associated_course_id == c.id:
						course = c
				return render(request,'course/createcoursepart.html',{'course':course})
			elif 'Finalize' in request.POST:
				return render(request,'course/wikidata.html')
		else:
			return render(request,'course/createquiz.html',{'coursepart':coursepart},{'error':'at least a question and one answer is needed'})
	else:
		return render(request,'course/createquiz.html',{'coursepart':coursepart})


def viewcourse(request,course_id):
	course = get_object_or_404(Course, pk=course_id)
	request.session['current_enrolled_course'] = course.id
	wikidatas = WikiData.objects.all()
	return render(request, 'course/viewcourse.html',{'course':course},{'wikidatas',wikidatas})

def viewcourseparts(request):
	course = get_object_or_404(Course, pk=request.session['current_enrolled_course'])
	courseparts = CoursePart.objects.all()
	for cp in courseparts:
		if request.session['current_enrolled_course'] == cp.associated_course_id:
			coursepart = cp
	request.session['current_enrolled_course_part'] = coursepart.id
	if request.method == 'POST':
		if 'Home' in request.POST:
			return redirect('home');
		if 'Enroll' in request.POST:
			return render(request,'course/viewcourseparts.html',{'coursepart':coursepart})
	return render(request,'course/viewcourseparts.html',{'coursepart':coursepart})

def viewcoursequiz(request):
	quizes = Quiz.objects.all()
	for q in quizes:
		if request.session['current_enrolled_course_part'] == q.associated_coursepart_id:
			quiz = q
	request.session['current_enrolled_course_part']
	if request.method == 'POST':
		if 'trueAnswer' in request.POST:
			return redirect('home')
		else:
			return render(request, 'course/viewcoursequiz.html', {'quiz':quiz}, {'error':'Wrong Answer, Try Again'})
	return render(request, 'course/viewcoursequiz.html', {'quiz':quiz})












#@app.route('/wikidata', methods=['POST'])
def wikidata(request):
	wikidatas = WikiData.objects.all()
	course_id = request.session['course_id']
	if request.method =="POST":
		if 'Finalize' in request.POST:
			return redirect('home')
		for wd in wikidatas:
			if str(wd.id) == request.POST:
				wd.delete()

		if 'search_text' in request.POST:
			wikidata_id = request.POST['search_text']
			request.session['search_text'] = wikidata_id
		else:
			wikidata_id = request.session['search_text']
		API_ENDPOINT = "https://www.wikidata.org/w/api.php"
		query =  wikidata_id
		params = {
			   	'action': 'wbsearchentities',
		    	'format': 'json',
		    	'language': 'en',
		    	'limit': '10',
			    'search': query
				}
		wiki_request = requests.get(API_ENDPOINT, params = params)
		w_json = wiki_request.json()['search']
		w_json = json.dumps(w_json)
		w_json = json.loads(w_json)

		wikidata = WikiData()
		for i in range(0,10):
			if str(i) in request.POST:
				wikidata.name = w_json[i]['label']
				wikidata.description = w_json[i]['description']
				wikidata.code = w_json[i]['url']
				wikidata.associated_course_id = course_id
				wikidata.save()
				return render(request,'course/wikidata.html',{'w_json':w_json, 'course_id':course_id, 'wikidatas':wikidatas})
		return render(request,'course/wikidata.html',{'w_json':w_json, 'course_id':course_id, 'wikidatas':wikidatas})
	else:
		return render(request,'course/wikidata.html')
