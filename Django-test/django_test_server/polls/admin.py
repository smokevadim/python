from django.contrib import admin
from polls.models import Question, Choice

# Register your models here.

class ChoiceInLine(admin.StackedInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']})
    ]
    list_display = ['question_text','pub_date','was_published_recently']
    inlines = [ChoiceInLine]
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
