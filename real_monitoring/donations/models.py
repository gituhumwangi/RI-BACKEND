from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        """
        Create and return a user with an email or phone number and password.
        """
        if not email and not phone_number:
            raise ValueError('The user must have either an email or phone number')
        
        if email:
            email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, phone_number, password, **extra_fields)


class User(AbstractBaseUser):
    # Required fields
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True, null=True, blank=True)  # Nullable for users without email
    phone_number = models.CharField(max_length=20, unique=True)  # Primary contact for non-smartphone users
    role = models.CharField(max_length=50, choices=[('donor', 'Donor'), ('recipient', 'Recipient'), ('admin', 'Admin')])
    
    # Authentication & security fields
    password_hash = models.CharField(max_length=255)  # Optional if using Django's built-in password management
    pin_code = models.CharField(max_length=10, null=True, blank=True)  # For SMS/USSD users
    communication_method = models.CharField(max_length=50, choices=[('email', 'Email'), ('sms', 'SMS'), ('ussd', 'USSD')])

    # Optional fields
    preferences = models.JSONField(null=True, blank=True)  # For storing preferences like notification settings
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('suspended', 'Suspended')])
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Required fields for Django's user model
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # User manager
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'  # Login using phone number for non-smartphone users
    REQUIRED_FIELDS = []  # Can add 'email' or other fields depending on your requirement

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
    
class Donation(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donations_made')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donations_received')
    
    business_profile = models.ForeignKey('BusinessProfile', on_delete=models.SET_NULL, null=True, blank=True)  # Link to BusinessProfile
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')])
    timestamp = models.DateTimeField(auto_now_add=True)
    
    verification_id = models.IntegerField(null=True, blank=True)
    transaction_hash = models.CharField(max_length=255, null=True, blank=True)
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Donation from {self.donor} to {self.recipient} - {self.amount} {self.currency}"

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_sent')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_received')
    
    content = models.TextField()  # The actual message content
    encrypted = models.BooleanField(default=True)  # Flag to mark if the message is encrypted
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically logs when the message was created
    
    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} on {self.timestamp}"
    
class Verification(models.Model):
    donation = models.OneToOneField('Donation', on_delete=models.CASCADE)  # One-to-one link with the Donation model
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # User (e.g., admin) who verified the donation
    verification_date = models.DateTimeField(auto_now_add=True)  # When the verification was done
    verification_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('verified', 'Verified'), ('rejected', 'Rejected')])
    verification_notes = models.TextField(null=True, blank=True)  # Optional field for notes about the verification process
    
    def __str__(self):
        return f"Verification for Donation ID {self.donation.id}: {self.verification_status}"
    
class BusinessProfile(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Owner of the business (usually the donor)
    business_name = models.CharField(max_length=255)
    description = models.TextField()
    registration_number = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name


