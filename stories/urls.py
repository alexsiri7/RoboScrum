from django.views.generic import DetailView, ListView
from django.conf.urls.defaults import *
from stories.models import Sprint

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('stories.views',
    url(r'^$',
         ListView.as_view(
		queryset=Sprint.objects.all().order_by('-start_date')[:5]
	)),
    url(r'^sprint/(?P<pk>\d+)/$',
         DetailView.as_view(
            model=Sprint)
	),
)

