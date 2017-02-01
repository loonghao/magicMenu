#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7
import sys
import os
import re


def sendComment(message_):
    pr_url = os.environ['ghprbPullLink']
    pr_url = pr_url.replace("github.com/", "api.github.com/repos/")
    pr_url = pr_url.replace("pull", "pulls")
    repo = pr_url.split("/")
    user, repo = repo[-4:-2]
    from pygithub3 import Github
    gh = Github(user=user, token='6f05cf46b09e909138d384937d71a2fb5b65abaa', repo=repo)
    for x in gh.issues.list_by_repo().all():
        if hasattr(x, "pull_request"):
            if x.pull_request.url == pr_url:
                gh.issues.comments.create(x.number, message_)
                print "sending message"
                break

# ws = '/Users/haolong/PycharmProjects/magicMenu'
ws = os.environ['WORKSPACE']
f = file(os.path.join(ws, "output.txt"))
found = False


m = re.compile("([+-][0-9]{1,3}\.[0-9]{2})\)")
message = ""
for line in f:
    print line,
    if not found and line.startswith("Report"):
        found = True
    if found:
        search = m.search(line)
        if search:
            message += line
            r = float(search.groups(0)[0])
message += ""
sendComment(message)
if r >= 0:
    sys.exit(0)
else:
    sys.exit(1)
