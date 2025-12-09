def cart_items_count(request):
    cart = request.session.get('cart', {})
    count = sum(cart.values())
    return {'cart_items_count': count}
