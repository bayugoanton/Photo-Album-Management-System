Recipe Gallery Application

A robust Django-based web application designed for managing and showcasing recipe collections. This project utilizes Cloudinary for secure image storage, Django's authentication system for user management, and a clean MVT (Model-View-Template) architecture to provide a seamless user experience.

Features
User Authentication: Secure sign-up, login, and logout functionality.

Album Management: Create, read, and manage photo albums.

Photo CRUD: Upload, edit, and delete recipe photos with instant feedback.

Search Integration: Filter recipes within albums by title or description.

Cloud Storage: Image handling via Cloudinary API.

Responsive Design: Built with Bootstrap for optimal viewing on any device.

Prerequisites
Ensure you have the following installed on your machine:

Python 3.x

pip

Git

Instructions to Run Locally
Clone the repository:

Bash
git clone <your-repository-url>
cd <your-project-folder>
Create and activate a virtual environment:

Bash
python -m venv venv
# On Windows:
venv\Scripts\activate


Install dependencies:

Bash
pip install -r requirements.txt
Configure Environment Variables:
Create a .env file in the root directory (or set them in your system environment) and add the following:

Code snippet
SECRET_KEY=your_django_secret_key
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
DEBUG=True
Run Migrations:

Bash
python manage.py makemigrations
python manage.py migrate
Start the development server:

Bash
python manage.py runserver
Open http://127.0.0.1:8000/ in your browser.

Environment Variables
The application requires the following variables for production (e.g., on Render):

SECRET_KEY: A unique string for Django's cryptographic signing.

CLOUDINARY_URL: Your unique Cloudinary API credentials.

DATABASE_URL: (Optional) Connection string for your production database.

DEBUG: Set to False in production.
