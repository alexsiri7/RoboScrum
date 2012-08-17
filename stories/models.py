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
    def relative_velocity(self):
      return self.velocity()*100/self.member_dedication
    def velocity(self):
      return self.story_set.filter(finished=True).filter(planned=True).aggregate(velocity=Sum('estimation'))["velocity"]
    def work_capacity(self):
      return self.story_set.aggregate(work_capacity=Sum('work_done'))["work_capacity"]
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
      return self.story_set.aggregate(totalCommitment=Sum('estimation'))["totalCommitment"]
    def original_commitment(self):
      return self.story_set.filter(planned=True).aggregate(totalCommitment=Sum('estimation'))["totalCommitment"]
    def adopted_commitment(self):
      return self.story_set.filter(planned=False).aggregate(totalCommitment=Sum('estimation'))["totalCommitment"]
    def focus_factor(self):
      return self.velocity()*100/self.work_capacity()
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
      points = self.story_set.filter(planned=True).aggregate(totalWork=Sum('work_done'), totalCommitment=Sum('estimation'))
      return abs(points["totalWork"]-points["totalCommitment"])
    def accuracy_of_estimation(self):
        return 100-(self.estimate_delta()*100/self.total_commitment())
    def accuracy_of_commit(self):
        return 100-abs(self.work_capacity()-self.original_commitment())*100/self.work_capacity()

class Story(models.Model):
    sprint = models.ForeignKey(Sprint)
    title = models.CharField(max_length=200)
    planned = models.BooleanField()
    estimation = models.IntegerField()
    work_done = models.IntegerField()
    finished = models.BooleanField()
    finished_day = models.IntegerField()
