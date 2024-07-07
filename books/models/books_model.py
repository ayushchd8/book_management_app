from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    year_published = models.IntegerField()
    summary = models.TextField()

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    review_text = models.TextField()
    rating = models.IntegerField()