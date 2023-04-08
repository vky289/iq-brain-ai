from django.contrib import admin
from app.core.models import Questions, Answers, Stats


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'question',
        'iq_index',
        'created_date'
    )


class AnswersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'questions',
        'option',
        'correct',
        'created_date'
    )


class StatsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'age',
        'iq_score',
        'created_date',
        'session_id'
    )


admin.site.register(Questions, QuestionAdmin)
admin.site.register(Answers, AnswersAdmin)
admin.site.register(Stats, StatsAdmin)

