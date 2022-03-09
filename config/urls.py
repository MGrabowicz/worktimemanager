from django.contrib import admin
from django.urls import path, include
from accounts.views import homeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homeView, name='home'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('teams/', include('teams.urls')),
    path('timesheets/', include('timesheets.urls')),
    path('absences/', include('absences.urls')),
]
