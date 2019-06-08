from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Course
from .models import WikiData
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
			return redirect('home')
		else:
			return render(request, 'course/createcourse.html',{'error':'All fields are required'})
	else:
		return render(request, 'course/createcourse.html')

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
