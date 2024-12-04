from django.contrib import admin
from .models import TrainingModule, TrainingProgress, Feedback


@admin.register(TrainingModule)
class TrainingModuleAdmin(admin.ModelAdmin):
    """
    Admin configuration for the TrainingModule model.
    """
    list_display = ('title', 'completion_time', 'created_at', 'has_material')
    search_fields = ('title',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

    def has_material(self, obj):
        """
        Check if the training module has associated material.
        """
        return bool(obj.material)
    has_material.boolean = True
    has_material.short_description = 'Has Material'


@admin.register(TrainingProgress)
class TrainingProgressAdmin(admin.ModelAdmin):
    """
    Admin configuration for the TrainingProgress model.
    """
    list_display = ('user_username', 'module_title', 'completed', 'completion_date', 'admin_verified')
    list_filter = ('completed', 'admin_verified', 'completion_date')
    search_fields = ('user__username', 'module__title')
    readonly_fields = ('completion_date',)

    def user_username(self, obj):
        """
        Display the username of the user.
        """
        return obj.user.username
    user_username.short_description = "User"

    def module_title(self, obj):
        """
        Display the title of the training module.
        """
        return obj.module.title
    module_title.short_description = "Module"


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Feedback model.
    """
    list_display = ('user_username', 'module_title', 'text_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'module__title', 'text')

    def user_username(self, obj):
        """
        Display the username of the user who provided the feedback.
        """
        return obj.user.username
    user_username.short_description = "User"

    def module_title(self, obj):
        """
        Display the title of the training module for which feedback was provided.
        """
        return obj.module.title
    module_title.short_description = "Module"

    def text_preview(self, obj):
        """
        Display a preview of the feedback text.
        """
        return obj.text[:50] + ("..." if len(obj.text) > 50 else "")
    text_preview.short_description = "Feedback"
