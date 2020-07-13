def cart(request):
    basket = []
    if request.user.is_authenticated:
        basket = request.user.basket.all()
    return {
       'cart': basket,
    }
