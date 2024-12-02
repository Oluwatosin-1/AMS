from django.shortcuts import render

from payments.forms import PayoutRequestForm
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

@login_required
def wallet_details(request):
    """View wallet details, including earnings and withdrawals."""
    affiliate = request.user.affiliate

    total_earnings = affiliate.calculate_total_earnings()
    total_withdrawn = affiliate.payout_set.aggregate(total=Sum('amount'))['total'] or 0
    wallet_balance = total_earnings - total_withdrawn

    return render(request, 'affiliates/wallet_details.html', {
        'total_earnings': total_earnings,
        'total_withdrawn': total_withdrawn,
        'wallet_balance': wallet_balance,
    })


@login_required
def withdraw_request(request):
    """Handle affiliate withdrawal requests."""
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    affiliate = request.user.affiliate

    if request.method == 'POST':
        form = PayoutRequestForm(request.POST)
        if form.is_valid():
            payout_request = form.save(commit=False)
            payout_request.affiliate = affiliate
            payout_request.save()
            return redirect('affiliate_dashboard')  # Redirect to the dashboard after submission
    else:
        form = PayoutRequestForm()

    return render(request, 'payments/withdraw_request.html', {'form': form})
