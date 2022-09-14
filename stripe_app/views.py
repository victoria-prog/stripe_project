import os
from django.http import JsonResponse
import stripe
from dotenv import load_dotenv
from django.shortcuts import get_object_or_404, render
from .models import Item
from .forms import ItemForm


load_dotenv()


stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


def index(request):
    context = {}
    items = Item.objects.all()
    context['items'] = items
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            cur_currency = form.cleaned_data['currency']
            Item.objects.update(currency=cur_currency)
    else:
        form = ItemForm()
    context['form'] = form
    return render(request, 'stripe_app/index.html', context)


def get_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'stripe_app/item.html', {'item': item})


def create_checkout_session(request, pk):
    item = get_object_or_404(Item, pk=pk)
    remote_domain = 'http://34.159.119.247'
    session = stripe.checkout.Session.create(
        line_items=[
            {'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                    'images': [remote_domain + item.image.url],
                },
                'unit_amount': item.get_price(),
            },
                'quantity': 1}],
        mode='payment',
        success_url=remote_domain + '/success/',
        cancel_url=remote_domain + '/canceled/',
        )
    return JsonResponse({'id': session.id})


def success(request):
    return render(request, 'stripe_app/success.html')


def canceled(request):
    return render(request, 'stripe_app/canceled.html')
