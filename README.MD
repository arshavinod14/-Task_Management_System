# Task Management API

## Setup and Installation Instructions

Follow the steps below to set up and run the Task Management API locally:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/arshavinod14/Task_Management_System.git
   cd task_management
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:

   - Update the database settings in `settings.py`.
   - Run the migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

5. **Run the Development Server**:

   ```bash
   python manage.py runserver
   ```

6. **Test the Endpoints**:
   Use [Postman](https://www.postman.com/) or any API testing tool to test the API endpoints.

---

## Features Implemented

1. **User Authentication**:

   - **Register**: Allows new users to register.
   - **Login**: Authenticated users receive a JWT token.

2. **Task Management**:

   - **Create Task**: Users can create tasks with details like title, description, status, and due date.
   - **Retrieve All Tasks**: Retrieve all tasks created by the authenticated user.
   - **Retrieve Single Task**: Retrieve a specific task by providing its ID.
   - **Update Task**: Allows partial updates of task details.
   - **Delete Task**: Deletes a specific task.

3. **Filtering and Sorting**:
   - Filter tasks by status (e.g., `Pending` or `Completed`).
   - Sort tasks by due date in ascending or descending order.

---

## Challenges Faced

1. **User Authentication**:
   - Integrating JWT authentication and ensuring secure token generation.

---

## API Endpoints

### Authentication

- **POST /register**: Register a new user.
- **POST /login**: Authenticate and receive a JWT token.

### Task Management

- **POST /task**: Create a new task.
- **GET /task**: Retrieve all tasks for the authenticated user.
- **GET /tasks/<task_id>**: Retrieve a specific task by its ID.
- **PATCH /tasks/<task_id>**: Update an existing task.
- **DELETE /tasks/<task_id>**: Delete a task.

### Filtering and Sorting

- **GET /task?status=Pending**: Filter tasks by status.
- **GET /task?ordering=-due_date**: Sort tasks by due date in descending order.

---
