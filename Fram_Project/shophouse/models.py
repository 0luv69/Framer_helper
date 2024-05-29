from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

# Create your models here.


class CustomUser(models.Model):
    user_m = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to='profile_pic', null=True, blank=True)
    ph_num = models.ImageField(null=True)




class FramerUser(models.Model):
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Bio= models.TextField(default='Hey, I am Framer Here')
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    trust_rate = models.IntegerField(choices=RATING_CHOICES, default=5)
    def __str__(self):
        return self.user_m

class BuyerUser(models.Model):
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.user_m
    

class Categories(models.Model):
    slug = models.SlugField(unique=True, null=True, blank=True)
    categories_name=  models.CharField(max_length=100)
    discription = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.categories_name)
        super(Categories, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Product(models.Model):
    slug = models.SlugField(unique=True, null=True, blank=True)
    categories= models.ForeignKey(Categories, on_delete=models.CASCADE)
    framer_user= models.ForeignKey(FramerUser, on_delete=models.CASCADE)
    title= models.CharField(max_length=100)
    price= models.FloatField()
    discription = models.TextField()
    on_sale = models.BooleanField(default=False)
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    Rate= models.IntegerField(choices=RATING_CHOICES,  default=5)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product') 
    alt_text= models.CharField(max_length=100)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    STATUS_CHOICES = (
        ('cart', 'In Cart'),
        ('purchased', 'Purchased'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart Item: {self.product.title}"
    


class CheckOutInfo(models.Model):
    user = models.ForeignKey(BuyerUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)

    s_ph_num = models.CharField(max_length=20)
    s_email = models.EmailField()

    Order_Notes=  models.CharField(max_length=350, null=True, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)



    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipping Info for {self.user.username}"



# to track the shiping product
class ShippingInfo(models.Model):
    checkout_info = models.ForeignKey(CheckOutInfo, on_delete=models.CASCADE)

    PAYMENT_OPTIONS = [('cash_payment', 'Cash Payment'),]
    payment_option = models.CharField(max_length=20, choices=PAYMENT_OPTIONS, default='cash_payment')

    shipping_number= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ordered_Date= models.DateField(auto_now_add=True)
    deliver_Date_on= models.DateField(null=True)
    recived_items= models.BooleanField(default=False)
    paid_money= models.BooleanField(default=False)


