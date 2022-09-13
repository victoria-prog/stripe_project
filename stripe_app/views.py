
import os
import stripe
from dotenv import load_dotenv
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect

from .forms import ItemForm
from .models import Item
from django.views.decorators.http import require_http_methods
from cart.cart import Cart

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
    is_in_cart = pk in ids_in_cart(request)
    return render(
        request, 'stripe_app/item.html', {'item': item, 'in_cart': is_in_cart}
    )


def cart_add(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Item, pk=pk)
    ids = ids_in_cart(request)
    if pk not in ids:
        cart.add(product=product)
    return redirect(reverse_lazy('stripe_app:get_item', args=[pk]))


def ids_in_cart(request):
    cart = Cart(request)
    return [value['product_id']for key, value in cart.session['cart'].items()]


def item_clear(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Item, pk=pk)
    cart.remove(product)
    return redirect(reverse_lazy('stripe_app:cart_detail'))


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect(reverse_lazy('stripe_app:cart_detail'))


def cart_detail(request):
    context = {}
    total_price = 0
    items = list_items(request)
    for item in items:
        total_price += item.get_price()
        request.session['cart'].get(str(item.pk))['price'] = item.get_price()
    if items.exists():
        context['currency'] = items.first().currency
        context['total_price'] = total_price
    return render(request, 'stripe_app/cart_detail.html', context)


@require_http_methods(['POST'])
def create_checkout_session(request):
    items = list_items(request)
    if items.exists():
        session = stripe.checkout.Session.create(
            line_items=get_items(items),
            mode='payment',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/canceled/',
        )
        return redirect(session.url, code=303)
    message = 'You should add at least one item to your busket.'
    return render(request, 'stripe_app/cart_detail.html', {'message': message})


def list_items(request):
    list_items = []
    for key in request.session['cart']:
        list_items.append(request.session['cart'][key]['product_id'])
    return Item.objects.filter(pk__in=list_items)


def get_items(items):
    cart = []
    for item in items:
        cart += [{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                    'images': ['item.image']
                },
                'unit_amount': item.get_price(),
                },
            'quantity': 1,
        }]
    return cart


def success(request):
    return render(request, 'stripe_app/success.html')


def canceled(request):
    return render(request, 'stripe_app/canceled.html')

