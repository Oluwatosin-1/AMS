from django.contrib import admin
from .models import TrainingModule, TrainingProgress

@admin.register(TrainingModule)
class TrainingModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'completion_time', 'created_at')
    search_fields = ('title',)
    ordering = ('created_at',)

@admin.register(TrainingProgress)
class TrainingProgressAdmin(admin.ModelAdmin):
    list_display = ('affiliate', 'module', 'completed', 'completed_at')
    list_filter = ('completed',)
    search_fields = ('affiliate__user__username', 'module__title')
    ordering = ('completed_at',)
