from django.shortcuts import render, redirect
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
			coursepart.associated_course_id = course.id
			coursepart.description = request.POST['description']
			coursepart.body = request.POST['body']
			coursepart.save()
			request.session['coursepart_id'] = coursepart.id
			if 'Finalize' in request.POST:
				return redirect('home')
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
								return redirect('home')
		else:
			return render(request,'course/createquiz.html',{'coursepart':coursepart},{'error':'at least a question and one answer is needed'})
	else:
		return render(request,'course/createquiz.html',{'coursepart':coursepart})

#@app.route('/wikidata', methods=['POST'])
def wikidata(request):
	if request.method =="POST":
		wikidata_id = request.POST['search_text']
	else:
		wikidata_id = ""
	wikidata = WikiData()

	API_ENDPOINT = "https://www.wikidata.org/w/api.php"
	query =  wikidata_id
	params = {
		    'action': 'wbsearchentities',
		    'format': 'json',
		    'language': 'en',
		    'limit': '1',
		    'search': query
		}
	wiki_request = requests.get(API_ENDPOINT, params = params)
	w_json = wiki_request.json()['search']
	w_json = json.dumps(w_json)
	w_json = json.loads(w_json)

	for entity in w_json:
		wikidata.name = entity['label']
		wikidata.description = entity['description']
		wikidata.url = "https:" + entity['url']
	try:
		URL = "https://www.wikidata.org/w/api.php?action=wbgetclaims&entity={}&format=json".format(wikidata_id)
		req = requests.get(URL).json()
		image_name= req['claims']['P18'][0]['mainsnak']['datavalue']['value']
		image_name = image_name.replace(' ', '_')
		md5sum = hashlib.md5(image_name.encode('utf-8')).hexdigest()
		a = md5sum[:1]
		ab = md5sum[:2]
		image_URL = "https://upload.wikimedia.org/wikipedia/commons/{}/{}/{}".format(a,ab,image_name)
		wikidata.image_url = image_URL
	except:
		pass
		wikidata.associated_course = 1
	wikidata.save()
	return HttpResponse('Post request success')
