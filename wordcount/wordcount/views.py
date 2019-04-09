from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def count(request):
    fulltext = request.GET['fulltext']

    wordlist = fulltext.split()
    worddictionary = {}

    for word in wordlist:
        if word in worddictionary:
            #Increase
            worddictionary[word] += 1
        else:
            #add to worddictionary
            worddictionary[word] = 1


    return render(request, 'count.html',{'fulltext':fulltext, 'count':len(wordlist), 'worddictionary':worddictionary})
