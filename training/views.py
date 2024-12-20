from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from .models import Feedback, TrainingModule, TrainingProgress
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator

@login_required
def training_modules(request):
    """
    Display available training modules categorized into:
    - Not Started
    - In Progress
    - Completed
    """
    modules = TrainingModule.objects.all()
    user_progress = {
        progress.module_id: progress
        for progress in TrainingProgress.objects.filter(user=request.user)
    }

    categorized_modules = {
        'not_started': [],
        'in_progress': [],
        'completed': [],
    }

    for module in modules:
        progress = user_progress.get(module.id)
        if not progress:
            categorized_modules['not_started'].append(module)
        elif progress.completed:
            categorized_modules['completed'].append((module, progress))
        else:
            categorized_modules['in_progress'].append((module, progress))

    context = {
        'categorized_modules': categorized_modules,
    }
    return render(request, 'trainings/modules.html', context)

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

    # Order videos explicitly by id
    videos = module.videos.all().order_by('id')  # Adjust the field if needed
    paginator = Paginator(videos, 1)  # Show 5 videos per page
    page_number = request.GET.get('page')
    page_videos = paginator.get_page(page_number)

    return render(request, 'trainings/start_training.html', {'module': module, 'videos': page_videos})

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
    """Display available training materials."""
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    training_modules = TrainingModule.objects.all()
    return render(request, 'trainings/materials.html', {'modules': training_modules})

@login_required
def feedback(request):
    """
    Handle training module feedback for affiliates.
    Display submitted feedback and allow new feedback submission.
    """
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    # Retrieve previously submitted feedback by the logged-in user
    submitted_feedback = Feedback.objects.filter(user=request.user).select_related('module')

    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        module_id = request.POST.get('module_id')
        module = get_object_or_404(TrainingModule, id=module_id)

        # Save feedback
        Feedback.objects.create(user=request.user, module=module, text=feedback_text)

        return redirect('feedback')  # Redirect to feedback page after submission

    # Fetch training modules for feedback form
    training_modules = TrainingModule.objects.all()
    
    return render(request, 'trainings/feedback.html', {
        'modules': training_modules,
        'submitted_feedback': submitted_feedback
    })

@staff_member_required
def feedback_list(request):
    """
    View feedback for training modules.
    """
    feedbacks = Feedback.objects.select_related('user', 'module').order_by('-created_at')
    return render(request, 'trainings/feedback_list.html', {'feedbacks': feedbacks})
