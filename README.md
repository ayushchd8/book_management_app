Book Management System
This project is a Django-based book management system integrated with a locally running Llama3 generative AI model for generating book summaries and a machine learning model for recommending books based on genre and average rating. The project is designed to be scalable, asynchronous, and deployable on AWS.

Features:

CRUD operations for Books and Reviews
Book summaries using a locally running Llama3 model
Book recommendations based on genre and average rating
Basic authentication and secure communication
Asynchronous operations for better scalability
Deployment on AWS
Unit and integration tests


Table of Contents:

Installation
Configuration
Usage
Endpoints
Testing
Deployment
Installation


Clone the repository:
git clone <repository_url>
cd book_management

Set up a virtual environment:
python3 -m venv env
source env/bin/activate

Install Dependencies:
pip install -r requirements.txt

Set up PostgreSQL:

Install PostgreSQL.
Create a database and user.

Configure environment variables:
Create a .env file in the project root with the following content:

DATABASE_NAME=bookdb
DATABASE_USER=yourusername
DATABASE_PASSWORD=yourpassword
DATABASE_HOST=localhost
DATABASE_PORT=5432

python manage.py migrate


Configuration
Django Settings:
Ensure settings.py includes the necessary configurations for installed apps, middleware, and database connections.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}

Endpoints
Books:

List all books: GET /api/books/
Retrieve a book: GET /api/books/{id}/
Create a book: POST /api/books/
Update a book: PUT /api/books/{id}/
Delete a book: DELETE /api/books/{id}/
Reviews:

List all reviews for a book: GET /api/books/{book_id}/reviews/
Retrieve a review: GET /api/reviews/{id}/
Create a review: POST /api/books/{book_id}/reviews/
Update a review: PUT /api/reviews/{id}/
Delete a review: DELETE /api/reviews/{id}/
Book Summary:

Generate a summary for a book: GET /api/books/{id}/summary/
Book Recommendations:

Get book recommendations: GET /api/books/recommendations/
Generate Book Summary:

Generate a summary for provided content: POST /api/books/generate-summary/

Testing:

python manage.py test


Deployment
Deploying on AWS EC2:

Set up an EC2 instance.
Install necessary dependencies.
Deploy your Django project.
Using AWS RDS:

Create an RDS instance.
Update your DATABASES setting in settings.py.
Using AWS S3:

Create an S3 bucket.
Use S3 for static and media file storage.




