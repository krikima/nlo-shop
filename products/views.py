from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product

def product_list(request):
    products = Product.objects.filter(stock__gt=0)  # Только товары с остатком
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        cart = request.session.get('cart', {})
        current_quantity = cart.get(str(product.id), 0)
        
        # Проверка: можно ли добавить ещё один?
        if current_quantity >= product.stock:
            messages.error(request, f"Нельзя добавить больше {product.stock} шт. — столько на складе.")
        else:
            cart[str(product.id)] = current_quantity + 1
            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, f"{product.name} добавлен в корзину!")
        
        return redirect('cart:cart')
    
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    current_quantity = cart.get(str(product_id), 0)

    if current_quantity >= product.stock:
        messages.error(request, f"Нельзя добавить больше {product.stock} шт.")
    else:
        cart[str(product_id)] = current_quantity + 1
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f"Добавлено: {product.name}")

    return redirect('products:product_list')