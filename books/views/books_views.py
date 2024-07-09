from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from books.models import Book, Review
from books.serializers.books_serializer import BookSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from books.utils import generate_summary
import joblib
import pandas as pd
import asyncio
from asgiref.sync import sync_to_async

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    async def list(self, request, *args, **kwargs):
        queryset = await sync_to_async(list)(Book.objects.all())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    async def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            await sync_to_async(serializer.save)()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    async def list(self, request, book_id=None):
        queryset = await sync_to_async(list)(self.queryset.filter(book_id=book_id))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    async def create(self, request, book_id=None):
        request.data['book'] = book_id
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            await sync_to_async(serializer.save)()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
async def book_summary(request, pk):
    try:
        book = await sync_to_async(Book.objects.get)(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    summary = await sync_to_async(generate_summary)(book.content)
    avg_rating = await sync_to_async(Review.objects.filter(book=book).aggregate)(Avg('rating'))
    return Response({'summary': summary, 'average_rating': avg_rating})


@api_view(['GET'])
async def book_recommendations(request):
    try:
        model = joblib.load('book_recommendation_model.pkl')
    except FileNotFoundError:
        return Response({'error': 'Model not found. Please train the model first.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    genre = request.query_params.get('genre', None)
    year_published = request.query_params.get('year_published', None)

    if genre is None or year_published is None:
        return Response({'error': 'Please provide genre and year_published as query parameters.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a DataFrame for the input data
    input_data = pd.DataFrame({
        'year_published': [int(year_published)],
        'genre': [genre]
    })
    input_data = pd.get_dummies(input_data, columns=['genre'])

    # Ensure the input data has the same columns as the training data
    model_features = model.feature_names_in_
    for feature in model_features:
        if feature not in input_data.columns:
            input_data[feature] = 0

    # Make prediction
    predictions = model.predict(input_data)
    recommended_books_queryset = Book.objects.filter(genre=genre).annotate(average_rating=Avg('reviews__rating')).order_by('-average_rating')[:5]
    recommended_books = await sync_to_async(list)(recommended_books_queryset)

    recommendations = []
    for book in recommended_books:
        recommendations.append({
            'title': book.title,
            'author': book.author,
            'year_published': book.year_published,
            'average_rating': book.average_rating,
        })

    return Response(recommendations, status=status.HTTP_200_OK)


@api_view(['POST'])
async def generate_book_summary(request):
    content = request.data.get('content')
    summary = await sync_to_async(generate_summary)(content)
    return Response({'summary': summary})
