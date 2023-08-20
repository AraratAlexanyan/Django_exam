from django.urls import path

from . import views
app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path('reg/', views.register_phone, name='registration'),  # ← new entry
    path('verify/', views.verify_code, name='verify'),  # ← new entry
    path('home/', views.home, name='home'),  # ← new entry
]
