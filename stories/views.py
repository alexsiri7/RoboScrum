from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader
from stories.models import Story, Sprint
from django.http import HttpResponse
from django.views.generic import DetailView, ListView

class SprintView(DetailView):
    days = ["", "","Mon", "", "", "", "Tue", "", "", "", "Wed", "", "", "", "Thu", "", "Fri"]
    model = Sprint

    def get_context_data(self, **kwargs):
        context = super(SprintView, self).get_context_data(**kwargs)
	if self.object.is_finished:
	        context['burndown'] = self.burndown()
	else:
		context['burndown_schema'] = self.burndown_schema()
        return context
    def burndown(self):
      total = self.object.original_commitment()
      burn = map(lambda (i,e): (self.days[i], total-total*i/4, total*1.2-total*i/4*1.2, total*0.8-total*i/4*0.8,total-e),enumerate(self.object.burnup()))
      return burn
    def burndown_schema(self):
      total = self.object.original_commitment()
      burn = map(lambda (i,e): (
		self.days[i],
		total-total*i/17, 
		total*1.2-total*i/17*1.2, 
		total*0.8-total*i/17*0.8)
	     ,enumerate(range(17)))
      return burn


class SprintListView(ListView):
    queryset = Sprint.objects.all().order_by('-start_date')
    def get_context_data(self, **kwargs):
        context = super(SprintListView, self).get_context_data(**kwargs)
        context['TVI'] = self.getTVI()
	context['Points'] = self.getPoints()
	context['Pct'] = self.getPct()
        return context
    def getTVI(self):
        return map(lambda s: (s.number, s.targeted_value_increase()), self.object_list.order_by('start_date').filter(is_finished=True).all())
    def getPoints(self):
        return map(lambda s: (s.number, s.work_capacity()*100/s.member_dedication, s.velocity()*100/s.member_dedication, s.original_commitment()*100/s.member_dedication), 
		self.object_list.order_by('start_date').filter(is_finished=True).all())
    def getPct(self):
        return map(lambda s: (s.number, s.focus_factor(), s.accuracy_of_estimation(), s.accuracy_of_commit()), 
		self.object_list.order_by('start_date').filter(is_finished=True).all())
