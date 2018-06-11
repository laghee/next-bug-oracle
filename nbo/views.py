from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.views import generic

from .helpers import *

from .models import Bug


def index(request):
    return render(request, 'nbo/index.html')


def result(request):
    gh_url = "https://api.github.com/search/issues?q="

    bz_url = "https://bugzilla.mozilla.org/rest/bug"

    gh1 = """repo:webcompat/web-bugs+state:open+label:priority-critical+
    -author:webcompat-bot+milestone:needsdiagnosis&sort=created&order=asc"""

    bz1_query = {
        'include_fields': 'id,summary,creation_time', 'product':
        'tech evangelism', 'component': ['desktop', 'mobile'], 'priority':
        'p1', 'whiteboard': 'needsdiagnosis', 'f1': 'resolution', 'o1':
        'isempty', 'order': 'creation_time%20asc'}

    gh2a = """repo:webcompat/web-bugs+state:open+label:priority-important+-
    author:webcompat-bot+milestone:needsdiagnosis&sort=created&order=asc"""

    gh2b = """repo:webcompat/web-bugs+state:open+label:priority-critical+
    author:webcompat-bot+milestone:needsdiagnosis&sort=created&order=asc"""

    bz3_query = {
        'include_fields': 'id,summary,creation_time', 'product':
        'tech evangelism', 'component': ['desktop', 'mobile'], 'priority':
        'p1', 'whiteboard': 'needsdiagnosis', 'f1': 'resolution', 'o1':
        'isempty', 'order': 'creation_time%20asc'}

    gh3 = """repo:webcompat/web-bugs+state:open+label:priority-normal+
    milestone:needsdiagnosis&sort=created&order=asc"""

    bug_one = bz_call(bz_url, bz1_query)
    bug_two = gh_call(gh_url, gh1)

    if bug_one is not None and bug_two is not None:
        bugs = [bug_one, bug_two]
        context = {'bug': random.choice(bugs)}
        return render(request, 'nbo/result.html', context)
    elif bug_one is not None:
        context = {'bug': bug_one}
        return render(request, 'nbo/result.html', context)
    elif bug_two is not None:
        context = {'bug': bug_two}
        return render(request, 'nbo/result.html', context)
    else:
        bug = Bug()
        bug.bug_id = 911
        bug.bug_text = "Something has gone terribly wrong."
        bug.link = "https://www.emaildesignreview.com/wp-content/uploads/2014/10/cat1.jpg"
        context = {'bug': bug}
        return render(request, 'nbo/result.html', context)
