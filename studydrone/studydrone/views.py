# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView

# Needed for templates
from django.template.loader import get_template
from django.template import Context

from django.http import HttpResponse

#def home(request):
#	return HttpResponse("Hello home base, you'll have a link to both apps")

def index(request):
		return render(request, 'index.html')
	
def signup(request):
	return render(request, 'signup.html', {"foo": "bar"})

def login(request):
		if request.method == 'POST':
				username = request.POST['email']
				password = request.POST['password']
				# Get the right redirect variable
				user = authenticate(username=username, password=password)
				if user is not None and user.is_active:
						login(request,user)
						#if for the redirect
						#Use a redirect for the below
						return render(request,'needs_redirect.html')
				return render(request,'invalid_user.html')
		# form = LoginForm();
		#return render(request,'signup.html')



#    context_object_name = 'latest_poll_list'

#    def get_queryset(self):
#        """Return the last five published polls."""
#        return Poll.objects.order_by('-pub_date')[:5]

