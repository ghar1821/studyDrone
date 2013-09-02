import os
import sys	
sys.path.append('/var/www/studydrone/studydrone')
os.environ['DJANGO_SETTINGS_MODULE'] = 'studydrone.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
