from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader
from stories.models import Story, Sprint
from django.http import HttpResponse
from django.views.generic import DetailView, ListView

class SprintView(DetailView):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    model = Sprint

    def get_context_data(self, **kwargs):
        context = super(SprintView, self).get_context_data(**kwargs)
        context['burndown'] = self.burndown()
        return context
    def burndown(self):
      total = self.object.original_commitment()
      burn = map(lambda (i,e): (self.days[i], total-total*i/4, total*1.2-total*i/4*1.2, total*0.8-total*i/4*0.8,total-e),enumerate(self.object.burnup()))
      return burn


class SprintListView(ListView):
    queryset = Sprint.objects.all().order_by('-start_date')
    def get_context_data(self, **kwargs):
        context = super(SprintListView, self).get_context_data(**kwargs)
        context['TVI'] = self.getTVI()
        return context
    def getTVI(self):
        return map(lambda s: (s.number, s.targeted_value_increase()), self.object_list.order_by('start_date').filter(is_finished=True).all())
