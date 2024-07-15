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


Deployment:

Step 1: Create an EC2 Instance

1.1 Launch an EC2 Instance
Sign in to the AWS Management Console and open the EC2 Dashboard.

Launch an instance:

Click on the Launch Instance button.
Choose an Amazon Machine Image (AMI). For simplicity, you can use the Amazon Linux 2 AMI or Ubuntu Server.
Choose an instance type. For development, the t2.micro instance type (eligible for free tier) is sufficient.
Configure instance details:
Number of instances: 1
Network: Default VPC
Subnet: Choose any default subnet
Auto-assign Public IP: Enable
Add storage: Default storage is typically enough, but you can increase it if needed.
Add tags: Add a tag to name your instance.
Configure security group:
Add a rule for HTTP on port 80.
Add a rule for HTTPS on port 443.
Add a rule for SSH on port 22 (restrict to your IP address for security).
Review and launch:

Click on the Launch button.
Select or create a key pair. This is essential for SSH access to your instance.
1.2 Connect to Your Instance
Download and save your key pair file (.pem) securely.

Change the file permissions of your key pair file:
    "chmod 400 your-key-pair.pem"

Connect to your instance using SSH:
    "ssh -i "your-key-pair.pem" ec2-user@your-ec2-public-ip"

1.3 Set Up Your Server

1. Update the package list:
        sudo yum update -y  # For Amazon Linux
        sudo apt update -y  # For Ubuntu

2. Install necessary packages:

    sudo yum install python3-pip nginx git -y  # For Amazon Linux
    sudo apt install python3-pip nginx git -y  # For Ubuntu

3. pip3 install virtualenv

4. Clone your project repository:

    git clone git@github.com:ayushchd8/book_management_app.git
    cd book_management

5. Create a virtual environment:
       virtualenv venv
       source venv/bin/activate

6. Install project dependencies:
       pip install -r requirements.txt
   
8. Set up your environment variables:
        touch .env
        echo "DATABASE_NAME=bookdb" >> .env
        echo "DATABASE_USER=yourusername" >> .env
        echo "DATABASE_PASSWORD=yourpassword" >> .env
        echo "DATABASE_HOST=your-rds-endpoint" >> .env
        echo "DATABASE_PORT=5432" >> .env
     
9. python manage.py migrate
10. python manage.py createsuperuser
11. python manage.py collectstatic

12. Run Server:
     python manage.py runserver 0.0.0.0:8000


1.4 Configure Nginx

1. Edit the Nginx configuration file: sudo nano /etc/nginx/nginx.conf
2. Add server configuration: 
        
   server {
    listen 80;
    server_name your-ec2-public-ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/project/static/;
    }
}

3. Restart Nginx: sudo systemctl restart nginx



Step 2: Set Up AWS RDS

2.1 Create an RDS Instance

 1. Open the RDS Dashboard.
 2. Create a new database:

        Choose Standard Create.
        Select PostgreSQL as the engine.
        Choose the Free Tier template if eligible.
        Configure database settings:
        DB instance identifier: bookdb
        Master username: yourusername
        Master password: yourpassword
        Configure instance specifications:
        DB instance class: db.t2.micro
        Storage: General Purpose (SSD), 20 GB.
        Configure connectivity:
        VPC: Default VPC
        Public access: Yes
        VPC security group: Create a new security group or use an existing one.
        Additional configuration:
        Initial database name: bookdb

3. Create the database.


2.2 Connect to RDS Instance

        1. Modify the RDS security group to allow incoming connections from EC2 instance's IP address.
        2. Update your .env file with the RDS endpoint: "echo "DATABASE_HOST=your-rds-endpoint" >> .env"
        3. Update your settings.py:

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


Step 3: Set Up AWS S3

    3.1 Create an S3 Bucket

        1. Open the S3 Dashboard.
        2. Create a new bucket:

                Bucket name: your-bucket-name
                Region: Choose the same region as your EC2 instance.
                Leave other settings as default and create the bucket.
                
    3.2 Configure Django to Use S3

        1. Install boto3 and django-storages: "pip install boto3 django-storages"
        2. Update settings.py:

            INSTALLED_APPS += [
                'storages',
            ]
            
            AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
            AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
            AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
            AWS_S3_REGION_NAME = 'your-region'
            AWS_S3_SIGNATURE_VERSION = 's3v4'
            
            DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
            STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
            
            STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/'
            MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'
        
        3. Add your AWS credentials to the .env file:
            echo "AWS_ACCESS_KEY_ID=your-access-key-id" >> .env
            echo "AWS_SECRET_ACCESS_KEY=your-secret-access-key" >> .env

        4. Collect Static Files Again: "python manage.py collectstatic"


Step 4: Set Up CI/CD Pipeline

    4.1 Use GitHub Actions for CI/CD

        1. Create a GitHub Actions workflow file: .github/workflows/deploy.yml

                name: Deploy to EC2

                on:
                  push:
                    branches:
                      - main
                
                jobs:
                  deploy:
                    runs-on: ubuntu-latest
                
                    steps:
                    - name: Checkout code
                      uses: actions/checkout@v2
                
                    - name: Set up Python
                      uses: actions/setup-python@v2
                      with:
                        python-version: 3.9
                
                    - name: Install dependencies
                      run: |
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                
                    - name: Run tests
                      run: |
                        python manage.py test
                
                    - name: Deploy to EC2
                      env:
                        EC2_KEY: ${{ secrets.EC2_KEY }}
                        EC2_USER: ${{ secrets.EC2_USER }}
                        EC2_IP: ${{ secrets.EC2_IP }}
                      run: |
                        scp -i $EC2_KEY -r * $EC2_USER@$EC2_IP:/home/ec2-user/book_management/
                        ssh -i $EC2_KEY $EC2_USER@$EC2_IP 'source /home/ec2-user/book_management/venv/bin/activate && cd /home/ec2-user/book_management && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput && sudo systemctl restart nginx'

        2. Add GitHub Secrets:

            Go to your GitHub repository settings.
            Add the following secrets:
            EC2_KEY: Your EC2 key pair content.
            EC2_USER: ec2-user (or the user you used for your EC2 instance).
            EC2_IP: Your EC2 instance public IP address.


        3. Push your changes to GitHub to trigger the deployment.

