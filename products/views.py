from django.shortcuts import render, redirect
from .forms import ProductForm 
from django.shortcuts import render
from .models import Product, AffiliateProductLink, ProductPurchase
from affiliates.models import Affiliate

def generate_affiliate_links(request):
    products = Product.objects.all()
    affiliate = request.user.affiliate  # Assuming logged-in user is an affiliate
    links = []
    for product in products:
        link, created = AffiliateProductLink.objects.get_or_create(
            affiliate=affiliate, product=product,
            defaults={'unique_url': f'/products/{product.id}/?ref={affiliate.id}'}
        )
        links.append(link)
    return render(request, 'products/affiliate_links.html', {'links': links})

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/create_product.html', {'form': form})


def purchase_product(request, product_id):
    product = Product.objects.get(id=product_id)
    ref = request.session.get('ref')
    affiliate = Affiliate.objects.get(id=ref) if ref else None

    if request.method == 'POST':
        client_email = request.POST['email']
        ProductPurchase.objects.create(
            product=product,
            affiliate=affiliate,
            client_email=client_email,
            amount=product.price
        )
        return render(request, 'products/purchase_success.html', {'product': product})
    return render(request, 'products/purchase_form.html', {'product': product})
