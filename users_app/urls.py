from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('deposit/', views.deposit, name='deposit'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    # path('return/<int:borrowing_id>/', views.return_book, name='return_book'),
]

urlpatterns += [
    path('return/<int:borrowing_id>/', views.return_book, name='return_book'),
]

