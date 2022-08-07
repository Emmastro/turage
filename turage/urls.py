from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    #path("accounts/", include("accounts.urls")),
    path("", include("ride.urls")),
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]