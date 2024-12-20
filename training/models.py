from django.db import models
from django.conf import settings


class TrainingVideo(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class TrainingModule(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    material = models.FileField(upload_to='training_materials/', null=True, blank=True)
    videos = models.ManyToManyField(TrainingVideo, blank=True)
    completion_time = models.PositiveIntegerField(help_text="Time in minutes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TrainingProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='training_progress'
    )
    module = models.ForeignKey(
        TrainingModule,
        on_delete=models.CASCADE,
        related_name='training_progress'
    )
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    admin_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.module.title} - {'Completed' if self.completed else 'Incomplete'}"

class Feedback(models.Model):
    """
    Model to store feedback for training modules.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="feedbacks"
    )
    module = models.ForeignKey(
        'TrainingModule',
        on_delete=models.CASCADE,
        related_name="feedbacks"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.module.title}"
