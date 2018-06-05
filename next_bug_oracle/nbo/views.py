from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.views import generic
import requests
import json

from .models import Bug


def index(request):
    return render(request, 'nbo/index.html')


def result(request):
    gh_url = 'https://api.github.com/search/issues?q='
    bz_url = 'https://bugzilla.mozilla.org/rest/bug'

    gh1 = 'repo:webcompat/web-bugs+state:open+label:priority-critical+-author:webcompat-bot&sort=created&order=asc'
    bz1_query = {
        'include_fields': 'id,summary,creation_time', 'product':
        'tech evangelism', 'component': ['desktop', 'mobile'], 'priority':
        'p1', 'whiteboard': 'needsdiagnosis', 'f1': 'resolution', 'o1':
        'isempty', 'order': 'creation_time%20asc'}
    gh2a = 'repo:webcompat/web-bugs+state:open+label:priority-important+-author:webcompat-bot&sort=created&order=asc'
    gh2b = 'repo:webcompat/web-bugs+state:open+label:priority-critical+author:webcompat-bot&sort=created&order=asc'
    bz3_query = {
        'include_fields': 'id,summary,creation_time', 'product':
            'tech evangelism', 'component': ['desktop', 'mobile'], 'priority':
            'p1', 'whiteboard': 'needsdiagnosis', 'f1': 'resolution', 'o1':
            'isempty', 'order': 'creation_time%20asc'}
    gh3 = 'repo:webcompat/web-bugs+state:open+label:priority-normal&sort=created&order=asc'

    bug = Bug()

    r = requests.get(bz_url, params=bz1_query)

    if r.status_code == requests.codes.ok:
        try:
            bug_list = r.json()
            if len(bug_list['bugs']) > 0:
                bug.bug_id = bug_list['bugs'][0]['id']
                bug.bug_text = bug_list['bugs'][0]['summary']
                bug.report_date = bug_list['bugs'][0]['creation_time']
                bug.source = 'bugzilla'
                bug_url_string = 'https://bugzilla.mozilla.org/show_bug.cgi?id=' + \
                    str(bug.bug_id)
                bug.link = bug_url_string
            else:
                r = requests.get(gh_url + gh1)

                if r.status_code == requests.codes.ok:
                    try:
                        bug_list = r.json()
                        if bug_list['total_count'] > 0:
                            bug.bug_id = bug_list['items'][0]['number']
                            bug.bug_text = bug_list['items'][0]['title']
                            bug.report_date = bug_list['items'][0]['created_at']
                            bug.source = 'github'
                            bug.link = bug_list['items'][0]['html_url']
                        else:
                            print("No bugs for you -- something wrong with GH call.")
                    except ValueError:
                        print("There's a problem with your json data.")
        except ValueError:
            print("There's a problem with your json data.")
    else:
        print("HTTP response code: " + r.status_code)

    context = {'bug': bug}
    return render(request, 'nbo/result.html', context)
