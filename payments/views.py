from django.shortcuts import render
from .models import Payment
from django.shortcuts import get_object_or_404, redirect
from .models import Payment
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

@staff_member_required
def process_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.status = 'Paid'
    payment.payment_date = timezone.now()
    payment.save()
    return redirect('admin_dashboard')

def payment_history(request):
    payments = Payment.objects.filter(affiliate=request.user.affiliate)
    return render(request, 'payments/history.html', {'payments': payments})
