import pandas as pd
from django.core.management.base import BaseCommand
from books.models import Book, Review
from django.db.models import Avg
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

class Command(BaseCommand):
    help = 'Train the book recommendation model'

    def handle(self, *args, **kwargs):
        # Fetch data from Book model
        books = Book.objects.all().annotate(average_rating=Avg('reviews__rating')).values(
            'title', 'author', 'genre', 'year_published', 'average_rating'
        )
        df = pd.DataFrame(list(books))

        if df.empty:
            self.stdout.write(self.style.ERROR('No data found in the Book model'))
            return

        # Feature encoding
        df = pd.get_dummies(df, columns=['genre'])

        # Split the data
        X = df.drop(['title', 'author', 'average_rating'], axis=1)
        y = df['average_rating']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Save the model
        joblib.dump(model, 'book_recommendation_model.pkl')

        self.stdout.write(self.style.SUCCESS('Successfully trained and saved the book recommendation model'))
