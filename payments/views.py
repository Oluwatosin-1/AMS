from django.shortcuts import render
from .models import Payment
from django.shortcuts import get_object_or_404, redirect
from .models import Payment
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@staff_member_required
def process_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.status = 'Paid'
    payment.payment_date = timezone.now()
    payment.save()
    return redirect('admin_dashboard')

@login_required
def payment_history(request):
    """Display the payment history for the affiliate."""
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")

    payments = Payment.objects.filter(affiliate=request.user.affiliate)
    return render(request, 'payments/history.html', {'payments': payments})
