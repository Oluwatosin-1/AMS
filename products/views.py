from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from referrals.models import Referral
from .forms import ProductForm 
from django.shortcuts import render
from .models import Product, AffiliateProductLink, ProductPurchase
from affiliates.models import Affiliate
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.generic import DetailView
from django.views.generic import DetailView, FormView
from django.shortcuts import redirect
from .models import Product, ProductPurchase, AffiliateProductLink
from .forms import ProductForm
from affiliates.models import Affiliate
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.conf import settings


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ref = self.request.GET.get('ref')  # Capture referral ID from URL
        if ref:
            self.request.session['ref'] = ref  # Store in session for tracking
        context['affiliate_ref'] = ref
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        ref = self.request.session.get('ref')
        affiliate = Affiliate.objects.filter(id=ref).first() if ref else None

        # Handle product purchase and affiliate tracking
        client_email = request.POST.get('email')
        purchase = ProductPurchase.objects.create(
            product=product,
            affiliate=affiliate,
            client_email=client_email,
            amount=product.price
        )

        # Calculate and assign commission
        if affiliate:
            commission_rate = product.get_commission_rate()  # Assume a method on Product
            affiliate_commission = purchase.amount * commission_rate
            Referral.objects.create(
                affiliate=affiliate,
                product=product,
                client_email=client_email,
                commission_earned=affiliate_commission
            )

        return redirect('purchase_success')  # Redirect to a success page


class ProductPurchaseView(FormView):
    template_name = 'products/purchase_form.html'
    form_class = ProductForm

    def form_valid(self, form):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        ref = self.request.session.get('ref')
        affiliate = Affiliate.objects.get(id=ref) if ref else None

        ProductPurchase.objects.create(
            product=product,
            affiliate=affiliate,
            client_email=form.cleaned_data['email'],
            amount=product.price
        )
        return redirect('purchase_success')



@login_required
def generate_affiliate_link(request, product_id):
    """Generate a unique affiliate link with the domain name."""
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")

    affiliate = request.user.affiliate
    product = get_object_or_404(Product, id=product_id)

    # Ensure the link does not already exist
    link, created = AffiliateProductLink.objects.get_or_create(
        affiliate=affiliate,
        product=product
    )

    if created:
        # Add the domain dynamically to the unique URL
        link.unique_url = f"{settings.SITE_DOMAIN}{reverse('product_detail', args=[product.id])}?ref={affiliate.id}"
        link.save()

    return redirect('affiliate_links')

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/create_product.html', {'form': form})

class PurchaseSuccessView(TemplateView):
    template_name = 'products/purchase_success.html'
