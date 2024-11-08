# books_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),  # Direct URL for book listing
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('review/<int:book_id>/', views.review_book, name='review_book'),
]
