from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# Create your models here.

class CustomerManager(BaseUserManager):
    # def create_user(self, email, name, phone_number, password):
    #     if not email:
    #         raise ValueError('Users must have an email address')
    #     if not name:
    #         raise ValueError('Users must have a name')
    #     if not phone_number:
    #         raise ValueError('Users must have a phone number')

    #     user = self.model(
    #         email=self.normalize_email(email),
    #         name=name,
    #         phone_number=phone_number
    #     )

    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user
    
    # def create_superuser(self, email, name, phone_number, password):
    #     user = self.create_user(
    #         email=email,
    #         name=name,
    #         phone_number=phone_number,
    #         password=password,
    #     )
    #     user.is_admin = True
    #     user.save(using=self._db)
    #     return user
    
    def _create_user(self, email, password, name, phone_number, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(
            email = self.normalize_email(email),
            name = name,
            phone_number = phone_number,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)              
        return user

    def create_user(self, email, password, name, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email, password, name, phone_number, **extra_fields)

    def create_superuser(self, email, password, name, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(email, password, name, phone_number, **extra_fields)

class Customer(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, unique=True)
    token = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    is_staff = models.BooleanField(default=False) # must needed, otherwise you won't be able to log into django-admin.
    is_active = models.BooleanField(default=True) # must needed, otherwise you won't be able to log into django-admin.
    is_superuser = models.BooleanField(default=False) # this field we inherit from PermissionsMixin.
    objects = CustomerManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name', 'email']

    # def __str__(self):
    #     return self.email

    # def has_perm(self, perm, obj=None):
    #     return True

    # def has_module_perms(self, app_label):
    #     return True
    # def authenticate(self, phone, password):
    #     phone = self.objects.filter(phone_number = phone, password  = password)
    #     if phone.exists():
    #         return phone
    #     else:
    #         return None

    # @property
    # def is_staff(self):
    #     return self.is_admin
    # def __str__(self):
    #     return self.username





# class User(AbstractBaseUser):
#     email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
#     name = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=15, unique=True)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)

#     objects = Manager()

    # USERNAME_FIELD = 'phone_number'
    # REQUIRED_FIELDS = ['name']

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return True

#     def has_module_perms(self, app_label):
#         return True

#     @property
#     def is_staff(self):
#         return self.is_admin

class Transporter(models.Model):
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    token = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, default="dummy")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username

class Quotes(models.Model):
    # unique_id = models.UUIDField(max_length=20,auto_created=True)
    quote = models.IntegerField(blank=False, null=False)
    transporter = models.ForeignKey(Transporter, on_delete=models.DO_NOTHING,related_name='transporter_who_gave_quote', blank=True, null=True)
    shipment = models.ForeignKey('Shipment',on_delete=models.CASCADE, related_name='shipment_for_which_quote_is_given', blank=True, null=True)

    class Meta:
        unique_together = ('transporter', 'shipment')

class Shipment(models.Model):
    Type=models.CharField(max_length=20,default="MiniTruck")
    Length=models.IntegerField(default="0")
    Width=models.IntegerField(default="0")
    Height=models.IntegerField(default="0")
    Weight=models.IntegerField(default="0")
    Quantity = models.IntegerField(default="0")
    Pickup = models.CharField(max_length=50,default="Pick")
    Drop = models.CharField(max_length=50,default="Drop")
    offer_price = models.IntegerField(default=1000, blank=True)
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE, related_name='transporter_who_accepted_the_shipment', blank=True, null=True, default= None)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_who_created_a_listing",  blank=True, null=True,default= None)
    # quotes = models.ForeignKey(Quotes, on_delete=models.CASCADE, related_name='quote_given_by_transporter', blank=True, null=True,default= None)
    title = models.CharField(max_length=255, default='acer computer')
    earliest_pickup_date = models.DateField(default='2024-06-12')
    latest_pickup_date = models.DateField(default='2024-06-15')
    earliest_delivery_date = models.DateField(default='2024-06-19')
    latest_delivery_date = models.DateField(default='2024-06-20')
    photo = models.ImageField(upload_to='shipment_photos/', blank=True, null=True)
    p_pincode =models.IntegerField(default=600012)
    d_pincode =models.IntegerField(default=600012)
    is_accepted = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=True)