from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("status/", include("health.urls")),
    path("/", include("bereikbaarheid.urls")),
]
