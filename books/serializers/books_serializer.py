from rest_framework import serializers
from books.models.books_model import Book, Review
from django.db.models import Avg

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'year_published', 'average_rating']

        def get_average_rating(self, obj):
            return obj.reviews.aggregate(Avg('rating')).get('rating__avg')