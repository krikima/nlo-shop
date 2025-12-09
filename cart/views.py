from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .utils import get_cart, update_cart_quantity, remove_from_cart
from products.models import Product
from orders.models import Order, OrderItem
from orders.telegram_bot import send_order_to_admin

def view_cart(request):
    cart = get_cart(request)
    if not cart:
        return render(request, 'cart.html', {'cart_items': [], 'total': 0})

    cart_items = []
    total = 0
    for product_id, qty in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * qty
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal
            })
        except Product.DoesNotExist:
            continue

    delivery_cost = 100 if total < 300 else 0
    total_with_delivery = total + delivery_cost

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'delivery_cost': delivery_cost,
        'total_with_delivery': total_with_delivery
    })

def checkout(request):
    cart = get_cart(request)
    if not cart:
        return redirect('products:product_list')

    total = sum(Product.objects.get(id=k).price * v for k, v in cart.items())
    delivery_cost = 100 if total < 300 else 0
    final_total = total + delivery_cost

    if request.method == "POST":
        order = Order.objects.create(
            first_name=request.POST['first_name'],
            phone=request.POST['phone'],
            address=request.POST.get('address', ''),
            delivery_type=request.POST['delivery_type'],
            total_price=final_total,
            telegram_username=request.POST.get('telegram_username', 'не указан')
        )
        for product_id, qty in cart.items():
            try:
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price=product.price
                )
            except Product.DoesNotExist:
                continue

        send_order_to_admin(order)
        if 'cart' in request.session:
            del request.session['cart']

        return redirect('orders:order_success', order_id=order.id)

    return render(request, 'checkout.html', {'final_total': final_total})

def update_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    quantity = cart.get(str(product_id), 1)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "increase":
            # Проверка: можно ли добавить?
            if quantity < product.stock:
                quantity += 1
            else:
                messages.error(request, f"Нельзя добавить больше {product.stock} шт.")
        elif action == "decrease" and quantity > 1:
            quantity -= 1

        cart[str(product_id)] = quantity
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart:cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart:cart')