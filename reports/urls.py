from django.urls import path
from reports import views

urlpatterns = [
    path('vendor/', views.vendor_report, name='vendor_report'),
]