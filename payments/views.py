from decimal import Decimal
import uuid
from django.shortcuts import render
import requests
from affiliates.models import Affiliate
from payments.forms import PayoutRequestForm
from products.models import ProductPurchase, Product
from referrals.models import Referral
from .models import Payment
from django.shortcuts import get_object_or_404, redirect
from .models import Payment
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Sum
from paystackapi.transaction import Transaction
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
import logging
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.http import Http404, FileResponse
import io

logger = logging.getLogger(__name__)


@staff_member_required
def process_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.status = "Paid"
    payment.payment_date = timezone.now()
    payment.save()
    return redirect("admin_dashboard")


@login_required
def payment_history(request):
    """Display the payment history for the affiliate."""
    if request.user.user_type != "affiliate":
        return HttpResponseForbidden("You are not authorized to access this page.")

    payments = Payment.objects.filter(affiliate=request.user.affiliate)
    return render(request, "payments/history.html", {"payments": payments})


@login_required
def wallet_details(request):
    """View wallet details, including earnings and withdrawals."""
    affiliate = request.user.affiliate

    total_earnings = affiliate.calculate_total_earnings()
    total_withdrawn = affiliate.payout_set.aggregate(total=Sum("amount"))["total"] or 0
    wallet_balance = total_earnings - total_withdrawn

    return render(
        request,
        "affiliates/wallet_details.html",
        {
            "total_earnings": total_earnings,
            "total_withdrawn": total_withdrawn,
            "wallet_balance": wallet_balance,
        },
    )


@login_required
def withdraw_request(request):
    """Handle affiliate withdrawal requests."""
    if request.user.user_type != "affiliate":
        return HttpResponseForbidden("You are not authorized to access this page.")

    affiliate = request.user.affiliate
    total_withdrawn = affiliate.payouts.aggregate(total=Sum("amount"))["total"] or 0
    total_earnings = affiliate.calculate_total_earnings()
    wallet_balance = total_earnings - total_withdrawn

    if request.method == "POST":
        form = PayoutRequestForm(request.POST)
        if form.is_valid():
            amount_requested = form.cleaned_data.get("amount")

            # Check if the amount meets the threshold and wallet balance
            if amount_requested < affiliate.payout_threshold:
                form.add_error(
                    "amount", "Amount must be greater than the minimum threshold."
                )
            elif amount_requested > wallet_balance:
                form.add_error(
                    "amount", "Insufficient wallet balance for this withdrawal."
                )
            else:
                payout_request = form.save(commit=False)
                payout_request.affiliate = affiliate
                payout_request.save()
                return redirect(
                    "affiliate_dashboard"
                )  # Redirect to dashboard after submission
    else:
        form = PayoutRequestForm()

    return render(
        request,
        "payments/withdraw_request.html",
        {
            "form": form,
            "affiliate": affiliate,
            "wallet_balance": wallet_balance,
            "total_earnings": total_earnings,
            "total_withdrawn": total_withdrawn,
        },
    )


@login_required
def sales_history(request):
    """Display the sales history for the affiliate."""
    if request.user.user_type != "affiliate":
        return HttpResponseForbidden("You are not authorized to access this page.")

    purchases = ProductPurchase.objects.filter(
        affiliate=request.user.affiliate, is_paid=True
    )
    return render(request, "payments/history.html", {"purchases": purchases})


def initialize_payment(request, product_id):
    """
    Initialize Paystack payment for the selected product.
    This view allows both logged-in and non-logged-in users to initialize payment.
    """
    logger.info(f"Initializing payment for product ID: {product_id}")
    product = get_object_or_404(Product, id=product_id)
    client_email = request.POST.get("email")

    # Validate the client email
    client_email = request.POST.get("email")  # For traditional POST
    if request.content_type == "application/json":
        import json

        body = json.loads(request.body)
        client_email = body.get("email", client_email)

    logger.info(f"Received email: {client_email}")  # Log the email

    if not client_email:
        logger.error("Client email is missing.")
        return JsonResponse({"error": "Email is required for payment."}, status=400)

    # Generate unique reference
    reference = str(uuid.uuid4())

    # Paystack initialization data
    paystack_url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
        "X-CSRFToken": "{{ csrf_token }}",  # Ensure this is included
    }
    data = {
        "email": client_email,
        "amount": int(product.price * 100),  # Convert price to kobo
        "reference": reference,
        "callback_url": request.build_absolute_uri(reverse("payment_callback")),
        "metadata": {
            "product_id": product.id,
            "affiliate_id": request.session.get(
                "ref"
            ),  # Retrieve affiliate ID from session
        },
    }

    # Send initialization request to Paystack
    response = requests.post(paystack_url, json=data, headers=headers)

    if response.status_code == 200:
        try:
            # Create a pending purchase record
            affiliate_id = request.session.get("ref")
            affiliate = Affiliate.objects.filter(id=affiliate_id).first()
            ProductPurchase.objects.create(
                product=product,
                affiliate=affiliate,
                client_email=client_email,
                amount=product.price,
                paystack_reference=reference,  # Store Paystack reference
            )
            return JsonResponse(
                {"payment_url": response.json()["data"]["authorization_url"]}
            )
        except Exception as e:
            logger.error(f"Error saving purchase record: {e}")
            return JsonResponse(
                {"error": "Failed to save purchase record."}, status=500
            )
    else:
        logger.error(f"Paystack initialization failed: {response.json()}")
        return JsonResponse({"error": "Payment initialization failed."}, status=500)


def payment_callback(request):
    """
    Verify Paystack payment and update purchase and referral data.
    """
    reference = request.GET.get("reference")
    logger.info(f"Payment callback received for reference: {reference}")

    if not reference:
        logger.error("Payment reference is missing.")
        return JsonResponse({"error": "Payment reference is required."}, status=400)

    # Verify payment with Paystack
    paystack_url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    response = requests.get(paystack_url, headers=headers)

    if response.status_code == 200:
        data = response.json().get("data", {})
        if data.get("status") == "success":
            try:
                # Retrieve and update the purchase record
                purchase = get_object_or_404(
                    ProductPurchase, paystack_reference=reference
                )
                purchase.is_paid = True
                purchase.save()

                # Store the purchase ID in the session for use in the success view
                request.session["purchase_id"] = purchase.id

                # Handle affiliate commission
                if purchase.affiliate:
                    commission_rate = Decimal(purchase.product.get_commission_rate())
                    affiliate_commission = Decimal(purchase.amount) * commission_rate
                    Referral.objects.create(
                        affiliate=purchase.affiliate,
                        product=purchase.product,
                        client_email=purchase.client_email,
                        commission_earned=affiliate_commission,
                    )

                return redirect("purchase_success")
            except Exception as e:
                logger.error(f"Error processing payment callback: {e}")
                return render(
                    request,
                    "products/payment_failed.html",
                    {"error": "Error processing payment. Please contact support."},
                )
        else:
            logger.error(f"Payment verification failed: {data.get('gateway_response')}")
            return render(
                request,
                "products/payment_failed.html",
                {"error": data.get("gateway_response", "Payment verification failed.")},
            )
    else:
        logger.error("Failed to verify payment with Paystack.")
        return JsonResponse({"error": "Payment verification failed."}, status=500)


@login_required
def verify_payment(request, purchase_id):
    """Verify Paystack payment."""
    purchase = get_object_or_404(ProductPurchase, id=purchase_id)

    # Verify the transaction with Paystack
    response = Transaction.verify(reference=purchase.paystack_reference)

    if response["status"] and response["data"]["status"] == "success":
        # Mark purchase as paid
        purchase.is_paid = True
        purchase.save()

        return redirect("purchase_success")
    else:
        return JsonResponse({"error": "Payment verification failed"}, status=400)


def invoice_download(request, purchase_id):
    """
    Generate and download an invoice for a purchase using ReportLab.
    Allows both logged-in and non-logged-in users to access the invoice.
    """
    try:
        # Retrieve the purchase from the session or directly via the purchase ID
        purchase = ProductPurchase.objects.get(id=purchase_id)

        # Verify that the user is either logged in and owns the purchase or is using the session-provided purchase ID
        if request.user.is_authenticated:
            # Check if the logged-in user matches the client email or is allowed to access the invoice
            if purchase.client_email != request.user.email:
                raise Http404("Unauthorized access to this invoice.")
        else:
            # If the user is not logged in, ensure they are accessing their own purchase via session
            if (
                "purchase_id" not in request.session
                or request.session["purchase_id"] != purchase_id
            ):
                raise Http404("Unauthorized access to this invoice.")

        # Create a buffer to hold the PDF
        buffer = io.BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=letter)

        # Define styles
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        normal_style = styles["BodyText"]

        # Invoice Title
        title = Paragraph("Invoice", title_style)

        # Invoice Details
        details = [
            ["Client Email:", purchase.client_email],
            ["Product Name:", purchase.product.name],
            ["Price:", f"${purchase.product.price}"],
            ["Purchase Date:", purchase.purchased_at.strftime("%Y-%m-%d %H:%M")],
            ["Transaction Reference:", purchase.paystack_reference],
        ]

        # Create a table for details
        details_table = Table(details, hAlign="LEFT")
        details_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        # Footer
        footer = Paragraph(
            "© 2024 Skillsquared Affiliate Management System", normal_style
        )

        # Add elements to PDF
        pdf.build([title, details_table, footer])

        # Generate the PDF
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True, filename=f"invoice_{purchase.id}.pdf"
        )
    except ProductPurchase.DoesNotExist:
        raise Http404("Purchase not found.")
    except Exception as e:
        logger.error(f"Error generating invoice: {str(e)}")
        raise Http404(f"Error generating invoice: {str(e)}")
