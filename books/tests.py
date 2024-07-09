from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book, Review

class BookAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_create_book(self):
        url = reverse('book-list')
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'genre': 'Fiction',
            'year_published': 2022
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'Test Book')

    def test_get_books(self):
        Book.objects.create(title='Test Book', author='Test Author', genre='Fiction', year_published=2022)
        url = reverse('book-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_book_by_id(self):
        book = Book.objects.create(title='Test Book', author='Test Author', genre='Fiction', year_published=2022)
        url = reverse('book-detail', args=[book.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], book.title)

    def test_update_book(self):
        book = Book.objects.create(title='Test Book', author='Test Author', genre='Fiction', year_published=2022)
        url = reverse('book-detail', args=[book.id])
        data = {
            'title': 'Updated Test Book',
            'author': 'Test Author',
            'genre': 'Fiction',
            'year_published': 2022
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get().title, 'Updated Test Book')

    def test_delete_book(self):
        book = Book.objects.create(title='Test Book', author='Test Author', genre='Fiction', year_published=2022)
        url = reverse('book-detail', args=[book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_add_review_to_book(self):
        book = Book.objects.create(title='Test Book', author='Test Author', genre='Fiction', year_published=2022)
        url = reverse('book-reviews', args=[book.id])
        data = {
            'content': 'Great book!',
            'rating': 5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().content, 'Great book!')

    def test_get_reviews_for_book(self):
        book = Book.objects.create(title='Test Book', author='Test Author', genre='Fiction', year_published=2022)
        Review.objects.create(book=book, content='Great book!', rating=5)
        url = reverse('book-reviews', args=[book.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_book_summary(self):
        book = Book.objects.create(title='Test Book', author='Test Author', genre='Fiction', year_published=2022)
        Review.objects.create(book=book, content='Great book!', rating=5)
        Review.objects.create(book=book, content='Not bad', rating=3)
        url = reverse('book-summary', args=[book.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('average_rating', response.data)

    def test_get_recommendations(self):
        Book.objects.create(title='Fiction Book', author='Author1', genre='Fiction', year_published=2020)
        Book.objects.create(title='Non-Fiction Book', author='Author2', genre='Non-Fiction', year_published=2021)
        url = reverse('book-recommendations')
        response = self.client.get(url, {'genre': 'Fiction'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_generate_summary(self):
        url = reverse('book-generate-summary')
        data = {
            'content': 'This is a test content for generating summary.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('summary', response.data)
