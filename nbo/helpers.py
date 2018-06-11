import requests
import random

from .models import Bug

json_err_text = "There's a problem with your json data."

http_text = "HTTP response code: "

bug = Bug()


def gh_call(gh_address, gh_params):
    r = requests.get(gh_address + gh_params)
    if r.status_code == requests.codes.ok:
        try:
            bug_list = r.json()
            list_size = bug_list['total_count']
            if list_size > 0:
                selector = random.randint(0, list_size-1)
                bug.bug_id = bug_list['items'][selector]['number']
                bug.bug_text = bug_list['items'][selector]['title']
                bug.report_date = bug_list['items'][selector]['created_at']
                bug.source = 'github'
                bug.link = bug_list['items'][selector]['html_url']
                return bug
            else:
                return None
        except ValueError:
            print(json_err_text)
    else:
        print(http_text + r.status_code)


def bz_call(bz_address, bz_params):
    bug_url_string = "https://bugzilla.mozilla.org/show_bug.cgi?id="
    r = requests.get(bz_address, params=bz_params)
    if r.status_code == requests.codes.ok:
        try:
            bug_list = r.json()
            list_size = len(bug_list['bugs'])
            if list_size > 0:
                selector = random.randint(0, list_size-1)
                bug.bug_id = bug_list['bugs'][selector]['id']
                bug.bug_text = bug_list['bugs'][selector]['summary']
                bug.report_date = bug_list['bugs'][selector]['creation_time']
                bug.source = 'bugzilla'
                bug_url_string += str(bug.bug_id)
                bug.link = bug_url_string
                return bug
            else:
                return None
        except ValueError:
            print(json_err_text)
    else:
        print(http_text + r.status_code)
