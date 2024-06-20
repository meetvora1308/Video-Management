# Video Management System

## Overview

This project provides a video management system with APIs for user registration, video upload, and video search functionalities. It runs on Ubuntu and requires Python 3.10.12 and redis.

## Setup

### Clone the Repository

Clone the project repository:

git clone <repository_url>
cd video-management

### Create Virtual Environment

Create and activate a virtual environment:

```python3 -m venv venv```

```source venv/bin/activate```  # On Windows use `venv\Scripts\activate`

### Install Dependencies

Install required dependencies:

```pip install -r requirements.txt```

## Running the Application

Ensure your virtual environment is activated and dependencies are installed. Start the application using Uvicorn:

```uvicorn app:app```

Additionally, start the Celery consumer for asynchronous tasks:

```celery -A celery_config.app worker --loglevel=info```

## APIs

### 1. Create User API

- **Endpoint**: /user/create_user
- **Method**: POST
- **Headers**:
  - accept: application/json
  - Content-Type: application/json
- **Payload**:
  {
    "username": "meetvora13",
    "password": "123"
  }

### 2. Upload Video API

- **Endpoint**: /video/upload_video
- **Method**: POST
- **Headers**:
  - accept: application/json
  - Authorization: Bearer <token>
  - Content-Type: multipart/form-data
- **Payload**: Example using curl:
  curl -X 'POST' \
    'http://127.0.0.1:8000/video/upload_video' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer <token>' \
    -F 'file=@baby laughing hysterically _ baby funny video status 😂😂.mp4;type=video/mp4'

### 3. Search Video API

- **Endpoint**: /video/search_video
- **Method**: GET
- **Headers**:
  - accept: application/json
  - Authorization: Bearer <token>
- **Query Parameters**:
  - name: Name of the video to search for.
- **Example Request**:
  curl -X 'GET' \
    'http://127.0.0.1:8000/video/search_video?name=file_example_AVI_480_750kB' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer <token>'

*Note*: Video search is based on name and size in bytes.

## Project Structure

- app/: Contains the main application logic.
- uploads/: Directory where uploaded videos are stored.
- requirements.txt: Lists Python dependencies for the project.
- README.md: This file, providing project overview, setup instructions, API details, and usage examples.
