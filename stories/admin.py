from stories.models import Story, Sprint
from django.contrib import admin


class StoryInline(admin.TabularInline):
    model = Story
    extra = 3

class NewStoryInline(admin.TabularInline):
    model = Story
    extra = 20
    fields = ['title','estimation']

class SprintAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None,               {'fields': ['number', 'start_date', 'member_dedication']}),
#    ]
    inlines = [StoryInline]
    list_display = ('number', 'start_date' )
    def get_form(self, request, obj=None, **kwargs):
      if obj is None: # obj is not None, so this is a change page
         self.exclude = ['is_finished']
         self.inlines = [NewStoryInline]
#	 kwargs['inlines'] = [StoryInline]
 #     else: # obj is None, so this is an add page
 #        kwargs['fields'].add('is_finished')
      return super(SprintAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Sprint, SprintAdmin)
