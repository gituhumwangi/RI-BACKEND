from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("donations.urls")),
    path('admin/', admin.site.urls),
]
