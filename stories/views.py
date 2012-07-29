from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader
from stories.models import Story, Sprint
from django.http import HttpResponse

def home(req):
    latest_sprint_list = Sprint.objects.all().order_by('-start_date')[:5]
    c = {'latest_sprint_list': latest_sprint_list}
    return render_to_response('sprint/index.html', c)

def detail(req, sprint_id):
    sprint = get_object_or_404(Sprint,id=sprint_id)
    return render_to_response('sprint/detail.html',{'sprint': sprint})
