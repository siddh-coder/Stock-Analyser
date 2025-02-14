from django.urls import path
from .views import stock_chart  # Import your view function

urlpatterns = [
    path('chart/', stock_chart, name='stock_chart'),
]


