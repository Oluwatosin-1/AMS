from django.contrib import admin
from .models import TrainingModule, TrainingProgress

@admin.register(TrainingModule)
class TrainingModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'completion_time', 'created_at')
    search_fields = ('title',)
    ordering = ('created_at',) 

@admin.register(TrainingProgress)
class TrainingProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'completed', 'completion_date')  # Replace module_name with module
    list_filter = ('completed', 'completion_date')
    search_fields = ('user__username', 'module__title')