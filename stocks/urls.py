from django.urls import path
from .views import stock_chart  # Import your view function

urlpatterns = [
    path('', stock_chart, name='stock_chart'),
]


