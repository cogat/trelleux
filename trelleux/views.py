import urllib
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.template import RequestContext
from djangosite.trelleux.models import TrelloClient
from djangosite.trelleux.trello import Client


def home(request):
    return render_to_response('index.html')

def get_started(request):
    url = 'https://trello.com/1/authorize?key={application_key}&name=Trelleux&expiration=never&response_type=token&callback_method=fragment&return_url={return_url}&scope=read,write'.format(
        application_key = settings.TRELLO_KEY,
        return_url = urllib.quote("%s/trello_auth/" % settings.SITE_URL),
    )
    return HttpResponseRedirect(url)

def trello_auth(request):
    c = RequestContext(request)

    if request.method == "POST":
        if request.POST['action'] == 'create':
            tc = get_object_or_404(TrelloClient, client_auth_token=request.POST.get('token'))
            tc.create_board()
            return HttpResponseRedirect("/trello_auth/?token=%s" % tc.client_auth_token)
    elif request.method == "GET":
        if request.GET.get('token'):
            tc, created = TrelloClient.objects.get_or_create(client_auth_token=request.GET.get('token'))
            c['client'] = tc

    return render_to_response('manage_boards.html', c)
