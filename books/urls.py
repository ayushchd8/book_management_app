from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views.books_views import book_list_create, book_detail, add_review, get_reviews, book_summary, generate_book_summary, generate_summary,book_recommendations

urlpatterns = [
    path('books', book_list_create),
    path('books/<int:id>', book_detail),
    path('books/<int:id>/reviews', add_review),
    path('books/<int:id>/reviews', get_reviews),
    path('books/<int:id>/summary', book_summary),
    path('recommendations', book_recommendations),
    path('generate-summary', generate_book_summary),
]