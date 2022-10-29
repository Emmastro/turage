from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    #path("accounts/", include("accounts.urls")),
    path("", include("ride.urls")),
    path("admin/", admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
]

handler404 = 'ride.views.handler404'
handler500 = 'ride.views.handler500'
handler403 = 'ride.views.handler403'
handler400 = 'ride.views.handler400'