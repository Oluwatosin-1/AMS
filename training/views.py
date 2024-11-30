from django.shortcuts import render
from .models import TrainingModule
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import TrainingModule, TrainingProgress
from django.utils import timezone

@login_required
def complete_training_module(request, module_id):
    module = get_object_or_404(TrainingModule, id=module_id)
    affiliate = request.user.affiliate
    progress, created = TrainingProgress.objects.get_or_create(
        affiliate=affiliate, module=module
    )
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save()
    return redirect('training_modules')

def training_modules(request):
    modules = TrainingModule.objects.all()
    return render(request, 'training/modules.html', {'modules': modules})
