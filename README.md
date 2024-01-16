# Note API Project Documentation
Introduction
The Note API Project is a Django Rest Framework (DRF) project that provides a secure and scalable API for managing notes. Users can create, read, update, and delete notes, share notes with other users, and search for notes based on keywords.

Getting Started

Prerequisites

Before running the project, ensure that you have the following installed:

Python 3.x

virtualenv (optional but recommended)

pip (Python package installer)

Setup

Clone the repository:



git clone https://github.com/harrshjain/note_api_project.git

Navigate to the project directory:

cd note_api_project

Create a virtual environment (optional but recommended):



python -m venv your_virtual_environment

Activate the virtual environment:

On Windows:

.\your_virtual_environment\Scripts\activate
On Unix or MacOS:

source your_virtual_environment/bin/activate

Install project dependencies:



pip install -r requirements.txt

Database Setup

Open the note_api_project/settings.py file and configure your database settings. The project is currently set to use PostgreSQL.

Apply database migrations:

python manage.py migrate

Create a Superuser

Create an administrative superuser to access the Django admin panel:

python manage.py createsuperuser

Follow the prompts to set up the superuser account.

Running the Project

Start the development server:

python manage.py runserver

Open your web browser and navigate to http://localhost:8000/admin/ to log in with the superuser credentials.

Access the API at http://localhost:8000/api/.


API Endpoints

Authentication Endpoints:

POST /api/auth/signup: Create a new user account.

POST /api/auth/login: Log in to an existing user account and receive an access token.

Note Endpoints:

GET /api/notes: Get a list of all notes for the authenticated user.

GET /api/notes/:id: Get a note by ID for the authenticated user.

POST /api/notes: Create a new note for the authenticated user.

PUT /api/notes/:id: Update an existing note by ID for the authenticated user.

DELETE /api/notes/:id: Delete a note by ID for the authenticated user.

POST /api/notes/:id/share: Share a note with another user for the authenticated user.

GET /api/search?q=:query: Search for notes based on keywords for the authenticated user.

Conclusion

You have successfully set up and run the Note API Project. Explore the API endpoints and customize the project based on your requirements.

