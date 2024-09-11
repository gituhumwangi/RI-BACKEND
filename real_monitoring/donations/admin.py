from django.contrib import admin
from .models import User, Donation, Message, Verification, BusinessProfile


# Register your models here.
admin.site.register(User)
admin.site.register(Donation)
admin.site.register(Message)
admin.site.register(Verification)
admin.site.register(BusinessProfile)
