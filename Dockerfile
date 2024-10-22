# Use the official Python image
FROM python:3.11.9-slim

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY /task_manager /app/task_manager

# Expose the port
EXPOSE 8000

# Run the application
CMD ["python", "task_manager/manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["sleep",  "infinity"]
