from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from .models import TrainingModule, TrainingProgress


@login_required
def training_modules(request):
    """Display available training modules with progress status."""
    modules = TrainingModule.objects.all()
    progress_mapping = {
        module: TrainingProgress.objects.filter(user=request.user, module=module).first()
        for module in modules
    }

    return render(request, 'trainings/modules.html', {
        'modules': modules,
        'progress_mapping': progress_mapping
    })


@login_required
def start_training(request, module_id):
    """Start training for a specific module."""
    module = get_object_or_404(TrainingModule, id=module_id)
    progress, created = TrainingProgress.objects.get_or_create(
        user=request.user,
        module=module
    )

    if progress.completed:
        return redirect('training_modules')  # Already completed

    return render(request, 'trainings/start_training.html', {'module': module})


@login_required
def complete_training_module(request, module_id):
    """Mark a training module as completed."""
    module = get_object_or_404(TrainingModule, id=module_id)
    progress, created = TrainingProgress.objects.get_or_create(
        user=request.user,
        module=module
    )
    progress.completed = True
    progress.completion_date = now()
    progress.save()
    return redirect('training_modules')


@login_required
def verify_training_completion(request, progress_id):
    """Admin verifies training completion."""
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only admins can verify training completions.")

    progress = get_object_or_404(TrainingProgress, id=progress_id)
    if request.method == 'POST':
        progress.admin_verified = True
        progress.save()
        return redirect('admin_training_verifications')

    return render(request, 'trainings/verify_completion.html', {'progress': progress})

def delete_training_module(request, pk):
    if not request.user.is_superuser:  # Restrict access to superusers
        return HttpResponseForbidden("You are not authorized to perform this action.")
    
    module = get_object_or_404(TrainingModule, pk=pk)
    if request.method == 'POST':
        module.delete()
        return redirect('training_module_list')  # Adjust to your training module list view name

    return render(request, 'training/confirm_delete.html', {'module': module})
 
 # Training Materials View
@login_required
def training_materials(request):
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")
    training_modules = TrainingModule.objects.all()
    return render(request, 'trainings/materials.html', {'modules': training_modules})

@login_required
def feedback(request):
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")
    training_modules = TrainingModule.objects.all()
    return render(request, 'trainings/feedback.html', {'modules': training_modules})
