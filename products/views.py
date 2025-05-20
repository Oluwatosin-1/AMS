import uuid
from django.shortcuts import render, redirect
from .forms import ProductForm
from django.shortcuts import render
from .models import Product, AffiliateProductLink, ProductPurchase
from affiliates.models import Affiliate
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from .models import Product, ProductPurchase, AffiliateProductLink
from .forms import ProductForm
from affiliates.models import Affiliate
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.conf import settings
from decimal import Decimal  # Import Decimal
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, FormView, View
import requests


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"

    def get_template_names(self):
        """
        Dynamically select the template based on user type.
        """
        if self.request.user.is_authenticated:
            if self.request.user.user_type == "affiliate":
                return "products/product_detail_affiliate.html"
        return "products/product_detail_buyer.html"

    def get_context_data(self, **kwargs):
        """
        Add additional context to the template.
        """
        context = super().get_context_data(**kwargs)

        # Check for referral ID in the GET parameters
        ref = self.request.GET.get("ref")
        if ref:
            self.request.session["ref"] = ref  # Store in session for tracking
            try:
                affiliate = Affiliate.objects.get(id=ref)
                context["affiliate_name"] = (
                    affiliate.user.get_full_name()
                )  # Assuming 'user' has first_name and last_name
            except Affiliate.DoesNotExist:
                context["affiliate_name"] = None

        context["affiliate_ref"] = ref

        # Include affiliate-specific information if applicable
        if (
            self.request.user.is_authenticated
            and self.request.user.user_type == "affiliate"
        ):
            affiliate = self.request.user.affiliate
            try:
                link = affiliate.affiliateproductlink_set.get(product=self.object)
                context["affiliate_link"] = link.unique_url
            except AffiliateProductLink.DoesNotExist:
                context["affiliate_link"] = None

            # Calculate commission based on the product's rate
            product = self.object
            commission_rate = Decimal(
                product.get_commission_rate()
            )  # Convert to Decimal
            context["affiliate_commission"] = product.price * commission_rate

        return context

    def post(self, request, *args, **kwargs):
        """
        Handle purchase form submission and initialize Paystack payment.
        """
        product = self.get_object()
        ref = self.request.session.get("ref")
        affiliate = Affiliate.objects.filter(id=ref).first() if ref else None

        # Generate a unique reference for the payment
        reference = str(uuid.uuid4())

        # Capture buyer's email
        client_email = request.POST.get("email")
        if not client_email:
            messages.error(request, "Email is required to proceed with payment.")
            return self.render_to_response(self.get_context_data())

        # Save the purchase record
        purchase = ProductPurchase.objects.create(
            product=product,
            affiliate=affiliate,
            client_email=client_email,
            amount=product.price,
            paystack_reference=reference,  # Store Paystack reference
        )

        # Initialize Paystack payment
        paystack_url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email": client_email,
            "amount": int(product.price * 100),  # Convert to kobo
            "reference": reference,
            "callback_url": request.build_absolute_uri(reverse("payment_callback")),
            "metadata": {
                "product_id": product.id,
                "affiliate_id": affiliate.id if affiliate else None,
                "purchase_id": purchase.id,
            },
        }

        # Make the API request to Paystack
        response = requests.post(paystack_url, json=data, headers=headers)

        if response.status_code == 200:
            # Redirect to Paystack payment page
            return redirect(response.json()["data"]["authorization_url"])
        else:
            # Log and handle errors appropriately
            error_message = response.json().get(
                "message", "Payment initialization failed."
            )
            messages.error(request, error_message)
            purchase.delete()  # Clean up the purchase record if initialization fails
            return render(
                request, "products/payment_failed.html", {"error": error_message}
            )


class ProductPurchaseView(FormView):
    template_name = "products/purchase_form.html"
    form_class = ProductForm

    def form_valid(self, form):
        product = get_object_or_404(Product, id=self.kwargs["product_id"])
        ref = self.request.session.get("ref")
        affiliate = Affiliate.objects.get(id=ref) if ref else None

        ProductPurchase.objects.create(
            product=product,
            affiliate=affiliate,
            client_email=form.cleaned_data["email"],
            amount=product.price,
        )
        return redirect("purchase_success")


@login_required
def generate_affiliate_link(request, product_id):
    """Generate a unique affiliate link with the domain name."""
    if request.user.user_type != "affiliate":
        return HttpResponseForbidden("You are not authorized to access this page.")

    affiliate = request.user.affiliate
    product = get_object_or_404(Product, id=product_id)

    # Ensure the link does not already exist
    link, created = AffiliateProductLink.objects.get_or_create(
        affiliate=affiliate, product=product
    )

    if created:
        # Add the domain dynamically to the unique URL
        link.unique_url = f"{settings.SITE_DOMAIN}{reverse('product_detail', args=[product.id])}?ref={affiliate.id}"
        link.save()

    return redirect("affiliate_links")


def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "products/create_product.html", {"form": form})


class PurchaseSuccessView(View):
    def get(self, request, *args, **kwargs):
        # Retrieve the purchase_id from the session
        purchase_id = request.session.get("purchase_id")

        if not purchase_id:
            return render(
                request,
                "products/payment_failed.html",
                {"error": "Purchase not found."},
            )

        # Fetch the purchase object
        purchase = get_object_or_404(ProductPurchase, id=purchase_id)
        product = purchase.product

        # Pass the purchase and product details to the template
        context = {
            "purchase": purchase,
            "product": product,
        }
        return render(request, "products/purchase_success.html", context)


# Store View
@login_required
def store(request):
    if request.user.user_type != "affiliate":
        return HttpResponseForbidden("You are not authorized to access this page.")

    affiliate = request.user.affiliate
    products = Product.objects.all()

    for product in products:
        # Generate affiliate link dynamically
        try:
            link = AffiliateProductLink.objects.get(
                affiliate=affiliate, product=product
            )
            product.affiliate_link = link.unique_url
        except AffiliateProductLink.DoesNotExist:
            product.affiliate_link = None

    return render(
        request,
        "products/store.html",
        {
            "products": products,
            "product_categories": Product.CATEGORY_CHOICES,
            "selected_category": request.GET.get("category"),
            "search_query": request.GET.get("search", ""),
        },
    )
