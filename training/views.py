from django.shortcuts import render
from .models import TrainingModule
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import TrainingModule, TrainingProgress
from django.utils import timezone
from django.http import HttpResponseForbidden

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

def delete_training_module(request, pk):
    if not request.user.is_superuser:  # Restrict access to superusers
        return HttpResponseForbidden("You are not authorized to perform this action.")
    
    module = get_object_or_404(TrainingModule, pk=pk)
    if request.method == 'POST':
        module.delete()
        return redirect('training_module_list')  # Adjust to your training module list view name

    return render(request, 'training/confirm_delete.html', {'module': module})
