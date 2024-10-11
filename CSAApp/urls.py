from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ask/', views.ask_Q, name='ask'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    
    
    path('fetch_conversation_data/', views.fetch_conversation_data, name='fetch_conversation_data'),
]
