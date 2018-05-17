from urllib.parse import quote

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.template import RequestContext
from django.utils.functional import SimpleLazyObject

from trelleux.models import TrelloClient


def home(request):
    return render_to_response('index.html')

def get_started(request):
    site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    root = "{0}://{1}".format(protocol, site.domain)

    url = 'https://trello.com/1/authorize?key={application_key}&name=Trelleux&expiration=never&response_type=token&callback_method=fragment&return_url={return_url}&scope=read,write'.format(
        application_key = settings.TRELLO_DEVELOPER_KEY,
        return_url = quote("%s/trello_auth/" % root),
    )
    return HttpResponseRedirect(url)

def trello_auth(request):
    c = {}

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
