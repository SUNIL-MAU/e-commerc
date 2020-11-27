# Django E-commerce website

This is e-commerce website built with Django.

# Project Summary
This website displays products. Users can add and remove products to their cart while also specifying the quantity of each item. They can then enter their address and phone number, choose Stripe to handle the payment processing. Here admin can create category, products and here in order to add product to their cart user have to login, to do this i have user django custom  middleware and in this project i did not user single line of javascript because i want to make it without javascript.

## Website home page

![Website home page](Images/Home%20screen.png "Website home page")

## Website login page


![](Images/Login%20Screen.png "Website login page")

## Website cart page

![](Images/Card%20Process.png "Website cart page")

## Website cart summary page

![](Images/Order%20Summery.png "Website cart summary page")

## Website cart item page

![](Images/cart%20Item.png "Website cart item page")

## Website cheakout detail page

![](Images/checkout%20details%20screen.png "Website cheakout detail page")


# Installation

`pip install django`

`pip install -r requirement.txt`

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py runserver`

# For Admin Login

```
python manage.py createsuperuser

Username:admin
Password:admin
```




