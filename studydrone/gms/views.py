# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

#from polls.models import Choice, Poll


class IndexView(TemplateView):
    template_name = 'gms/index.html'


