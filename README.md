# Task Manager API

A RESTful Task Management API built with Django and Django REST Framework. This project allows authenticated users to organize tasks, manage categories, set priorities and deadlines, and upload task attachments.

## Features

* **Authentication:** JWT-based authentication.
* **Task Management:** Create, retrieve, update, and delete tasks.
* **Category Management:** Organize tasks into categories.
* **Task Priorities:** Assign priorities to tasks.
* **Deadlines:** Set due dates for tasks.
* **Filtering:** Filter tasks based on supported fields.
* **Pagination:** Retrieve results in manageable pages.
* **File Attachments:** Upload supported files with a 5 MB size limit.
* **User Data Isolation:** Users can access and manage only their own tasks.
* **Input Validation:** Validate task data and uploaded attachments.
* **Testing:** Automated API tests for core task operations and file uploads.
* **Static Files:** WhiteNoise configuration for serving collected static files.

## Tech Stack

* Python
* Django
* Django REST Framework
* Django REST Framework Simple JWT
* SQLite for local development
* WhiteNoise
* Git and GitHub

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/irfan2604-creator/task-manager-api.git
cd task-manager-api
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use an approved alternative activation method or configure your execution policy appropriately.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file in the project root.

Example development configuration:

```dotenv
DJANGO_ENV=development
DEBUG=True
SECRET_KEY=replace-with-a-new-local-development-secret
ALLOWED_HOSTS=127.0.0.1,localhost,testserver
```

Use a newly generated secret key for your local environment. Never commit `.env` or production credentials to Git.

Ensure your Django settings load these environment variables correctly.

### 5. Apply migrations

```powershell
python manage.py migrate
```

### 6. Create a superuser

```powershell
python manage.py createsuperuser
```

Follow the prompts to create an administrator account.

### 7. Start the development server

```powershell
python manage.py runserver
```

The API will be available at:

`http://127.0.0.1:8000/`

## API Endpoints

The following endpoints describe the project's intended API structure. Confirm the actual URL configuration before relying on these routes.

| Method    | Endpoint                | Purpose                              |
| --------- | ----------------------- | ------------------------------------ |
| GET       | `/api/tasks/`           | List the authenticated user's tasks  |
| POST      | `/api/tasks/`           | Create a task                        |
| GET       | `/api/tasks/<id>/`      | Retrieve a task                      |
| PUT       | `/api/tasks/<id>/`      | Replace a task                       |
| PATCH     | `/api/tasks/<id>/`      | Partially update a task              |
| DELETE    | `/api/tasks/<id>/`      | Delete a task                        |
| GET       | `/api/categories/`      | List categories                      |
| POST      | `/api/categories/`      | Create a category                    |
| GET       | `/api/categories/<id>/` | Retrieve a category                  |
| PUT/PATCH | `/api/categories/<id>/` | Update a category                    |
| DELETE    | `/api/categories/<id>/` | Delete a category                    |
| POST      | `/api/token/`           | Obtain JWT access and refresh tokens |
| POST      | `/api/token/refresh/`   | Refresh an access token              |

## Authentication

Obtain a JWT token using the token endpoint.

Example request:

```http
POST /api/token/
Content-Type: application/json
```

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Use the returned access token in subsequent API requests:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Do not share real access tokens or credentials.

## Task Attachment Uploads

The task API accepts multipart form data for file uploads.

Supported extensions:

* PDF
* TXT
* PNG
* JPG
* JPEG

Maximum file size: **5 MB**.

Example request:

```http
POST /api/tasks/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: multipart/form-data
```

Include the task fields and an `attachment` file in the multipart request.

The extension and size checks are basic validation, not a complete file-security solution. Production deployments should also validate file content and use appropriate upload-storage and access controls.

## Running Tests

Run the Django test suite:

```powershell
python manage.py test
```

The test suite covers task API operations, authentication, user ownership, and attachment uploads where implemented.

## Static and Media Files

Static files are collected using:

```powershell
python manage.py collectstatic --noinput
```

WhiteNoise is configured to serve collected static files.

User-uploaded media is stored locally during development. Production deployments should use suitable persistent or object storage and configure media access securely.

## Security Notes

* Keep `.env` out of version control.
* Never commit passwords, secret keys, or API credentials.
* Use `DEBUG=False` in production.
* Configure production `ALLOWED_HOSTS` explicitly.
* Use HTTPS in production.
* Configure secure cookies and other production security settings.
* Review uploaded-file validation and access controls before deployment.

## Future Improvements

* Add more filtering and search options.
* Improve API documentation with OpenAPI/Swagger.
* Expand automated tests.
* Add structured logging and error monitoring.
* Add Docker and Docker Compose support.
* Deploy the API to a production hosting platform.

## Author

Developed as a backend portfolio project to practice Django, Django REST Framework, authentication, authorization, API design, file uploads, testing, and production configuration.
