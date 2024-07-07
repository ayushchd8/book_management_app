# books/views.py

from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from books.models import Book, Review
from books.serializers.books_serializer import BookSerializer, ReviewSerializer
from django.db.models import Avg
from books.utils import generate_summary
import joblib
import pandas as pd
import aiohttp
from asgiref.sync import sync_to_async

@api_view(['GET', 'POST'])
async def book_list_create(request):
    if request.method == 'GET':
        books = await sync_to_async(list)(Book.objects.all())
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            await sync_to_async(serializer.save)()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
async def book_detail(request, id):
    try:
        book = await sync_to_async(Book.objects.get)(pk=id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            await sync_to_async(serializer.save)()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        await sync_to_async(book.delete)()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
async def add_review(request, id):
    try:
        book = await sync_to_async(Book.objects.get)(pk=id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        await sync_to_async(serializer.save)(book=book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
async def get_reviews(request, id):
    try:
        book = await sync_to_async(Book.objects.get)(pk=id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    reviews = await sync_to_async(list)(book.reviews.all())
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
async def book_summary(request, id):
    try:
        book = await sync_to_async(Book.objects.get)(pk=id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    summary = f"Summary for {book.title} by {book.author}."
    average_rating = await sync_to_async(book.reviews.aggregate)(Avg('rating')).get('rating__avg')
    return Response({'summary': summary, 'average_rating': average_rating})

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

    input_data = pd.DataFrame({'year_published': [int(year_published)], 'genre': [genre]})
    input_data = pd.get_dummies(input_data, columns=['genre'])

    model_features = model.feature_names_in_
    for feature in model_features:
        if feature not in input_data.columns:
            input_data[feature] = 0

    predictions = model.predict(input_data)
    recommended_books = await sync_to_async(Book.objects.filter)(genre=genre).annotate(average_rating=Avg('reviews__rating')).order_by('-average_rating')[:5]

    recommendations = []
    for book in recommended_books:
        recommendations.append({'title': book.title, 'author': book.author, 'year_published': book.year_published, 'average_rating': book.average_rating})

    return Response(recommendations, status=status.HTTP_200_OK)


@api_view(['POST'])
async def generate_book_summary(request):
    content = request.data.get('content')
    summary = generate_summary(content)
    return Response({'summary': summary})
