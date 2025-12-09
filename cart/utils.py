def get_cart(request):
    return request.session.get('cart', {})

def add_to_cart(request, product_id, quantity=1):
    cart = get_cart(request)
    cart[str(product_id)] = cart.get(str(product_id), 0) + int(quantity)
    request.session['cart'] = cart

def remove_from_cart(request, product_id):
    cart = get_cart(request)
    cart.pop(str(product_id), None)
    request.session['cart'] = cart

def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']

def update_cart_quantity(request, product_id, quantity):
    cart = get_cart(request)
    if str(product_id) in cart:
        if quantity <= 0:
            cart.pop(str(product_id))
        else:
            cart[str(product_id)] = quantity
    request.session['cart'] = cart