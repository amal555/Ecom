from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomCustomersManager(BaseUserManager):
    def create_user(self,username,name, email,password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            name = name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            name = name
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user





class Customers(AbstractBaseUser):
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=50, unique=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    objects = CustomCustomersManager()

    def __str__(self):
        return self.name

# class Products(models.Model):
#     customers = models.ForeignKey("Customers", on_delete=models.CASCADE,related_name='products')
#     products_user = models.ForeignKey("User", on_delete=models.CASCADE,related_name="user_products",null=True)
    
#     # user_cust
#     products_name = models.CharField(max_length=200)
#     created_date = models.DateTimeField(auto_now_add=True)
#     image_data = models.TextField()
#     description = models.TextField()
#     discount = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     is_active = models.BooleanField(default=True)

class Productss(models.Model):
    customers = models.ForeignKey("Customers", on_delete=models.CASCADE,related_name='productss')
    products_user = models.ForeignKey("User", on_delete=models.CASCADE,related_name="user_productss",null=True)
    
    # user_cust
    products_name = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    image_data = models.TextField()
    description = models.TextField()
    discount = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
class User(models.Model):
    customers_user = models.ForeignKey("Customers", on_delete=models.CASCADE,related_name='user_cust')
    # products_user = models.ForeignKey("Products", on_delete=models.CASCADE,related_name='user_products',null=True)
    customer_name = models.CharField(max_length=200)
    customers_address = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
