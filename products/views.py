from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Vote

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)

def product_vote(request, product_id):
    if request.method == 'POST' and request.user.is_authenticated:
        vote_type = request.POST.get('vote_type')
        product = get_object_or_404(Product, id=product_id)

        # Determine vote value based on the vote type
        vote_value = 1 if vote_type == 'up' else -1

        # Check if the user has already voted for this product
        existing_vote = Vote.objects.filter(product=product, user=request.user).first()

        if existing_vote:
            # Update the existing vote
            existing_vote.vote = vote_value
            existing_vote.save()
        else:
            # Create a new vote
            Vote.objects.create(product=product, user=request.user, vote=vote_value)

        return redirect('products')  # Redirect to the product list or the specific product page

    return redirect('products')  # Redirect if not authenticated or not a POST request