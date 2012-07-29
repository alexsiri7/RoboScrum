from django.conf.urls.defaults import *
from stories.views import SprintView, SprintListView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('stories.views',
    url(r'^$',SprintListView.as_view()),
    url(r'^sprint/(?P<pk>\d+)/$',
         SprintView.as_view()
	),
)

