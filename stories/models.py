from django.db import models
from django.db.models import Sum

class Sprint(models.Model):
    @classmethod
    def original_velocity(cls):
      return cls.first_sprint().relative_velocity()
    @classmethod
    def first_sprint(cls):
      return Sprint.objects.order_by('number')[0]
    number = models.IntegerField()
    member_dedication = models.IntegerField()
    is_finished = models.BooleanField()
    start_date = models.DateTimeField('date started')
    def __unicode__(self):
      return unicode(self.number)
    def stories(self):
      return self.story_set.order_by('-planned').all()
    def relative_velocity(self):
      return self.velocity()*100/self.member_dedication
    def velocity(self):
      total =  self.story_set.filter(finished=True).filter(planned=True).aggregate(velocity=Sum('estimation'))["velocity"]
      return total if total is not None else 0
    def work_capacity(self):
      total = self.story_set.aggregate(work_capacity=Sum('work_done'))["work_capacity"]
      return total if total is not None else 0
    def burnup(self):
      tot = 0
      burnup = []
      vel_map = self.day_velocity_map()
      for e in range(5):
        tot += vel_map.get(e, 0)
        burnup.append( tot)
      return burnup
    def day_velocity(self):
      return self.story_set.filter(finished=True).filter(planned=True).values('finished_day').annotate(velocity=Sum('estimation'))
    def day_velocity_map(self):
      ret = dict()
      for i in self.day_velocity():
        ret[i["finished_day"]] = i["velocity"]
      return ret
    def total_commitment(self):
      total = self.story_set.aggregate(totalCommitment=Sum('estimation'))["totalCommitment"]
      return total if total is not None else 0
    def original_commitment(self):
      total= self.story_set.filter(planned=True).aggregate(totalCommitment=Sum('estimation'))["totalCommitment"]
      return total if total is not None else 0
    def adopted_commitment(self):
      return self.story_set.filter(planned=False).aggregate(totalCommitment=Sum('estimation'))["totalCommitment"]
    def focus_factor(self):
      wc = self.work_capacity()
      return self.velocity()*100/self.work_capacity() if wc > 0 else 0
    def adopted_work(self):
      return self.adopted_commitment()*100/self.original_commitment()
    def found_points(self):
      points = self.story_set.aggregate(totalWork=Sum('work_done'), totalCommitment=Sum('estimation'))
      return points["totalWork"]-points["totalCommitment"]
    def found_work(self):
      return self.found_points()*100/self.original_commitment()
    def targeted_value_increase(self):
      return self.relative_velocity()*100/Sprint.original_velocity()
    def estimate_delta(self):
      stories = self.story_set.filter(planned=True, finished=True)
      diff = 0
      for s in stories:
        diff = diff + abs(s.work_done - s.estimation)
      return diff
    def accuracy_of_estimation(self):
        return 100-(self.estimate_delta()*100/self.total_commitment())
    def accuracy_of_commit(self):
        return 100-abs(self.work_capacity()-self.original_commitment())*100/self.work_capacity()

class Story(models.Model):
    sprint = models.ForeignKey(Sprint)
    title = models.CharField(max_length=200)
    planned = models.BooleanField(default=True)
    estimation = models.IntegerField()
    work_done = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)
    finished_day = models.IntegerField(default=0)
    def is_win(self):
       return self.finished and self.planned and abs(self.estimation-self.work_done)<3 or (abs(self.estimation-self.work_done)/min(self.estimation,self.work_done)<0.2 if min(self.estimation,self.work_done)>0 else False)
