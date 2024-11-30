from django.db import models
from affiliates.models import Affiliate

class TrainingModule(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    completion_time = models.PositiveIntegerField(help_text="Time in minutes")  # Estimated time
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TrainingProgress(models.Model):
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.affiliate.user.username} - {self.module.title}"
