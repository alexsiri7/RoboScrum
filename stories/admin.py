from stories.models import Story, Sprint
from django.contrib import admin


class StoryInline(admin.TabularInline):
    model = Story
    extra = 3

class SprintAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['number', 'start_date', 'is_finished', 'member_dedication']}),
    ]
    inlines = [StoryInline]
    list_display = ('number', 'start_date' )

admin.site.register(Sprint, SprintAdmin)
