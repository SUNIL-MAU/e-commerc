from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product,cart):
    keys = cart.keys()
    # print('product',product)
    # print('cart',cart)
    for id in keys:
      
        if int(id) == product.id:
            return True

    return False


@register.filter(name='cart_quantity')
def cart_quantity(product,cart):
    keys = cart.keys()
    # print('keys--', keys)
    # print('product----- ', product)
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)

    return 0    



@register.filter(name='price_total')
def prince_total(product,cart):
    # print(cart)
    # print(product)
    return product.price * cart_quantity(product,cart)  

@register.filter(name='totel_cart_price')
def totel_cart_price(products, cart):
    sum = 0
    for p in products:
        sum += prince_total(p, cart)

    return sum    

@register.filter(name='multiply')
def multiply(number, number1):

    return number*number1  

@register.filter(name='cart_length')
def cart_length(leg):
    car = len(leg)

    return car