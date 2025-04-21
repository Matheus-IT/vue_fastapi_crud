# Vue + Fastapi CRUD Application

A full-stack application built with **Vue.js** (frontend) and **Fastapi** (backend) to demonstrate CRUD (Create, Read, Update, Delete) operations for managing users. The application is containerized using **Docker** for easy setup and deployment.

---

## Features

- **List Users**: View a table of users with details like username, roles, timezone, and activity status.
- **Create User**: Add a new user with a username, password, roles, timezone, and activity status.
- **Edit User**: Update an existing user's details.
- **Delete User**: Remove a user from the system.
- **User Details Page**: View detailed information about a specific user.
- **Responsive Design**: Built with **Vuetify** for a clean and responsive UI.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

---

## Getting Started

Follow these steps to set up and run the application:

### 1. Clone the Repository

```bash
git clone https://github.com/Matheus-IT/vue_flask_crud.git
cd vue_flask_crud
```

### 2. Build and Run the Application

Build the Docker images and start the containers:

```bash
docker compose build
docker compose up
```

### 3. Access the Application

Once the containers are running, open your browser and navigate to:

- **Frontend (Vue.js)**: [http://localhost:5173](http://localhost:5173)
- **Backend (Fastapi API)**: [http://localhost:8000](http://localhost:8000)

---

## Application Structure

### Frontend (Vue.js)

- **Vue 3**: Frontend framework.
- **Vuetify**: UI component library for a Material Design look.
- **Vue Router**: Handles client-side routing.
- **Axios**: For making HTTP requests to the Fastapi backend.

### Backend (Fastapi)

- **Fastapi**: Python web framework for the backend API.
- **MongoDB**: Database for storing user data.

### Docker

- **Docker Compose**: Manages multi-container Docker applications.
- **Services**:
  - `frontend`: Vue.js application.
  - `backend`: Fastapi API.
  - `mongo`: MongoDB database.
  - `importer`: Script to populate the database.
---

## API Endpoints

The Fastapi backend exposes the following RESTful API endpoints:

| Method | Endpoint           | Description                     |
|--------|--------------------|---------------------------------|
| GET    | `/users`           | Get a list of all users.        |
| GET    | `/users/<user_id>` | Get details of a specific user. |
| POST   | `/users`           | Create a new user.              |
| PUT    | `/users/<user_id>` | Update an existing user.        |
| DELETE | `/users/<user_id>` | Delete a user.                  |

---

## Stopping the Application

To stop the application, press `Ctrl+C` in the terminal where the containers are running, then run:

```bash
docker compose down
```

This will stop and remove the containers.

---

## Troubleshooting

### Common Issues

1. **Port Conflicts**:
   - Ensure ports `5173` (frontend) and `8000` (backend) are not in use by other applications.

2. **Docker Build Failures**:
   - Ensure Docker and Docker Compose are installed correctly.
   - Run `docker compose build --no-cache` to rebuild the images without cache.
