from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views.books_views import BookViewSet, ReviewViewSet, book_summary, book_recommendations, generate_book_summary

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'books/(?P<book_id>\d+)/reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('books/<int:pk>/summary/', book_summary, name='book-summary'),
    path('recommendations/', book_recommendations, name='book-recommendations'),
    path('generate-summary/', generate_book_summary, name='generate-summary'),
]
